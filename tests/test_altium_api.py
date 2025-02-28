from py_altium365.altium_api import AltiumApi
from py_altium365.base.enums import PrtGlobalService


def test_user_login_correct(mocker):
    api = AltiumApi()

    mock_portal_con = mocker.Mock()
    mock_portal_con.login_user.return_value.success = True
    mock_portal_con.login_user.return_value.session_handle = "test_session_handle"
    api._portal_con = mock_portal_con

    mock_soapy_con_workspace = mocker.patch("py_altium365.altium_api.SoapyConWorkspace")
    mock_soapy_con_workspace.return_value = "test_soapy_con_workspace"

    assert api.login("test_user", "test_pass")
    assert api._session_guid == "test_session_handle"
    assert api._workspace_con == "test_soapy_con_workspace"
    assert mock_portal_con.login_user.called
    assert mock_soapy_con_workspace.called


def test_user_login_incorrect(mocker):
    api = AltiumApi()

    mock_portal_con = mocker.Mock()
    mock_portal_con.login_user.return_value.success = False
    mock_portal_con.login_user.return_value.message = "test_message"
    api._portal_con = mock_portal_con

    assert not api.login("test_user", "test_pass")
    assert api._session_guid is None
    assert api._workspace_con is None
    assert mock_portal_con.login_user.called


def test_user_login_incorrect_with_message(mocker):
    api = AltiumApi()

    mock_portal_con = mocker.Mock()
    mock_portal_con.login_user.return_value.success = False
    mock_portal_con.login_user.return_value.message = "test_message"
    api._portal_con = mock_portal_con

    assert api.login("test_user", "test_pass", return_message=True) == "test_message"
    assert api._session_guid is None
    assert api._workspace_con is None
    assert mock_portal_con.login_user.called


def test_user_login_connection_error(mocker):
    api = AltiumApi()

    mock_portal_con = mocker.Mock()
    mock_portal_con.login_user.side_effect = ConnectionError
    api._portal_con = mock_portal_con

    assert not api.login("test_user", "test_pass")
    assert api._session_guid is None
    assert api._workspace_con is None
    assert mock_portal_con.login_user.called


def test_login_workspace(mocker):
    api = AltiumApi()

    api.login = mocker.Mock()
    api.login.return_value = True

    mock_soapy_con_workspace = mocker.patch("py_altium365.altium_api.SoapyConServiceDiscovery")
    sd_login = mocker.Mock()
    mock_soapy_con_workspace.login = sd_login
    sd_login.return_value.user_info = True
    api._workspace_con = mock_soapy_con_workspace

    mocker.patch("py_altium365.altium_api.AltiumApiWorkspace", return_value="test_workspace")

    assert api.login_workspace("test_workspace", "test_user", "test_pass") == "test_workspace"


def test_get_service_url_cache(mocker):
    api = AltiumApi()

    api._service_urls = {
        PrtGlobalService.WORKSPACE.name: "test_workspace_url",
    }

    mock_portal_con = mocker.Mock()
    mock_portal_con.get_prt_global_service_url.return_value = "test_portal_url"
    api._portal_con = mock_portal_con

    assert api.get_service_url(PrtGlobalService.WORKSPACE) == "test_workspace_url"
    assert api.get_service_url(PrtGlobalService.WORKSPACE, True) == "test_portal_url"
    mock_portal_con.get_prt_global_service_url.assert_called_once_with(PrtGlobalService.WORKSPACE, None)


def test_get_service_url_no_cache(mocker):
    api = AltiumApi()

    api._service_urls = {}

    mock_portal_con = mocker.Mock()
    mock_portal_con.get_prt_global_service_url.return_value = "test_portal_url"
    api._portal_con = mock_portal_con

    assert api.get_service_url(PrtGlobalService.WORKSPACE) == "test_portal_url"
    mock_portal_con.get_prt_global_service_url.assert_called_once_with(PrtGlobalService.WORKSPACE, None)
