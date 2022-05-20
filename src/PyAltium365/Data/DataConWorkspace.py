from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from PyAltium365.Data.DataConPortal import Account
from PyAltium365.Helpers.DataClassDict import dataclassdict, field_dict

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class ServiceDiscoverProductName(Enum):
    AltiumDesigner = "Altium Designer"


@dataclass
@dataclassdict
class UserWorkspace:
    altium_api: AltiumApi
    CreateDate: datetime = field_dict(dict_name=["createdate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    Creator: str = field_dict(dict_name=["creator"], default=None)
    CurrentUserCount: int = field_dict(dict_name=["currentusercount"], default=None)
    Description: str = field_dict(dict_name=["description"], default=None)
    DisplayHostingUrl: str = field_dict(dict_name=["displayhostingurl"], default=None)
    ExpirationDate: datetime = field_dict(dict_name=["expirationdate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    HostingUrl: str = field_dict(dict_name=["hostingurl"], default=None)
    IsAdministrator: bool = field_dict(dict_name=["isadministrator"], default=False)
    IsDefault: bool = field_dict(dict_name=["isdefault"], default=False)
    LegacyHostingUrl: str = field_dict(dict_name=["legacyhostingurl"], default=None)
    LocationId: int = field_dict(dict_name=["locationid"], default=None)
    LocationName: str = field_dict(dict_name=["locationname"], default=None)
    MaxUser: int = field_dict(dict_name=["maxuser"], default=None)
    Name: str = field_dict(dict_name=["name"], default=None)
    OwnerAccountGuid: str = field_dict(dict_name=["owneraccountguid"], default=None)
    OwnerId: int = field_dict(dict_name=["ownerid"], default=None)
    SpaceSubscriptionGuid: str = field_dict(dict_name=["spacesubscriptionguid"], default=None)
    StartDate: datetime = field_dict(dict_name=["startdate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    Status: int = field_dict(dict_name=["status"], default=None)
    StatusName: str = field_dict(dict_name=["statusname"], default=None)
    Type: int = field_dict(dict_name=["type"], default=None)
    TypeName: str = field_dict(dict_name=["typename"], default=None)
    WorkspaceId: int = field_dict(dict_name=["workspaceid"], default=None)

    def get_owner_account(self) -> Optional[Account]:
        return self.altium_api.get_account_details(self.OwnerAccountGuid)

    def get_subscription_space(self) -> None:
        raise NotImplementedError()
