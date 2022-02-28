from typing import Union, List, Tuple, TYPE_CHECKING

from PyAltium365.Connections.ConnectionExceptions import InternalConnectionException
from PyAltium365.Connections.SoapyCon import SoapyCon
from PyAltium365.Data.DataConPortal import UserLogin, License, Group, User, Account, GroupLicenseAssignment
from PyAltium365.Exceptions import ConnectionException, DataException
from PyAltium365.Helpers.DictListHelper import get_from_dict_and_check_type, check_data_in_dict, get_from_dict_and_check_type2
from requests import Session

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class SoapyConPortal(SoapyCon):
    def __init__(self, session: Session, altium_api: AltiumApi):
        super().__init__(session, "https://portal365.altium.com/?cls=soap")
        self._altium_api = altium_api

    def get_prt_global_service_url(self, service_name: str, set_name: str, handle: str = None) -> Union[str, None]:
        try:
            head = self._gen_header_basic()
            body = self._gen_generic_tag("Handle", handle)
            body += self._gen_generic_tag("ServiceName", service_name)
            body += self._gen_generic_tag("SetName", set_name)

            resp = self._send_command("GetPRT_GlobalServiceUrl", head, body)
            dic = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetPRT_GlobalServiceUrlResponse'], True), True)
            if isinstance(dic["ServiceURL"], str):
                return dic["ServiceURL"]
        except InternalConnectionException:
            pass
        return None

    def get_prt_settings(self, settings: List[str], handle: str = None) -> List[str]:
        try:
            head = self._gen_header_basic()
            body = self._gen_generic_tag("Handle", handle)
            body += self._gen_generic_tag_start("SettingNames")
            for setting in settings:
                body += self._gen_generic_tag("string", setting, "http://schemas.microsoft.com/2003/10/Serialization/Arrays")
            body += self._gen_generic_tag_end()

            resp = self._send_command("GetPRT_Settings", head, body, "GetPRT_SettingsRequest")
            dic = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetPRT_SettingsResponse', 'Settings'], True), True)
            if type(dic["KeyValueItem"]) is dict:
                return [dic["KeyValueItem"]["Value"]]
            if type(dic["KeyValueItem"]) is list:
                return [str(x["Value"]) for x in dic["KeyValueItem"]]
            raise DataException()
        except InternalConnectionException:
            raise ConnectionException()

    def login_user(self, username: str, password: str) -> UserLogin:
        try:
            head = self._gen_header_basic()
            body = self._gen_generic_tag("Username", username)
            body += self._gen_generic_tag("Password", password)

            resp = self._send_command("Login", head, body)
            dic = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'LoginResponse', 'LoginResult'], True), True)
            return (UserLogin(self._altium_api)).from_dict(dic)  # type: ignore
        except InternalConnectionException:
            raise ConnectionException()

    def get_lic_available_licences_for_contact(self, handle: str, product_line_guid: str = None) \
            -> Tuple[List[License], List[GroupLicenseAssignment], List[Group]]:
        try:
            head = self._gen_header_basic()
            body = self._gen_generic_tag("Handle", handle)
            if product_line_guid is not None:
                body += self._gen_generic_tag("ProductLineGUID", product_line_guid)

            resp = self._send_command("GetLIC_AvailableLicenses_ForContactAD16Plus", head, body,
                                      "GetLIC_AvailableLicenses_ForContact")
            dic = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetLIC_AvailableLicenses_ForContactResponse', 'LicenseAssignmentDetails'],
                                                                 True), True)
            licenses: List[License] = []
            group_license_assignments: List[GroupLicenseAssignment] = []
            groups: List[Group] = []
            dict_licenses = get_from_dict_and_check_type(dic, "Licenses", dict)
            list_licenses = get_from_dict_and_check_type2(dict_licenses, "item", list, dict)
            for list_license in list_licenses if type(list_licenses) is list else [list_licenses]:
                licenses.append(License(self._altium_api).from_dict(list_license))  # type: ignore
            dict_group_license_assignments = get_from_dict_and_check_type(dic, "GroupLicenseAssignments", dict)
            list_group_license_assignments = get_from_dict_and_check_type2(dict_group_license_assignments, "item", list, dict)
            for list_group_license_assignment in list_group_license_assignments \
                    if type(list_group_license_assignments) is list else [list_group_license_assignments]:
                group_license_assignments.append(GroupLicenseAssignment(self._altium_api).from_dict(list_group_license_assignment))  # type: ignore
            dict_groups = get_from_dict_and_check_type(dic, "Groups", dict)
            list_groups = get_from_dict_and_check_type2(dict_groups, "item", list, dict)
            for list_group in list_groups if type(list_groups) is list else [list_groups]:
                groups.append(Group(self._altium_api).from_dict(list_group))  # type: ignore

            for group_license_assignment in group_license_assignments:
                for group in groups:
                    if group_license_assignment.GroupGUID == group.GUID:
                        group_license_assignment.group = group
                        group.group_license_assignments.append(group_license_assignment)
                for license in licenses:
                    if group_license_assignment.LicenseGUID == license.GUID:
                        group_license_assignment.license = license
                        license.group_license_assignments.append(group_license_assignment)
            return licenses, group_license_assignments, groups
        except InternalConnectionException:
            raise ConnectionException()

    def get_prt_contact_details(self, handle: str, user_guid: str) -> User:
        try:
            head = self._gen_header_basic()
            body = self._gen_generic_tag("Handle", handle)
            body += self._gen_generic_tag("Filter", f"ID = '{user_guid}'")

            resp = self._send_command("GetPRT_ContactDetails", head, body)
            dic = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetPRT_ContactDetailsResponse', 'ContactDetails'], True), True)
            check_data_in_dict(dic, "Success", bool, True)
            dict_contacts = get_from_dict_and_check_type(dic, "Contacts", dict)
            contact = get_from_dict_and_check_type(dict_contacts, "item", dict)

            return (User(self._altium_api)).from_dict(contact)  # type: ignore
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_account_details(self, handle: str, account_guid: str) -> Account:
        try:
            head = self._gen_header_basic()
            body = self._gen_generic_tag("Handle", handle)
            body += self._gen_generic_tag("Filter", f"ID = '{account_guid}'")

            resp = self._send_command("GetAccountDetails", head, body)
            dic = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetAccountDetailsResponse', 'AccountDetails'], True), True)
            check_data_in_dict(dic, "Success", bool, True)
            dict_accounts = get_from_dict_and_check_type(dic, "Accounts", dict)
            contact = get_from_dict_and_check_type(dict_accounts, "item", dict)

            return (Account(self._altium_api)).from_dict(contact)  # type: ignore
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def _gen_header_basic(self, api_version: str = '2.0') -> str:
        return self._gen_generic_tag("APIVersion", api_version, "http://tempuri.org/")
