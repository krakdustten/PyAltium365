from typing import Tuple, Any

import pytest

from py_altium365.altium_api_workspace import AltiumApiWorkspace


def create_workspace_api(mocker) -> Tuple[AltiumApiWorkspace, Any]:
    workspace_url = "test_workspace_url"
    service_discovery = mocker.Mock()
    service_discovery.user_info.session_id = "test_session_id"
    service_discovery.service_urls.SEARCHBASE = "test_search_base_url"
    return AltiumApiWorkspace(workspace_url, service_discovery), service_discovery


def test_init(mocker):
    workspace_url = "test_workspace_url"
    service_discovery = mocker.Mock()
    service_discovery.user_info.session_id = "test_session_id"
    service_discovery.service_urls.SEARCHBASE = "test_search_base_url"

    api_workspace = AltiumApiWorkspace(workspace_url, service_discovery)
    assert api_workspace._workspace_url == workspace_url
    assert api_workspace._service_discovery == service_discovery
    assert api_workspace._session_guid == service_discovery.user_info.session_id
    assert api_workspace._service_discovery.service_urls.SEARCHBASE == "test_search_base_url"


def test_init_no_user_info(mocker):
    workspace_url = "test_workspace_url"
    service_discovery = mocker.Mock()
    service_discovery.user_info = None

    with pytest.raises(ConnectionError):
        AltiumApiWorkspace(workspace_url, service_discovery)


def test_init_no_search_base_url(mocker):
    workspace_url = "test_workspace_url"
    service_discovery = mocker.Mock()
    service_discovery.user_info.session_id = "test_session_id"
    service_discovery.service_urls.SEARCHBASE = None

    with pytest.raises(ConnectionError):
        AltiumApiWorkspace(workspace_url, service_discovery)


def test_create_search_object(mocker):
    api, service_discovery = create_workspace_api(mocker)
    service_discovery.service_urls.SEARCHBASE = "test_search_base_url"
    mocker.patch("py_altium365.altium_api_workspace.JsonConSearchAsync", return_value="TEST")

    assert api.create_search_object() == "TEST"


def test_create_search_object_no_search_base_url(mocker):
    api, service_discovery = create_workspace_api(mocker)
    service_discovery.service_urls.SEARCHBASE = None

    with pytest.raises(ConnectionError):
        api.create_search_object()
