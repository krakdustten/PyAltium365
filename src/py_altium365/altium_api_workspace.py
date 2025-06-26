from py_altium365.connection.json_con_search_async import JsonConSearchAsync
from py_altium365.connection.soapy_con_service_discovery import SoapyConServiceDiscovery
from py_altium365.connection.vault.soapy_con_vault import SoapConVault
from py_altium365.connection.vault.soapy_con_vault_base import SoapMethodOption


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
        self.workspace_url: str = workspace_url
        self._service_discovery: SoapyConServiceDiscovery = service_discovery
        self.session_guid: str = service_discovery.user_info.session_id
        if self._service_discovery.service_urls.SEARCHBASE is None:
            raise ConnectionError("Failed to get search base URL")
        self._vault = SoapConVault(self)

    def create_search_object(self) -> JsonConSearchAsync:
        """
        Create a search object
        :return:
        """
        if self._service_discovery.service_urls.SEARCHBASE is None:
            raise ConnectionError("Failed to get search base URL")
        return JsonConSearchAsync(self, self._service_discovery.service_urls.SEARCHBASE, self.session_guid, self.workspace_url.strip(":443").strip("https://"))

    def get_item_from_guid(self, guid: str):
        self._vault.get_alu_items(options=[SoapMethodOption.INCLUDE_ALL_CHILD_OBJECTS])
        return self.workspace_url



