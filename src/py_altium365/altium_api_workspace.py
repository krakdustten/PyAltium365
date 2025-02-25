from py_altium365.connection.json_con_search_async import JsonConSearchAsync
from py_altium365.connection.soapy_con_service_discovery import SoapyConServiceDiscovery


class AltiumApiWorkspace:
    """Altium API workspace class"""

    def __init__(self, workspace_url: str, service_discovery: SoapyConServiceDiscovery):
        """
        Initialize the Altium API workspace object
        :param workspace_url: The URL of the workspace
        :param service_discovery: The service discovery object
        """

        if service_discovery.user_info is None:
            raise ConnectionError("Failed to get user info")
        self._workspace_url: str = workspace_url
        self._service_discovery: SoapyConServiceDiscovery = service_discovery
        self._session_guid: str = service_discovery.user_info.session_id
        if self._service_discovery.service_urls.SEARCHBASE is None:
            raise ConnectionError("Failed to get search base URL")
        self._service_search_async = JsonConSearchAsync(
            self._service_discovery.service_urls.SEARCHBASE, self._session_guid, workspace_url.strip(":443").strip("https://")
        )

    def create_search_object(self):
        """
        Create a search object
        :return:
        """
        return self._service_search_async.get_search_interface()
