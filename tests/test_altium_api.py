import os
from dotenv import load_dotenv  # type: ignore

from py_altium365.altium_api import AltiumApi
from py_altium365.base.enums import PrtGlobalService


def _generate_api() -> AltiumApi:
    api = AltiumApi()
    load_dotenv()
    test_user = os.environ.get("ALTIUM_USER")
    test_pass = os.environ.get("ALTIUM_PASS")
    if test_user is None or test_pass is None:
        assert False
    api.login(test_user, test_pass)
    return api


def test_user_login_correct():
    api = AltiumApi()
    load_dotenv()
    test_user = os.environ.get("ALTIUM_USER")
    test_pass = os.environ.get("ALTIUM_PASS")
    if test_user is None or test_pass is None:
        assert False
    assert api.login(test_user, test_pass)


def test_user_login_incorrect():
    api = AltiumApi()
    test_user = "test"
    test_pass = "test"
    assert not api.login(test_user, test_pass)


def test_user_workspace_login():
    api = _generate_api()
    workspaces = api.get_user_workspaces()
    assert workspaces is not None
    assert len(workspaces) > 1
    assert api.login_workspace(workspaces[0], os.environ.get("ALTIUM_USER"), os.environ.get("ALTIUM_PASS"))
    api2 = AltiumApi()
    assert api2.login_workspace(workspaces[0], os.environ.get("ALTIUM_USER"), os.environ.get("ALTIUM_PASS"))


def test_get_service_url():
    api = _generate_api()
    assert api.get_service_url(PrtGlobalService.WORKSPACE) == "https://workspaces.altium.com/workspaceexternalservices/WorkspaceHelperService.asmx"


def test_get_user_workspaces():
    api = _generate_api()
    workspaces = api.get_user_workspaces()
    assert workspaces is not None
    assert len(workspaces) > 1
