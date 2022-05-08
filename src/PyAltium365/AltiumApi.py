import os
from typing import Dict, Any, Union, Optional, List
from urllib.parse import urlparse

import requests
from PyAltium365.Connections.JsonConSearchAsync import JsonConSearchAsync
from PyAltium365.Connections.SoapyConPortal import SoapyConPortal
from PyAltium365.Connections.SoapyConServiceDiscovery import SoapyConServiceDiscovery
from PyAltium365.Connections.SoapyConVault import SoapyConVault
from PyAltium365.Connections.SoapyConWorkspace import SoapyConWorkspace
from PyAltium365.Data.DataConPortal import User, PrtGlobalServiceName, PrtSettings, Account
from PyAltium365.Data.DataConSearchAsync import AsyncSearchObject
from PyAltium365.Data.DataConServiceDiscovery import ServiceEndpoints
from PyAltium365.Data.DataConVault import AluItem, AluLifeCycleDefinition, AluItemRevision, AluLifeCycleState, AluLifeCycleStateChange, \
    AluLifeCycleStateTransition, AluItemRevisionLink
from PyAltium365.Data.DataConWorkspace import UserWorkspace
from PyAltium365.Helpers.DataConvHelper import convert_data_to_type
from PyAltium365.Helpers.GeneralHelper import ReturnOnException


class AltiumApi:
    def __init__(self) -> None:
        self._connected = False

        # Global part
        self._session = requests.Session()
        self._portal_con: SoapyConPortal = SoapyConPortal(self._session, self)
        self._workspace_con: Optional[SoapyConWorkspace] = None
        self._session_guid: Union[str, None] = None
        self._prt_service_urls: Dict[PrtGlobalServiceName, str] = {}
        self._prt_settings: Dict[PrtSettings, Any] = {}

        # workspace based data
        self._service_discovery_con: Optional[SoapyConServiceDiscovery] = None
        self._service_endpoints: Optional[ServiceEndpoints] = None
        self._seswork_guid: Optional[str] = None
        self._service_vault: Optional[SoapyConVault] = None
        self._service_search_async: Optional[JsonConSearchAsync] = None

    def login(self, user_name: str, password: str) -> bool:
        u = self._portal_con.login_user(user_name, password)
        if u is not None:
            self._session_guid = u.SessionHandle
            workspace_url = self.get_prt_service_url(PrtGlobalServiceName.WORKSPACE, True)
            if type(workspace_url) is str:
                self._workspace_con = SoapyConWorkspace(self._session, workspace_url, self)
                return True
            self._session_guid = None
        return False

    def workspace_login(self, workspace: Union[UserWorkspace, str], user_name: str, password: str) -> bool:
        if self._session_guid is None:
            if not self.login(user_name, password):
                return False
        if type(workspace) is UserWorkspace:
            workspace = workspace.HostingUrl
        if type(workspace) is not str:
            return False
        self._service_discovery_con = SoapyConServiceDiscovery(self._session, workspace, self)
        user_info, service_endp, discovery_config = self._service_discovery_con.login(user_name, password)
        self._service_endpoints = service_endp
        self._seswork_guid = user_info.SessionId
        self._service_vault = SoapyConVault(self._session, workspace, self)
        self._service_search_async = JsonConSearchAsync(self._session, self._service_endpoints.SEARCHBASE, self)
        return True

    @ReturnOnException()
    def get_contact_details(self, guid: str) -> Optional[User]:
        if self._session_guid is None:
            return None
        return self._portal_con.get_prt_contact_details(self._session_guid, guid)

    @ReturnOnException()
    def get_account_details(self, guid: str) -> Optional[Account]:
        if self._session_guid is None:
            return None
        return self._portal_con.get_account_details(self._session_guid, guid)

    def get_prt_service_url(self, name: PrtGlobalServiceName, force_request: bool = False) -> Optional[str]:
        if name in self._prt_service_urls and not force_request:
            return self._prt_service_urls[name]
        url = self._portal_con.get_prt_global_service_url(name.value[0], name.value[1], self._session_guid if name.value[2] else None)
        if url is not None:
            self._prt_service_urls[name] = url
        return url

    def get_prt_setting(self, name: PrtSettings, force_request: bool = False) -> Any:
        if name in self._prt_settings and not force_request:
            return convert_data_to_type(self._prt_settings[name], name.value[2])
        setting = self._portal_con.get_prt_settings([name.value[0]], self._session_guid if name.value[1] else None)[0]
        self._prt_settings[name] = setting
        return convert_data_to_type(setting, name.value[2])

    def check_adw_account_license(self) -> bool:
        if self._workspace_con is None or self._session_guid is None:
            return False
        return self._workspace_con.check_adw_account_license(self._session_guid)

    def get_user_workspaces(self) -> Optional[List[UserWorkspace]]:
        if self._workspace_con is None or self._session_guid is None:
            return None
        return self._workspace_con.get_user_workspaces(self._session_guid)

    @ReturnOnException()
    def create_search_object(self) -> Optional[AsyncSearchObject]:
        return AsyncSearchObject(self._service_search_async, self)

    @ReturnOnException()
    def get_item_from_guid(self, guid: str) -> Optional[AluItem]:
        if self._service_vault is None or self._seswork_guid is None:
            return None
        return self._service_vault.get_alu_items(self._seswork_guid, f"GUID = '{guid}'")[0]

    @ReturnOnException()
    def get_life_cycle_definition_from_guid(self, guid: str) -> Optional[AluLifeCycleDefinition]:
        if self._service_vault is None or self._seswork_guid is None:
            return None
        return self._service_vault.get_alu_life_cycle_definitions(self._seswork_guid, f"GUID = '{guid}'")[0]

    @ReturnOnException()
    def get_item_revision_from_guid(self, guid: str) -> Optional[AluItemRevision]:
        if self._service_vault is None or self._seswork_guid is None:
            return None
        return self._service_vault.get_alu_item_revision(self._seswork_guid, f"GUID = '{guid}'")[0]

    def get_item_revisions_from_item(self, item: AluItem) -> List[AluItemRevision]:
        if self._service_vault is None or self._seswork_guid is None:
            return []
        return self._service_vault.get_alu_item_revision(self._seswork_guid, f"ItemGUID = '{item.GUID}'")

    @ReturnOnException()
    def get_latest_item_revisions_from_item(self, item: AluItem) -> Optional[AluItemRevision]:
        revs = self.get_item_revisions_from_item(item)
        max_rev = revs[0]
        for rev in revs:
            if rev.RevisionId > max_rev.RevisionId:
                max_rev = rev
        return max_rev

    @ReturnOnException()
    def get_life_cycle_state_from_guid(self, guid: str) -> Optional[AluLifeCycleState]:
        if self._service_vault is None or self._seswork_guid is None:
            return None
        return self._service_vault.get_alu_life_cycle_state(self._seswork_guid, f"GUID = '{guid}'")[0]

    def get_life_cycle_state_changes_from_item_revision(self, item_revision: AluItemRevision) -> List[AluLifeCycleStateChange]:
        if self._service_vault is None or self._seswork_guid is None:
            return []
        return self._service_vault.get_alu_life_cycle_state_changes(self._seswork_guid, f"ItemRevisionGUID = '{item_revision.GUID}'")

    @ReturnOnException()
    def get_life_cycle_state_transition_guid(self, guid: str) -> Optional[AluLifeCycleStateTransition]:
        if self._service_vault is None or self._seswork_guid is None:
            return None
        return self._service_vault.get_alu_life_cycle_state_transitions(self._seswork_guid, f"GUID = '{guid}'")[0]

    @ReturnOnException([])
    def get_possible_life_cycle_state_transitions_from_item_revision(self, item_revision: AluItemRevision) -> List[AluLifeCycleStateTransition]:
        if self._service_vault is None or self._seswork_guid is None:
            return []
        return self._service_vault.get_alu_life_cycle_state_transitions(self._seswork_guid, f"LifeCycleStateBeforeGUID = '{item_revision.LifeCycleStateGUID}'")

    @ReturnOnException([])
    def get_item_revision_link_from_item_revision(self, item_revision: AluItemRevision, child: bool = True) -> List[AluItemRevisionLink]:
        if self._service_vault is None or self._seswork_guid is None:
            return []
        filter = "ParentItemRevisionGUID" if child else "ChildItemRevisionGUID"
        return self._service_vault.get_alu_item_revision_links(self._seswork_guid, f"{filter}='{item_revision.GUID}'")

    @ReturnOnException([])
    def get_child_item_revisions_from_item_revision(self, item_revision: AluItemRevision) -> List[AluItemRevision]:
        lin = self.get_item_revision_link_from_item_revision(item_revision, True)
        lout = []
        for li in lin:
            lou = self.get_item_revision_from_guid(li.ChildItemRevisionGUID)
            if lou is not None:
                lout.append(lou)
        return lout

    @ReturnOnException([])
    def get_parent_item_revisions_from_item_revision(self, item_revision: AluItemRevision) -> List[AluItemRevision]:
        lin = self.get_item_revision_link_from_item_revision(item_revision, False)
        lout = []
        for li in lin:
            lou = self.get_item_revision_from_guid(li.ChildItemRevisionGUID)
            if lou is not None:
                lout.append(lou)
        return lout

    @ReturnOnException(False)
    def change_life_cycle_state(self, item_revision: List[AluItemRevision], life_cycle_transition: List[AluLifeCycleStateTransition]) -> bool:
        if len(item_revision) != len(life_cycle_transition):
            return False
        irg = []
        lcst = []
        lcsag = []
        for ind in range(len(item_revision)):
            irg.append(item_revision[ind].GUID)
            lcst.append(life_cycle_transition[ind].GUID)
            lcsag.append(life_cycle_transition[ind].LifeCycleStateAfterGUID)
        return self._service_vault.add_alu_life_cycle_state_changes(self._seswork_guid, irg, lcst, lcsag)

    @ReturnOnException(None)
    def download_item_revision(self, item_revision: AluItemRevision, path: str, rename: Optional[str] = None) -> Optional[str]:
        if self._service_vault is None or self._seswork_guid is None:
            return None
        url = self._service_vault.get_alu_item_revision_download_urls(self._seswork_guid, [item_revision.GUID])[0]

        if rename is None:
            rename = os.path.basename(urlparse(url).path)
        if not rename.endswith(".zip"):
            rename = rename + ".zip"
        full_path = os.path.join(path, rename)
        if not os.path.exists(path):
            os.makedirs(path)
        r = self._session.get(url, stream=True)
        with open(full_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        return full_path
