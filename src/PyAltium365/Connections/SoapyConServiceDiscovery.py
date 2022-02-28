from typing import TYPE_CHECKING, Tuple, List, Dict
from PyAltium365.Connections.ConnectionExceptions import InternalConnectionException
from PyAltium365.Connections.SoapyCon import SoapyCon
from PyAltium365.Data.DataConServiceDiscovery import DiscoveryLoginOption, UserInfo, ServiceEndpoints, DiscoveryConfig
from PyAltium365.Exceptions import DataException, ConnectionException
from PyAltium365.Helpers.DictListHelper import get_from_dict_and_check_type_r
from requests import Session

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class SoapyConServiceDiscovery(SoapyCon):
    def __init__(self, session: Session, url: str, altium_api: AltiumApi):
        super().__init__(session, url + "/servicediscovery/servicediscovery.asmx")
        self._altium_api = altium_api

    def login(self, user_name: str, password: str, secure_login: bool = False, option: DiscoveryLoginOption = DiscoveryLoginOption.NONE,
              product_name: str = "Altium Designer") -> Tuple[UserInfo, ServiceEndpoints, List[DiscoveryConfig]]:
        try:
            head = None
            body = self._gen_generic_tag("userName", user_name)
            body += self._gen_generic_tag("password", password)
            body += self._gen_generic_tag("secureLogin", str(secure_login).lower())
            body += self._gen_generic_tag("discoveryLoginOptions", option.value)
            body += self._gen_generic_tag("productName", product_name)

            resp = self._send_command("http://altium.com/Login", head, body, "Login", "http://altium.com/")

            dic = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'LoginResponse', 'LoginResult'], True), True)
            user_info: Dict = get_from_dict_and_check_type_r(dic, "UserInfo", dict, {})
            end_points: Dict = get_from_dict_and_check_type_r(dic, "Endpoints", dict, {})
            configs: Dict = get_from_dict_and_check_type_r(dic, "Configurations", dict, {'UserWorkspaceInfo': {}})
            configs_result = []
            for c in configs['UserWorkspaceInfo'] if type(configs['UserWorkspaceInfo']) is list else [configs['UserWorkspaceInfo']]:
                configs_result.append(DiscoveryConfig(self._altium_api).from_dict(c))  # type: ignore

            return UserInfo(self._altium_api).from_dict(user_info), ServiceEndpoints(self._altium_api).from_dict(end_points), configs_result  # type: ignore
        except (InternalConnectionException, DataException):
            raise ConnectionException()
