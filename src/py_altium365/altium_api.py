from typing import List, Optional, Union

from py_altium365.altium_api_workspace import AltiumApiWorkspace
from py_altium365.base.enums import PrtGlobalService
from py_altium365.connection.soapy_con_portal import SoapyConPortal
from py_altium365.connection.soapy_con_service_discovery import SoapyConServiceDiscovery
from py_altium365.connection.soapy_con_workspace import (
    SoapyConWorkspace,
    UserWorkspaceInfo,
)


class AltiumApi:
    """
    Altium API class
    """

    def __init__(self) -> None:
        """
        Initialize the Altium API object
        """

        # Global variables

        self._portal_con: SoapyConPortal = SoapyConPortal(self)
        self._session_guid: Optional[str] = None
        self._service_urls: dict[str, str] = {}
        self._workspace_con: Optional[SoapyConWorkspace] = None

        # Workspace variables
        self._service_discovery_con: Optional[SoapyConServiceDiscovery] = None

    def login(self, username: str, password: str, return_message: bool = False) -> Union[str, bool]:
        """
        Login to the Altium API
        :param username: The altium username
        :param password: The altium password
        :param return_message: If the login fails, return the message
        :return: True if the login was successful, False otherwise or the message if return_message is True
        """
        try:
            user_login = self._portal_con.login_user(username, password)
            if not user_login.success:
                if return_message and user_login.message is not None:
                    return user_login.message
                return False
            self._session_guid = user_login.session_handle
            self._workspace_con = SoapyConWorkspace(self)
        except ConnectionError:
            return False
        return True

    def login_workspace(
        self, workspace: Union[UserWorkspaceInfo, str], username: str, password: str, return_message: bool = False, force_login: bool = False
    ) -> Optional[AltiumApiWorkspace]:
        """
        Login to a workspace
        :param workspace: The url of the workspace or the UserWorkspaceInfo object
        :param username: The altium username
        :param password: The altium password
        :param return_message: If the login fails, return the message
        :param force_login: Force a user login even if the session is already active
        :return: True if the login was successful, False otherwise or the message if return_message is True
        """
        if self._session_guid is None or force_login:
            msg = self.login(username, password, return_message)
            if msg is not True:
                return None
        if isinstance(workspace, UserWorkspaceInfo):
            workspace = workspace.hosting_url
        if not isinstance(workspace, str):
            return None
        # ODO: Implement workspace login
        service_discovery_con = SoapyConServiceDiscovery(workspace)
        service_discovery_con.login(username, password)
        if not service_discovery_con.user_info:
            return None
        return AltiumApiWorkspace(workspace, service_discovery_con)

    def get_service_url(self, service: PrtGlobalService, force_request: bool = False) -> Optional[str]:
        """
        Get a service URL
        :param service: The service to get the URL for
        :param force_request: If the URL should be requested again from altium or use the cached URL
        :return: The service URL
        """
        if service.name in self._service_urls and not force_request:
            return self._service_urls[service.name]
        url = self._portal_con.get_prt_global_service_url(service, self._session_guid)
        if url is not None:
            self._service_urls[service.name] = url
        return url

    def get_user_workspaces(self) -> List[UserWorkspaceInfo]:
        """
        Get the user workspaces
        :return: The user workspaces
        """
        if self._workspace_con is None:
            return []
        if self._session_guid is None:
            return []
        return self._workspace_con.get_user_workspaces(self._session_guid)
