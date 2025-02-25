from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
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
    full_name: Optional[str] = element(tag="FullName", default=None)
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


class ServiceEndpoints(BaseModel):
    """Service endpoints."""

    ANNOTATIONS: Optional[str] = None
    APPLICATIONS: Optional[str] = None
    BMS: Optional[str] = None
    BOMSERVICE: Optional[str] = None
    BOMSERVICE_AD: Optional[str] = None
    CH: Optional[str] = None
    COMMENTS: Optional[str] = None
    COMMENTSBASE: Optional[str] = None
    COMMENTSUI: Optional[str] = None
    COMPARISONSERVICE: Optional[str] = None
    CollaborationService: Optional[str] = None
    CommentsCloud: Optional[str] = None
    Components: Optional[str] = None
    DDS: Optional[str] = None
    DICTIONARIES: Optional[str] = None
    DSS: Optional[str] = None
    EDS: Optional[str] = None
    EIS: Optional[str] = None
    EXPLORERSERVICE: Optional[str] = None
    FeatureChecking: Optional[str] = None
    IDS: Optional[str] = None
    IDSCloud: Optional[str] = None
    INUSE: Optional[str] = None
    ISR: Optional[str] = None
    Invitation: Optional[str] = None
    LIBRARY_MODELMETADATA_WORKER: Optional[str] = None
    LWTASKS: Optional[str] = None
    Library_Components_Api: Optional[str] = None
    Library_Parts_Api: Optional[str] = None
    MANAGEDFLOWS: Optional[str] = None
    MANAGEDLIBRARIESSERVICE: Optional[str] = None
    MCADCS: Optional[str] = None
    NOTIFICATIONSSERVICE: Optional[str] = None
    PARTCATALOG: Optional[str] = None
    PARTCATALOGUI: Optional[str] = None
    PARTCATALOG_API: Optional[str] = None
    PLMSYNC: Optional[str] = None
    PROJECTCOMPARESERVICE: Optional[str] = None
    PROJECTHISTORYSERVICE: Optional[str] = None
    PROJECTS: Optional[str] = None
    PROJECTSUI: Optional[str] = None
    PUSH: Optional[str] = None
    PushCloud: Optional[str] = None
    REQUIREMENTSSERVICE: Optional[str] = None
    SCHEDULER: Optional[str] = None
    SEARCH: Optional[str] = None
    SEARCHBASE: Optional[str] = None
    SEARCHTEMPLATES: Optional[str] = None
    SECURITY: Optional[str] = None
    SETTINGS: Optional[str] = None
    Sharing: Optional[str] = None
    TASKS: Optional[str] = None
    TC2: Optional[str] = None
    USERSUI: Optional[str] = None
    VAULT: Optional[str] = None
    VAULTUI: Optional[str] = None
    VCSSERVICE: Optional[str] = None
    VIEWER: Optional[str] = None


class SoapyConServiceDiscovery(SoapyCon):
    """SOAP connection to the Altium service discovery."""

    def __init__(self, workspace_url: str):
        super().__init__(ConnectionHandler.get_instance(), workspace_url + "/servicediscovery/servicediscovery.asmx")

        self.service_urls: ServiceEndpoints = ServiceEndpoints()
        self.user_info: Optional[SoapServiceDiscoveryLoginUserInfoResult] = None

    def login(
        self,
        user_name: str,
        password: str,
        secure_login: bool = False,
        option: DiscoveryLoginOption = DiscoveryLoginOption.NONE,
        product_name: str = "Altium Designer",
    ) -> bool:
        """Login to the service discovery."""

        response = self._send_command(
            None,
            SoapMethodServiceDiscoveryLogin(user_name=user_name, password=password, secure_login=secure_login, option=option, product_name=product_name),
            return_method=SoapServiceDiscoveryResponse,
            soap_action="http://altium.com/Login",
        )

        if response.login_result is None:
            return False

        for endpoint in response.login_result.endpoints:
            self.service_urls.__dict__[endpoint.service_kind.replace(".", "_")] = endpoint.service_url
        self.user_info = response.login_result.user_info
        return True
