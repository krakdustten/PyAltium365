from typing import Optional

from py_altium365.connection.json_con_search_async import JsonConSearchAsync
from py_altium365.connection.soapy_con_service_discovery import SoapyConServiceDiscovery
from py_altium365.connection.vault.soapy_con_vault import SoapConVault
from py_altium365.connection.vault.soapy_con_vault_base import AluItem, SoapMethodOption, AluFolder


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

    def get_item_from_guid(self, guid: str) -> Optional[AluItem]:
        """
        Get an item from the vault using its GUID
        :param guid: The GUID of the item to retrieve
        :return: A list of AluItem objects matching the GUID
        """
        items = self._vault.get_alu_items(options=[SoapMethodOption.INCLUDE_ALL_CHILD_OBJECTS], p_filter="GUID='" + guid + "'")
        return items[0] if len(items) > 0 else None

    def get_items_in_folder(self, folder: AluFolder) -> list[AluItem]:
        """
        Get all items in a specific folder
        :param folder: An AluFolder object representing the folder to retrieve items from
        :return: A list of AluItem objects in the specified folder
        """
        return self._vault.get_alu_items(options=[SoapMethodOption.INCLUDE_ALL_CHILD_OBJECTS], p_filter="FolderGUID='" + folder.guid + "'")

    def get_all_folders(self) -> list[AluFolder]:
        """
        Get all folders in the vault
        :return: A list of AluFolder objects representing the folders
        """
        return self._vault.get_alu_folders(options=[SoapMethodOption.INCLUDE_ALL_CHILD_OBJECTS])

    def get_folder_from_guid(self, guid: str) -> Optional[AluFolder]:
        """
        Get a folder from the vault using its GUID
        :param guid: The GUID of the folder to retrieve
        :return: An AluFolder object matching the GUID, or None if not found
        """
        folders = self._vault.get_alu_folders(options=[SoapMethodOption.INCLUDE_ALL_CHILD_OBJECTS], p_filter="GUID='" + guid + "'")
        return folders[0] if len(folders) > 0 else None

    def get_folders_in_folder(self, folder: AluFolder) -> list[AluFolder]:
        """
        Get all folders in a specific folder
        :param folder: An AluFolder object representing the folder to retrieve subfolders from
        :return: A list of AluFolder objects in the specified folder
        """
        return self._vault.get_alu_folders(options=[SoapMethodOption.INCLUDE_ALL_CHILD_OBJECTS], p_filter="ParentFolderGUID='" + folder.guid + "'")
