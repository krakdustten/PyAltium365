from datetime import datetime
from typing import List, Optional

from pydantic_xml import BaseXmlModel, element

from py_altium365.base.connection_handler import ConnectionHandler
from py_altium365.base.enums import PrtGlobalService
from py_altium365.connection.soapy_con import (
    SoapHeader,
    SoapMethod,
    SoapResponse,
    SoapyCon,
)


class SoapUserCredentials(
    BaseXmlModel,
    tag="UserCredentials",
    ns="temp",
    nsmap={"temp": "http://tempuri.org/"},
):
    """SOAP user credentials."""

    user_id: Optional[int] = element(tag="userid", default=None)
    password: str = element(tag="password", nmap={"temp": "http://tempuri.org/"}, ns="temp")


class SoapHeaderCredentials(
    SoapHeader,
    tag="Header",
    ns="soap",
):
    """SOAP header for an API call."""

    user_credentials: SoapUserCredentials


class SoapMethodGetUserWorkspaces(
    SoapMethod,
    tag="GetUserWorkspaces",
    nsmap={"temp": "http://tempuri.org/"},
    ns="temp",
):
    """SOAP method for login."""


class UserWorkspaceInfo(BaseXmlModel, tag="UserWorkspaceInfo", ns="temp", nsmap={"temp": "http://tempuri.org/"}):
    """User workspace information."""

    workspace_id: int = element(tag="workspaceid")
    owner_id: int = element(tag="ownerid")
    name: str = element(tag="name")
    create_date: datetime = element(tag="createdate")
    status: int = element(tag="status")
    start_date: datetime = element(tag="startdate")
    expiration_date: datetime = element(tag="expirationdate")
    max_user: int = element(tag="maxuser")
    current_user_count: int = element(tag="currentusercount")
    type: int = element(tag="type")
    type_name: str = element(tag="typename")
    hosting_url: str = element(tag="hostingurl")
    space_subscription_guid: str = element(tag="spacesubscriptionguid")
    description: str = element(tag="description", default="")
    display_hosting_url: str = element(tag="displayhostingurl")
    location_id: int = element(tag="locationid")
    creator: str = element(tag="creator")
    location_name: str = element(tag="locationname")
    is_administrator: bool = element(tag="isadministrator", default=False)
    is_default: bool = element(tag="isdefault", default=False)
    status_name: str = element(tag="statusname")
    legacy_hosting_url: str = element(tag="legacyhostingurl")
    owner_account_guid: str = element(tag="owneraccountguid")
    has_administrators: bool = element(tag="hasadministrators", default=False)
    owner_user_guid: str = element(tag="owneruserguid")
    is_secure: bool = element(tag="issecure", default=False)


class SoapGetUserWorkspacesResult(
    BaseXmlModel,
    tag="GetUserWorkspacesResult",
    ns="temp",
    nsmap={"temp": "http://tempuri.org/"},
):
    """SOAP Login result for the SOAP login call."""

    workspaces: List[UserWorkspaceInfo]


class SoapGetUserWorkspacesResponse(
    SoapResponse,
    tag="GetUserWorkspacesResponse",
    nsmap={"temp": "http://tempuri.org/"},
    ns="temp",
):
    """SOAP method for login."""

    result: SoapGetUserWorkspacesResult


class SoapyConWorkspace(SoapyCon):
    """
    SOAP connection to the Altium workspace.
    """

    def __init__(self, altium_api):
        """
        Initialize the SOAP connection to the Altium portal.
        :param altium_api: The Altium API object.
        """
        workspace_url = altium_api.get_service_url(PrtGlobalService.WORKSPACE)
        if workspace_url is None:
            raise ConnectionError("Failed to get workspace URL")
        super().__init__(ConnectionHandler.get_instance(), workspace_url)
        self._altium_api = altium_api

    def get_user_workspaces(self, session_guid: str):
        """
        Get the user workspaces
        :param session_guid: The session GUID
        :return: The user workspaces
        """
        response = self._send_command(
            SoapHeaderCredentials(user_credentials=SoapUserCredentials(password=session_guid)),
            SoapMethodGetUserWorkspaces(),
            return_method=SoapGetUserWorkspacesResponse,
            soap_action="http://tempuri.org/GetUserWorkspaces",
        )

        return response.result.workspaces
