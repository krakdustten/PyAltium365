from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Union, List, TYPE_CHECKING, Optional

from PyAltium365.Exceptions import DataException
from PyAltium365.Helpers.DataClassDict import field_dict, dataclassdict
from PyAltium365.Helpers.DictListHelper import get_from_dict_and_check_type

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi
    from PyAltium365.Data.DataConPortalPredef import GroupLicenseAssignment, User, Account


class PrtGlobalServiceName(Enum):
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


class PrtSettings(Enum):
    CIIVA_USER_NAME = ("CiivaUserName", False, str)
    CIIVA_PASSWORD = ("CiivaPassword", False, str)
    FREQUENCY_REFRESH_LIST_OF_WORKSPACES = ("FrequencyRefreshListOfWorkspaces", True, int)


@dataclass
@dataclassdict
class UserLogin:
    altium_api: AltiumApi

    AllowedFeatures: list = field(default_factory=lambda: [])
    ContactGUID: str = field_dict(dict_name=["ContactGUID"], default=None)
    Email: str = field_dict(dict_name=["Email"], default=None)
    FaultCode: str = field_dict(dict_name=["FaultCode"], default=None)
    FirstName: str = field_dict(dict_name=["FirstName"], default=None)
    FullName: str = field_dict(dict_name=["FullName"], default=None)
    LanguageLocaleKey: str = field_dict(dict_name=["LanguageLocaleKey"], default=None)
    LastLoginDate: datetime = field_dict(dict_name=["LastLoginDate"], default=datetime.min, dict_conv_str=('([0-9-T:]*)[.]\\d*Z', '%Y-%m-%dT%H:%M:%S'))
    LastName: str = field_dict(dict_name=["LastName"], default=None)
    LocaleSidKey: str = field_dict(dict_name=["LocaleSidKey"], default=None)
    Message: str = field_dict(dict_name=["Message"], default=None)
    Parameters: dict = field(default_factory=lambda: {})
    PasswordExpired: bool = field_dict(dict_name=["PasswordExpired"], default=False)
    ProfilePicture: dict = field(default_factory=lambda: {})
    SessionHandle: str = field_dict(dict_name=["SessionHandle"], default=None)
    Success: bool = field_dict(dict_name=["Success"], default=False)
    TimeZoneSidKey: str = field_dict(dict_name=["TimeZoneSidKey"], default=None)
    UserName: str = field_dict(dict_name=["UserName"], default=None)
    UserRightsString: str = field_dict(dict_name=["UserRightsString"], default=None)

    def _from_dict(self, items: Dict[str, Union[str, Dict]]) -> None:
        try:
            parameters = get_from_dict_and_check_type(items, "Parameters", dict)
            parameters2 = get_from_dict_and_check_type(parameters, "Parameter", dict)
            for parameter in parameters2:
                name = get_from_dict_and_check_type(parameter, "Name", str)
                value = get_from_dict_and_check_type(parameter, "Value", str)
                self.Parameters[name] = value
        except DataException:
            pass

        profilepictures = get_from_dict_and_check_type(items, "ProfilePicture", dict)
        self.ProfilePicture["Small"] = get_from_dict_and_check_type(profilepictures, "Small", str)
        self.ProfilePicture["Medium"] = get_from_dict_and_check_type(profilepictures, "Medium", str)
        self.ProfilePicture["Large"] = get_from_dict_and_check_type(profilepictures, "Large", str)
        self.ProfilePicture["Full"] = get_from_dict_and_check_type(profilepictures, "Full", str)
        try:
            allowed_features = get_from_dict_and_check_type(items, "AllowedFeatures", dict)
            allowed_features2 = get_from_dict_and_check_type(allowed_features, "string", dict)
            for allowed_feature in allowed_features2:
                self.AllowedFeatures.append(allowed_feature)
        except DataException:
            pass
        return None


@dataclass
@dataclassdict
class License:
    altium_api: AltiumApi

    ActivationCode: str = field_dict(dict_name=["ActivationCode"], default=None)
    Autoname: str = field_dict(dict_name=["Autoname"], default=None)
    BoardUniqueId: str = field_dict(dict_name=["BoardUniqueId"], default=None)
    CampaignCode: str = field_dict(dict_name=["CampaignCode"], default=None)
    ContactFirstName: str = field_dict(dict_name=["ContactFirstName"], default=None)
    ContactGUID: str = field_dict(dict_name=["ContactGUID"], default=None)
    ContactLastName: str = field_dict(dict_name=["ContactLastName"], default=None)
    CreatedAt: datetime = field_dict(dict_name=["CreatedAt"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    CreatedByGUID: str = field_dict(dict_name=["CreatedByGUID"], default=None)
    DesignCapabilityGuid: str = field_dict(dict_name=["DesignCapabilityGuid"], default=None)
    DurationDays: int = field_dict(dict_name=["DurationDays"], default=None)
    GUID: str = field_dict(dict_name=["GUID"], default=None)
    GeographicScopeGUID: str = field_dict(dict_name=["GeographicScopeGUID"], default=None)
    GeographicScopeName: str = field_dict(dict_name=["GeographicScopeName"], default=None)
    IsActive: bool = field_dict(dict_name=["IsActive"], default=False)
    LastModifiedByGUID: str = field_dict(dict_name=["LastModifiedByGUID"], default=None)
    LastModifiedDate: datetime = field_dict(dict_name=["LastModifiedDate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    LicenseEnabled: bool = field_dict(dict_name=["LicenseEnabled"], default=False)
    LicenseKindGUID: str = field_dict(dict_name=["LicenseKindGUID"], default=None)
    LicenseTypeName: str = field_dict(dict_name=["LicenseTypeName"], default=None)
    LicenseUsageGUID: str = field_dict(dict_name=["LicenseUsageGUID"], default=None)
    LicenseUsageName: str = field_dict(dict_name=["LicenseUsageName"], default=None)
    OwnerAccountGUID: str = field_dict(dict_name=["OwnerAccountGUID"], default=None)
    OwnerGUID: str = field_dict(dict_name=["OwnerGUID"], default=None)
    OwnershipCertificateGUID: str = field_dict(dict_name=["OwnershipCertificateGUID"], default=None)
    PermissionSetCapabilitySequence: int = field_dict(dict_name=["PermissionSetCapabilitySequence"], default=None)
    PermissionSetFamilyName: str = field_dict(dict_name=["PermissionSetFamilyName"], default=None)
    PermissionSetFamilySequence: str = field_dict(dict_name=["PermissionSetFamilySequence"], default=None)
    PermissionSetGUID: str = field_dict(dict_name=["PermissionSetGUID"], default=None)
    PermissionSetName: str = field_dict(dict_name=["PermissionSetName"], default=None)
    PlatformOS: str = field_dict(dict_name=["PlatformOS"], default=None)
    ProductGUID: str = field_dict(dict_name=["ProductGUID"], default=None)
    ProductLineGUID: str = field_dict(dict_name=["ProductLineGUID"], default=None)
    RightToUpgradeExpiryDate: datetime = field_dict(dict_name=["RightToUpgradeExpiryDate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    SerialNumber: int = field_dict(dict_name=["SerialNumber"], default=None)
    StartDate: datetime = field_dict(dict_name=["StartDate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    SubscriptionGUID: str = field_dict(dict_name=["SubscriptionGUID"], default=None)
    Summer08PermissionSetEntitlementGUID: str = field_dict(dict_name=["Summer08PermissionSetEntitlementGUID"], default=None)
    UserCount: int = field_dict(dict_name=["UserCount"], default=None)
    ZuoraAutoRenew: bool = field_dict(dict_name=["ZuoraAutoRenew"], default=False)
    ZuoraSubscriptionId: str = field_dict(dict_name=["ZuoraSubscriptionId"], default=None)

    group_license_assignments: List[GroupLicenseAssignment] = field(default_factory=lambda: [])

    def get_created_by_user(self) -> Optional[User]:
        return self.altium_api.get_contact_details(self.CreatedByGUID)

    def get_last_modified_by_user(self) -> Optional[User]:
        return self.altium_api.get_contact_details(self.LastModifiedByGUID)

    def get_contact_user(self) -> Optional[User]:
        return self.altium_api.get_contact_details(self.ContactGUID)

    def get_license_kind(self) -> None:
        raise NotImplementedError()

    def get_license_usage(self) -> None:
        raise NotImplementedError()

    def get_permission_set(self) -> None:
        raise NotImplementedError()

    def get_owner_account(self) -> Optional[Account]:
        return self.altium_api.get_account_details(self.OwnerAccountGUID)

    def get_geographic_scope(self) -> None:
        raise NotImplementedError()

    def get_product_line(self) -> None:
        raise NotImplementedError()

    def get_subscription(self) -> None:
        raise NotImplementedError()

    def get_design_capability(self) -> None:
        raise NotImplementedError()


@dataclass
@dataclassdict
class Group:
    altium_api: AltiumApi

    AccountGUID: str = field_dict(dict_name=["AccountGUID"], default=None)
    Active: bool = field_dict(dict_name=["Active"], default=False)
    GroupGUID: str = field_dict(dict_name=["GroupGUID"], default=None)
    GroupName: str = field_dict(dict_name=["GroupName"], default=None)
    GUID: str = field_dict(dict_name=["GUID"], default=None)
    LastModifiedDate: datetime = field_dict(dict_name=["LastModifiedDate"], default=datetime.min, dict_conv_str=('([0-9-T:]*)[.]\\d*Z', '%Y-%m-%dT%H:%M:%S'))
    OwnerContactGUID: str = field_dict(dict_name=["OwnerContactGUID"], default=None)
    OwnerGUID: str = field_dict(dict_name=["OwnerGUID"], default=None)

    group_license_assignments: List[GroupLicenseAssignment] = field(default_factory=lambda: [])


@dataclass
@dataclassdict
class GroupLicenseAssignment:
    altium_api: AltiumApi

    Active: bool = field_dict(dict_name=["Active"], default=False)
    AllowBorrow: bool = field_dict(dict_name=["AllowBorrow"], default=False)
    AutoLease: bool = field_dict(dict_name=["AutoLease"], default=False)
    Autoname: str = field_dict(dict_name=["Autoname"], default=None)
    CreatedAt: datetime = field_dict(dict_name=["CreatedAt"], default=datetime.min, dict_conv_str=('([0-9-T:]*)[.]\\d*Z', '%Y-%m-%dT%H:%M:%S'))
    CreatedByGUID: str = field_dict(dict_name=["CreatedByGUID"], default=None)
    GroupGUID: str = field_dict(dict_name=["GroupGUID"], default=None)
    GUID: str = field_dict(dict_name=["GUID"], default=None)
    LastModifiedByGUID: str = field_dict(dict_name=["LastModifiedByGUID"], default=None)
    LastModifiedDate: datetime = field_dict(dict_name=["LastModifiedDate"], default=datetime.min, dict_conv_str=('([0-9-T:]*)[.]\\d*Z', '%Y-%m-%dT%H:%M:%S'))
    LicenseGUID: str = field_dict(dict_name=["LicenseGUID"], default=None)
    LicenseSerialNo: str = field_dict(dict_name=["LicenseSerialNo"], default=None)
    MaxBorrowDuration: int = field_dict(dict_name=["MaxBorrowDuration"], default=None)
    MaxUserCount: int = field_dict(dict_name=["MaxUserCount"], default=None)
    NotificationGroupGuid: str = field_dict(dict_name=["NotificationGroupGuid"], default=None)
    OwnerGUID: str = field_dict(dict_name=["OwnerGUID"], default=None)
    PermissionSetGUID: str = field_dict(dict_name=["PermissionSetGUID"], default=None)
    SyncId: str = field_dict(dict_name=["SyncId"], default=None)

    license: Optional[License] = field(default=None)
    group: Optional[Group] = field(default=None)

    def get_created_by_user(self) -> None:
        raise NotImplementedError()

    def get_last_modified_by_user(self) -> None:
        raise NotImplementedError()


@dataclass
@dataclassdict
class User:
    altium_api: AltiumApi

    AccountGUID: str = field_dict(dict_name=["AccountGUID"], default=None)
    Active: bool = field_dict(dict_name=["Active"], default=False)
    ContactName: str = field_dict(dict_name=["ContactName"], default=None)
    CurrencyGUID: str = field_dict(dict_name=["CurrencyGUID"], default=None)
    Email: str = field_dict(dict_name=["Email"], default=None)
    EmailOptOut: bool = field_dict(dict_name=["EmailOptOut"], default=False)
    EmailSalutation: str = field_dict(dict_name=["EmailSalutation"], default=None)
    EmailSalutationCH: str = field_dict(dict_name=["EmailSalutationCH"], default=None)
    EmailSalutationEN: str = field_dict(dict_name=["EmailSalutationEN"], default=None)
    EmailSalutationFR: str = field_dict(dict_name=["EmailSalutationFR"], default=None)
    EmailSalutationGE: str = field_dict(dict_name=["EmailSalutationGE"], default=None)
    EmailSalutationJP: str = field_dict(dict_name=["EmailSalutationJP"], default=None)
    EncryptedId: str = field_dict(dict_name=["EncryptedId"], default=None)
    EvaluationMode: str = field_dict(dict_name=["EvaluationMode"], default=None)
    Fax: str = field_dict(dict_name=["Fax"], default=None)
    FirstName: str = field_dict(dict_name=["FirstName"], default=None)
    GUID: str = field_dict(dict_name=["GUID"], default=None)
    HardwareTester: bool = field_dict(dict_name=["HardwareTester"], default=False)
    LanguageGUID: str = field_dict(dict_name=["LanguageGUID"], default=None)
    LastModifiedDate: datetime = field_dict(dict_name=["LastModifiedDate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    LastName: str = field_dict(dict_name=["LastName"], default=None)
    LeadSource: str = field_dict(dict_name=["LeadSource"], default=None)
    MailingCity: str = field_dict(dict_name=["MailingCity"], default=None)
    MailingCountry: str = field_dict(dict_name=["MailingCountry"], default=None)
    MailingCounty: str = field_dict(dict_name=["MailingCounty"], default=None)
    MailingPostalCode: str = field_dict(dict_name=["MailingPostalCode"], default=None)
    MailingState: str = field_dict(dict_name=["MailingState"], default=None)
    MailingStreet: str = field_dict(dict_name=["MailingStreet"], default=None)
    MobilePhone: str = field_dict(dict_name=["MobilePhone"], default=None)
    OptInMaterial: str = field_dict(dict_name=["OptInMaterial"], default=None)
    OptInProducts: str = field_dict(dict_name=["OptInProducts"], default=None)
    OwnerGUID: str = field_dict(dict_name=["OwnerGUID"], default=None)
    Phone: str = field_dict(dict_name=["Phone"], default=None)
    ProductInterests: str = field_dict(dict_name=["ProductInterests"], default=None)
    ProfileEnabled: bool = field_dict(dict_name=["ProfileEnabled"], default=False)
    Salutation: str = field_dict(dict_name=["Salutation"], default=None)
    ShipInstallationDisks: bool = field_dict(dict_name=["ShipInstallationDisks"], default=False)
    Title: str = field_dict(dict_name=["Title"], default=None)
    UserGUID: str = field_dict(dict_name=["UserGUID"], default=None)


@dataclass
@dataclassdict
class Account:
    AccountGUID: str = field_dict(dict_name=["AccountGUID"], default=None)
    AccountName: str = field_dict(dict_name=["AccountName"], default=None)
    AccountNumber: str = field_dict(dict_name=["AccountNumber"], default=None)
    Account_Record_Type_formula: str = field_dict(dict_name=["Account_Record_Type_formula"], default=None)
    BillingCity: str = field_dict(dict_name=["BillingCity"], default=None)
    BillingCountry: str = field_dict(dict_name=["BillingCountry"], default=None)
    BillingCounty: str = field_dict(dict_name=["BillingCounty"], default=None)
    BillingPostalCode: str = field_dict(dict_name=["BillingPostalCode"], default=None)
    BillingState: str = field_dict(dict_name=["BillingState"], default=None)
    BillingStreet: str = field_dict(dict_name=["BillingStreet"], default=None)
    Currency: str = field_dict(dict_name=["Currency"], default=None)
    CustomerNumber: str = field_dict(dict_name=["CustomerNumber"], default=None)
    Fax: str = field_dict(dict_name=["Fax"], default=None)
    GUID: str = field_dict(dict_name=["GUID"], default=None)
    IsActive: bool = field_dict(dict_name=["IsActive"], default=False)
    IsDeleted: bool = field_dict(dict_name=["IsDeleted"], default=False)
    IsEducational: bool = field_dict(dict_name=["IsEducational"], default=False)
    LastModifiedDate: datetime = field_dict(dict_name=["LastModifiedDate"], default=datetime.min, dict_conv_str=('([0-9-T:]*)[.]\\d*Z', '%Y-%m-%dT%H:%M:%S'))
    OwnerGUID: str = field_dict(dict_name=["OwnerGUID"], default=None)
    ParentGUID: str = field_dict(dict_name=["ParentGUID"], default=None)
    Phone: str = field_dict(dict_name=["Phone"], default=None)
    ShipInstallationDisks: bool = field_dict(dict_name=["ShipInstallationDisks"], default=False)
    ShippingCity: str = field_dict(dict_name=["ShippingCity"], default=None)
    ShippingCountry: str = field_dict(dict_name=["ShippingCountry"], default=None)
    ShippingCounty: str = field_dict(dict_name=["ShippingCounty"], default=None)
    ShippingPostalCode: str = field_dict(dict_name=["ShippingPostalCode"], default=None)
    ShippingState: str = field_dict(dict_name=["ShippingState"], default=None)
    ShippingStreet: str = field_dict(dict_name=["ShippingStreet"], default=None)
    Site: str = field_dict(dict_name=["Site"], default=None)
    Website: str = field_dict(dict_name=["Website"], default=None)
