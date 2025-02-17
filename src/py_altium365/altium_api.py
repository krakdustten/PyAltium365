from typing import Optional, Union

from py_altium365.base.enums import PrtGlobalService
from py_altium365.connection.soapy_con_portal import SoapyConPortal


class AltiumApi:
    """
    Altium API class
    """

    def __init__(self):
        """
        Initialize the Altium API object
        """
        self._portal_con: SoapyConPortal = SoapyConPortal(self)
        self._session_guid: Optional[str] = None
        self._service_urls: dict[PrtGlobalService, str] = {}

    def login(self, username: str, password: str, return_message: bool = False) -> Union[str, bool]:
        """
        Login to the Altium API
        :param username: The altium username
        :param password: The altium password
        :param return_message: If the login fails, return the message
        :return: True if the login was successful, False otherwise or the message if return_message is True
        """
        user_login = self._portal_con.login_user(username, password)
        if not user_login.success:
            if return_message and user_login.message is not None:
                return user_login.message
            return False
        self._session_guid = user_login.session_handle

        for service in PrtGlobalService:
            self._portal_con.get_prt_global_service_url(service, self._session_guid)
        return True

    def get_service_url(self, service: PrtGlobalService, force_request: bool = False) -> Optional[str]:
        """
        Get a service URL
        :param service: The service to get the URL for
        :param force_request: If the URL should be requested again from altium or use the cached URL
        :return: The service URL
        """
        if service in self._service_urls and not force_request:
            return self._service_urls[service]
        url = self._portal_con.get_prt_global_service_url(service, self._session_guid)
        if url is not None:
            self._service_urls[service] = url
        return url
