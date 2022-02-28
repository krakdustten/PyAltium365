from typing import TYPE_CHECKING, List
from PyAltium365.Connections.ConnectionExceptions import InternalConnectionException
from PyAltium365.Connections.SoapyCon import SoapyCon
from PyAltium365.Data.DataConWorkspace import UserWorkspace
from PyAltium365.Exceptions import DataException, ConnectionException
from PyAltium365.Helpers.DataConvHelper import convert_data_to_type
from PyAltium365.Helpers.DictListHelper import get_from_dict_and_check_type
from requests import Session

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class SoapyConWorkspace(SoapyCon):
    def __init__(self, session: Session, url: str, altium_api: AltiumApi):
        super().__init__(session, url)
        self._altium_api = altium_api

    def check_adw_account_license(self, session_guid: str) -> bool:
        try:
            head = self._gen_generic_tag_start("UserCredentials", "http://tempuri.org/")
            head += self._gen_generic_tag("password", session_guid, "http://tempuri.org/")
            head += self._gen_generic_tag_end()
            body = ""

            resp = self._send_command("http://tempuri.org/CheckADWAccountLicense", head, body, "CheckADWAccountLicense")
            dic = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'CheckADWAccountLicenseResponse'], True), True)
            result = get_from_dict_and_check_type(dic, "CheckADWAccountLicenseResult", str)
            b = convert_data_to_type(result, bool)
            return b if type(b) is bool else False
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_user_workspaces(self, session_guid: str) -> List[UserWorkspace]:
        try:
            head = self._gen_generic_tag_start("UserCredentials", "http://tempuri.org/")
            head += self._gen_generic_tag("password", session_guid, "http://tempuri.org/")
            head += self._gen_generic_tag_end()
            body = ""

            resp = self._send_command("http://tempuri.org/GetUserWorkspaces", head, body, "GetUserWorkspaces")
            diclist = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetUserWorkspacesResponse', 'GetUserWorkspacesResult'], True), True)
            result = []
            for d in diclist['UserWorkspaceInfo'] if type(diclist['UserWorkspaceInfo']) is list else [diclist['UserWorkspaceInfo']]:
                result.append(UserWorkspace(self._altium_api).from_dict(d))  # type: ignore
            return result
        except (InternalConnectionException, DataException):
            raise ConnectionException()
