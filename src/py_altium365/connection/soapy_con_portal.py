from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic_xml import BaseXmlModel, element, wrapped

from py_altium365.base.connection_handler import ConnectionHandler
from py_altium365.base.enums import PrtGlobalService
from py_altium365.connection.soapy_con import (
    SoapHeader,
    SoapMethod,
    SoapResponse,
    SoapyCon,
)

if TYPE_CHECKING:
    from py_altium365.altium_api import AltiumApi


class SoapHeaderApi(
    SoapHeader,
    tag="Header",
    ns="soap",
):
    """SOAP header for an API call."""

    api_version: str = element(tag="APIVersion", default="2.0", nsmap={"": "http://tempuri.org/"})


class SoapMethodLogin(
    SoapMethod,
    tag="Login",
    nsmap={"temp": "http://tempuri.org/"},
    ns="temp",
):
    """SOAP method for login."""

    username: str = element(tag="Username")
    password: str = element(tag="Password")


class SoapProfilePicture(BaseXmlModel, tag="ProfilePicture"):
    """SOAP Profile picture."""

    small_link: Optional[str] = element(tag="Small", default=None)
    medium_link: Optional[str] = element(tag="Medium", default=None)
    large_link: Optional[str] = element(tag="Large", default=None)
    full_link: Optional[str] = element(tag="Full", default=None)


class SoapParameter(BaseXmlModel, tag="Parameter", ns="temp", nsmap={"temp": "http://tempuri.org/"}):
    """SOAP Parameter."""

    name: str = element(tag="Name")
    value: Optional[str] = element(tag="Value", default=None)


class SoapLoginResult(
    BaseXmlModel,
    tag="LoginResult",
    ns="temp",
    nsmap={"i": "http://www.w3.org/2001/XMLSchema-instance", "temp": "http://tempuri.org/"},
):
    """SOAP Login result for the SOAP login call."""

    message: Optional[str] = element(tag="Message", default=None)
    success: bool = element(tag="Success")
    session_handle: Optional[str] = element(tag="SessionHandle", default=None)
    user_name: Optional[str] = element(tag="UserName", default=None)
    first_name: Optional[str] = element(tag="FirstName", default=None)
    last_name: Optional[str] = element(tag="LastName", default=None)
    full_name: Optional[str] = element(tag="FullName", default=None)
    time_zone_sid_key: Optional[str] = element(tag="TimeZoneSidKey", default=None)
    language_locale_key: Optional[str] = element(tag="LanguageLocaleKey", default=None)
    locale_sid_key: Optional[str] = element(tag="LocaleSidKey", default=None)
    user_rights_string: Optional[str] = element(tag="UserRightsString", default=None)
    contact_guid: Optional[str] = element(tag="ContactGUID", default=None)
    email: Optional[str] = element(tag="Email", default=None)
    last_login_date: Optional[datetime] = element(tag="LastLoginDate", default=None)
    password_expired: Optional[bool] = element(tag="PasswordExpired", default=None)
    profile_picture: Optional[SoapProfilePicture] = element(tag="ProfilePicture", default=None)
    parameters: List[SoapParameter] = wrapped(
        path="Parameters",
        tag="Parameter",
        default=[],
    )
    fault_code: Optional[str] = element(tag="FaultCode", default=None)
    allowed_features: List[str] = wrapped(
        path="AllowedFeatures",
        entity=element(tag="string", ns="a", default=None),
        nsmap={
            "a": "http://schemas.microsoft.com/2003/10/Serialization/Arrays",
        },
        default=[],
    )
    secured_session_handle: Optional[str] = element(tag="SecuredSessionHandle", default=None)


class SoapLoginResponse(
    SoapResponse,
    tag="LoginResponse",
    ns="temp",
    nsmap={"temp": "http://tempuri.org/"},
):
    """SOAP Login response."""

    login_result: SoapLoginResult


class SoapMethodGetPrtGlobalServiceUrl(
    SoapMethod,
    tag="GetPRT_GlobalServiceUrl",
    nsmap={"temp": "http://tempuri.org/"},
    ns="temp",
):
    """SOAP method for getting a PRT global service URL."""

    handle: Optional[str] = element(tag="Handle", default=None)
    service_name: str = element(tag="ServiceName")
    set_name: str = element(tag="SetName")


class SoapGetPrtGlobalServiceUrlResponse(
    SoapResponse,
    tag="GetPRT_GlobalServiceUrlResponse",
    ns="temp",
    nsmap={"temp": "http://tempuri.org/"},
):
    """SOAP response for getting a PRT global service URL."""

    service_url: Optional[str] = element(tag="ServiceURL", nsmap={"temp": "http://tempuri.org/"}, default=None)


class SoapyConPortal(SoapyCon):
    """SOAP connection to the Altium portal."""

    def __init__(self, altium_api: AltiumApi) -> None:
        """
        Initialize the SOAP connection to the Altium portal.
        :param altium_api: The Altium API object.
        """
        super().__init__(ConnectionHandler.get_instance(), "https://portal365.altium.com/?cls=soap")
        self._altium_api = altium_api

    def login_user(self, username: str, password: str) -> SoapLoginResult:
        """
        Login a user to the Altium portal.
        :param username: The altium username.
        :param password: The altium password.
        :return: The user login result.
        """
        response = self._send_command(
            SoapHeaderApi(),
            SoapMethodLogin(username=username, password=password),
            return_method=SoapLoginResponse,
        )

        return response.login_result

    def get_prt_global_service_url(self, service: PrtGlobalService, handle: Optional[str] = None) -> Optional[str]:
        """
        Get a PRT global service URL.
        :param service: The PRT global service to get the URL for.
        :param handle: A handle for the service.
        :return: The service URL.
        """
        if handle is None and service == service.is_guid_req:  # type: ignore
            raise ValueError(f"Handle is required for {service.name} service")
        if not service.is_guid_req:
            handle = None

        response = self._send_command(
            SoapHeaderApi(),
            SoapMethodGetPrtGlobalServiceUrl(
                handle=handle,
                service_name=service.service_name,
                set_name=service.set_name,
            ),
            return_method=SoapGetPrtGlobalServiceUrlResponse,
        )
        return response.service_url
