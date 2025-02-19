from dataclasses import dataclass
from enum import Enum


@dataclass()
class PrtService:
    """
    Data class for the PRT Service
    """

    service_name: str
    set_name: str
    is_guid_req: bool


class PrtGlobalService(PrtService, Enum):
    """
    Enum for the PRT Global Service
    """

    CIIVA = ("CiivaApi", "Secure", False)
    ENGAGEMENT_PAGE = ("EngagementPage", "Secure", False)
    VAULT_CONTENT_SERVICE = ("VaultContentServiceURL", "Secure", True)
    STAT_SERVICE = ("StatServiceURL", "Secure", True)
    WORKSPACE = ("WorkspacesUrl", "Secure", True)
    PART_CATALOG = ("PartCatalogUrl", "Secure", True)
    A365_USER_PROFILE = ("A365UserProfile", "Secure", True)
    A365_VALIDATESESION = ("A365ValidateSession", "Secure", True)
    AD_PAYMENT_SERVICE = ("ADPaymentService", "Secure", True)
    APP_REGISTRY = ("AppRegistryUrl", "Secure", True)

    # def __new__(cls, name: str, set_name: str, is_guid_req: bool):
    #     obj = object.__new__(cls)
    #     obj._value_ = name
    #     obj.service_name = name  # type: ignore
    #     obj.set_name = set_name  # type: ignore
    #     obj.is_guid_req = is_guid_req  # type: ignore
    #     return obj

    # def __init__(self, name: str, set_name: str, is_guid_req: bool):
    #     self.name = name
    #     self.set_name = set_name
    #     self.is_guid_req = is_guid_req
