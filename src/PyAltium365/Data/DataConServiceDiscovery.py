from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Dict, Union

from PyAltium365.Exceptions import DataException
from PyAltium365.Helpers.DataClassDict import dataclassdict, field_dict
from PyAltium365.Helpers.DictListHelper import get_from_dict_and_check_type

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class DiscoveryLoginOption(Enum):
    NONE = "None"
    KILL_EXISTING_SESSION = "KillExistingSession "
    USE_SEPARATE_SESSION = "UseSeparateSession"


@dataclass
@dataclassdict(check_parameter_sub_list=(("EndPointInfo",), "ServiceKind", "ServiceUrl"))
class ServiceEndpoints:
    altium_api: AltiumApi
    ARK: str = field_dict(dict_name=["ARK"], default=None)
    BMS: str = field_dict(dict_name=["BMS"], default=None)
    CH: str = field_dict(dict_name=["CH"], default=None)
    CollaborationService: str = field_dict(dict_name=["CollaborationService"], default=None)
    COMMENTS: str = field_dict(dict_name=["COMMENTS"], default=None)
    COMMENTSBASE: str = field_dict(dict_name=["COMMENTSBASE"], default=None)
    CommentsCloud: str = field_dict(dict_name=["CommentsCloud"], default=None)
    DATAACQUISITION: str = field_dict(dict_name=["DATAACQUISITION"], default=None)
    DSS: str = field_dict(dict_name=["DSS"], default=None)
    EDS: str = field_dict(dict_name=["EDS"], default=None)
    EIS: str = field_dict(dict_name=["EIS"], default=None)
    FeatureChecking: str = field_dict(dict_name=["FeatureChecking"], default=None)
    FILEACCESS: str = field_dict(dict_name=["FILEACCESS"], default=None)
    IDS: str = field_dict(dict_name=["IDS"], default=None)
    IDSCloud: str = field_dict(dict_name=["IDSCloud"], default=None)
    INUSE: str = field_dict(dict_name=["INUSE"], default=None)
    Invitation: str = field_dict(dict_name=["Invitation"], default=None)
    ISR: str = field_dict(dict_name=["ISR"], default=None)
    LWTASKS: str = field_dict(dict_name=["LWTASKS"], default=None)
    MANAGEDFLOWS: str = field_dict(dict_name=["MANAGEDFLOWS"], default=None)
    MANAGEDLIBRARIESSERVICE: str = field_dict(dict_name=["MANAGEDLIBRARIESSERVICE"], default=None)
    MCADCS: str = field_dict(dict_name=["MCADCS"], default=None)
    NOTIFICATIONSSERVICE: str = field_dict(dict_name=["NOTIFICATIONSSERVICE"], default=None)
    PARTCATALOG: str = field_dict(dict_name=["PARTCATALOG"], default=None)
    PARTCATALOGUI: str = field_dict(dict_name=["PARTCATALOGUI"], default=None)
    PLMSYNC: str = field_dict(dict_name=["PLMSYNC"], default=None)
    PROJECTCOMPARESERVICE: str = field_dict(dict_name=["PROJECTCOMPARESERVICE"], default=None)
    PROJECTHISTORYSERVICE: str = field_dict(dict_name=["PROJECTHISTORYSERVICE"], default=None)
    PROJECTS: str = field_dict(dict_name=["PROJECTS"], default=None)
    PROJECTSUI: str = field_dict(dict_name=["PROJECTSUI"], default=None)
    PUSH: str = field_dict(dict_name=["PUSH"], default=None)
    PushCloud: str = field_dict(dict_name=["PushCloud"], default=None)
    SCHEDULER: str = field_dict(dict_name=["SCHEDULER"], default=None)
    SEARCH: str = field_dict(dict_name=["SEARCH"], default=None)
    SEARCHBASE: str = field_dict(dict_name=["SEARCHBASE"], default=None)
    SEARCHTEMPLATES: str = field_dict(dict_name=["SEARCHTEMPLATES"], default=None)
    SECURITY: str = field_dict(dict_name=["SECURITY"], default=None)
    SETTINGS: str = field_dict(dict_name=["SETTINGS"], default=None)
    Sharing: str = field_dict(dict_name=["Sharing"], default=None)
    TASKS: str = field_dict(dict_name=["TASKS"], default=None)
    TC2: str = field_dict(dict_name=["TC2"], default=None)
    USERSUI: str = field_dict(dict_name=["USERSUI"], default=None)
    VAULT: str = field_dict(dict_name=["VAULT"], default=None)
    VAULTUI: str = field_dict(dict_name=["VAULTUI"], default=None)
    VCSSERVICE: str = field_dict(dict_name=["VCSSERVICE"], default=None)
    WEBREVIEW: str = field_dict(dict_name=["WEBREVIEW"], default=None)


@dataclass
@dataclassdict(check_parameter_sub_list=(("Parameters", "UserParameter"), "Name", "Value"))
class UserInfo:
    altium_api: AltiumApi
    AccountId: str = field_dict(dict_name=["AccountId"], default=None)
    ActivationStatus: str = field_dict(dict_name=["ActivationStatus"], default=None)
    AuthType: int = field_dict(dict_name=["AuthType"], default=None)
    AutoSync: bool = field_dict(dict_name=["AutoSync"], default=False)
    Badges: str = field_dict(dict_name=["Badges"], default=None)
    Country: str = field_dict(dict_name=["Country"], default=None)
    CreatedAt: datetime = field_dict(dict_name=["CreatedAt"], default=datetime.min, dict_conv_str=('([0-9- :]*)[.]\\d*', '%Y-%m-%d %H:%M:%S'))
    CreatedByGUID: str = field_dict(dict_name=["CreatedByGUID"], default=None)
    CurrentPosition: str = field_dict(dict_name=["CurrentPosition"], default=None)
    DefaultAvatarBrush: str = field_dict(dict_name=["DefaultAvatarBrush"], default=None)
    DisplayName: str = field_dict(dict_name=["DisplayName"], default=None)
    Domain: str = field_dict(dict_name=["Domain"], default=None)
    Email: str = field_dict(dict_name=["Email"], default=None)
    ExampleWork: str = field_dict(dict_name=["Badges"], default=None)
    Experience: str = field_dict(dict_name=["Experience"], default=None)
    Fax: str = field_dict(dict_name=["Fax"], default=None)
    Features: List[str] = field(default_factory=lambda: [])
    FirstName: str = field_dict(dict_name=["FirstName"], default=None)
    FullName: str = field_dict(dict_name=["FullName"], default=None)
    GlobalUserGUID: str = field_dict(dict_name=["GlobalUserGUID"], default=None)
    HideEmail: bool = field_dict(dict_name=["HideEmail"], default=False)
    HRID: str = field_dict(dict_name=["HRID"], default=None)
    IDSHostName: str = field_dict(dict_name=["IDSHostName"], default=None)
    IsActive: bool = field_dict(dict_name=["IsActive"], default=False)
    LanguageLocaleKey: str = field_dict(dict_name=["LanguageLocaleKey"], default=None)
    LastModifiedAt: datetime = field_dict(dict_name=["LastModifiedAt"], default=datetime.min, dict_conv_str=('([0-9- :]*)[.]\\d*', '%Y-%m-%d %H:%M:%S'))
    LastModifiedByGUID: str = field_dict(dict_name=["LastModifiedByGUID"], default=None)
    LastName: str = field_dict(dict_name=["LastName"], default=None)
    LocaleSidKey: str = field_dict(dict_name=["LocaleSidKey"], default=None)
    Organisation: str = field_dict(dict_name=["Organisation"], default=None)
    Phone: str = field_dict(dict_name=["Phone"], default=None)
    ProfilePicture: str = field_dict(dict_name=["ProfilePicture"], default=None)
    ReputationPoints: int = field_dict(dict_name=["ReputationPoints"], default=None)
    Salutation: str = field_dict(dict_name=["Salutation"], default=None)
    SessionId: str = field_dict(dict_name=["SessionId"], default=None)
    Specialties: str = field_dict(dict_name=["Specialties"], default=None)
    TimeZoneSidKey: str = field_dict(dict_name=["TimeZoneSidKey"], default=None)
    UserId: str = field_dict(dict_name=["UserId"], default=None)
    UserName: str = field_dict(dict_name=["UserName"], default=None)
    WebSite: str = field_dict(dict_name=["WebSite"], default=None)

    def _from_dict(self, items: Dict[str, Union[str, Dict]]) -> None:
        try:
            features = get_from_dict_and_check_type(items, "Features", dict)
            strings = get_from_dict_and_check_type(features, "string", list)
            for string in strings:
                self.Features.append(string)
        except DataException:
            pass


@dataclass
@dataclassdict
class DiscoveryConfig:
    altium_api: AltiumApi
    Guid: str = field_dict(dict_name=["Guid"], default=None)
    Hrid: str = field_dict(dict_name=["Hrid"], default=None)
    Description: str = field_dict(dict_name=["Description"], default=None)
