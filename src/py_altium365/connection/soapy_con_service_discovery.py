from enum import Enum
from typing import List, Optional

from pydantic_xml import BaseXmlModel, element, wrapped

from py_altium365.base.connection_handler import ConnectionHandler
from py_altium365.connection.soapy_con import SoapMethod, SoapResponse, SoapyCon


class DiscoveryLoginOption(str, Enum):
    """Discovery login options."""

    NONE = "None"
    KILL_EXISTING_SESSION = "KillExistingSession"
    USE_SEPARATE_SESSION = "UseSeparateSession"


class SoapMethodServiceDiscoveryLogin(
    SoapMethod,
    tag="Login",
    nsmap={"": "http://altium.com/"},
    ns="",
):
    """SOAP method for login to the service discovery."""

    user_name: str = element(tag="userName")
    password: str = element(tag="password")
    secure_login: bool = element(tag="secureLogin", default=False)
    option: DiscoveryLoginOption = element(tag="discoveryLoginOptions", default=DiscoveryLoginOption.NONE)
    product_name: str = element(tag="productName")


class SoapEndPointInfo(BaseXmlModel, tag="EndPointInfo", ns="", nsmap={"": "http://altium.com/"}):
    """SOAP Parameter."""

    service_kind: str = element(tag="ServiceKind")
    service_url: Optional[str] = element(tag="ServiceUrl", default=None)


class SoapUserParameter(BaseXmlModel, tag="UserParameter", ns="", nsmap={"": "http://altium.com/"}):
    """SOAP Parameter."""

    name: str = element(tag="Name")
    value: Optional[str] = element(tag="Value", default=None)


class SoapServiceDiscoveryLoginUserInfoResult(
    BaseXmlModel,
    tag="UserInfo",
    ns="",
    nsmap={"": "http://altium.com/"},
):
    """SOAP Login result for the SOAP login call in the service discovery."""

    session_id: str = element(tag="SessionId")
    user_id: str = element(tag="UserId")
    domain: Optional[str] = element(tag="Domain", default=None)
    account_id: str = element(tag="AccountId")
    email: str = element(tag="Email")
    user_name: str = element(tag="UserName")
    first_name: str = element(tag="FirstName")
    last_name: str = element(tag="LastName")
    full_name: str = element(tag="FullName")
    organisation: str = element(tag="Organisation")
    auth_type: int = element(tag="AuthType")
    parameters: List[SoapUserParameter] = wrapped(
        path="Parameters",
        tag="UserParameter",
        default=[],
    )
    features: List[str] = wrapped(
        path="Features",
        entity=element(tag="string", default=None),
        default=[],
    )


class SoapServiceDiscoveryLoginResult(
    BaseXmlModel,
    tag="LoginResult",
    ns="",
    nsmap={"": "http://altium.com/"},
):
    """SOAP Login result for the SOAP login call."""

    endpoints: List[SoapEndPointInfo] = wrapped(
        path="Endpoints",
        tag="EndPointInfo",
        default=[],
    )
    user_info: SoapServiceDiscoveryLoginUserInfoResult


class SoapServiceDiscoveryResponse(
    SoapResponse,
    tag="LoginResponse",
    ns="",
    nsmap={"": "http://altium.com/"},
):
    """SOAP Login response."""

    login_result: SoapServiceDiscoveryLoginResult


class SoapyConServiceDiscovery(SoapyCon):
    """SOAP connection to the Altium service discovery."""

    def __init__(self, workspace_url: str):
        super().__init__(ConnectionHandler.get_instance(), workspace_url + "/servicediscovery/servicediscovery.asmx")

    def login(
        self,
        user_name: str,
        password: str,
        secure_login: bool = False,
        option: DiscoveryLoginOption = DiscoveryLoginOption.NONE,
        product_name: str = "Altium Designer",
    ):
        """Login to the service discovery."""

        response = self._send_command(
            None,
            SoapMethodServiceDiscoveryLogin(user_name=user_name, password=password, secure_login=secure_login, option=option, product_name=product_name),
            return_method=SoapServiceDiscoveryResponse,
            soap_action="http://altium.com/Login",
        )

        print(response)
