from typing import TYPE_CHECKING, Optional, List
from PyAltium365.Connections.ConnectionExceptions import InternalConnectionException
from PyAltium365.Connections.SoapyCon import SoapyCon
from PyAltium365.Data.DataConVault import AluVault, AluItem, AluTag, AluLifeCycleState, AluItemRevision, AluLifeCycleDefinition, AluLifeCycleStateChange, \
    AluLifeCycleStateTransition, AluItemRevisionLink
from PyAltium365.Exceptions import DataException, ConnectionException
from requests import Session

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class SoapyConVault(SoapyCon):
    def __init__(self, session: Session, url: str, altium_api: AltiumApi):
        super().__init__(session, url + "/vault/?cls=soap")
        self._altium_api = altium_api

    def get_alu_vault_record(self, seswork_guid: str) -> AluVault:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)

            resp = self._send_command("GetALU_VaultRecord", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_VaultRecordResponse', 'MethodResult'])
            vault = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_VaultRecordResponse', 'Vault'], True), True)

            return AluVault(self._altium_api).from_dict(vault)  # type: ignore
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_alu_items(self, seswork_guid: str, filter: Optional[str] = None, exclude_acl_entries: bool = False) -> List[AluItem]:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)
            if exclude_acl_entries:
                body += self._gen_generic_tag_start("Options")
                body += self._gen_generic_tag("item", f"ExcludeACLEntries={str(exclude_acl_entries).lower()}")
                body += self._gen_generic_tag_end()
            if filter is not None:
                body += self._gen_generic_tag("Filter", filter)

            resp = self._send_command("GetALU_Items", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_ItemsResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_ItemsResponse', 'Records'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                li.append(AluItem(self._altium_api).from_dict(item))  # type: ignore
            return li
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_alu_tags(self, seswork_guid: str, filter: Optional[str] = None) -> List[AluTag]:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)
            if filter is not None:
                body += self._gen_generic_tag("Filter", filter)

            resp = self._send_command("GetALU_Tags", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_TagsResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_TagsResponse', 'Records'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                li.append(AluTag(self._altium_api).from_dict(item))  # type: ignore
            return li
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_alu_life_cycle_state(self, seswork_guid: str, filter: Optional[str] = None) -> List[AluLifeCycleState]:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)
            if filter is not None:
                body += self._gen_generic_tag("Filter", filter)

            resp = self._send_command("GetALU_LifeCycleStates", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_LifeCycleStatesResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_LifeCycleStatesResponse', 'Records'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                li.append(AluLifeCycleState(self._altium_api).from_dict(item))  # type: ignore
            return li
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_alu_item_revision(self, seswork_guid: str, filter: Optional[str] = None, exclude_acl_entries: bool = False) -> List[AluItemRevision]:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)
            if exclude_acl_entries:
                body += self._gen_generic_tag_start("Options")
                body += self._gen_generic_tag("item", f"ExcludeACLEntries={str(exclude_acl_entries).lower()}")
                body += self._gen_generic_tag_end()
            if filter is not None:
                body += self._gen_generic_tag("Filter", filter)

            resp = self._send_command("GetALU_ItemRevisions", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_ItemRevisionsResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_ItemRevisionsResponse', 'Records'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                li.append(AluItemRevision(self._altium_api).from_dict(item))  # type: ignore
            return li
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_alu_life_cycle_definitions(self, seswork_guid: str, filter: Optional[str] = None,
                                       exclude_acl_entries: bool = False) -> List[AluLifeCycleDefinition]:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)
            if exclude_acl_entries:
                body += self._gen_generic_tag_start("Options")
                body += self._gen_generic_tag("item", f"ExcludeACLEntries={str(exclude_acl_entries).lower()}")
                body += self._gen_generic_tag_end()
            if filter is not None:
                body += self._gen_generic_tag("Filter", filter)

            resp = self._send_command("GetALU_LifeCycleDefinitions", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_LifeCycleDefinitionsResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_LifeCycleDefinitionsResponse', 'Records'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                li.append(AluLifeCycleDefinitions(self._altium_api).from_dict(item))  # type: ignore
            return li
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_alu_life_cycle_state_changes(self, seswork_guid: str, filter: Optional[str] = None,
                                         exclude_acl_entries: bool = False) -> List[AluLifeCycleStateChange]:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)
            if exclude_acl_entries:
                body += self._gen_generic_tag_start("Options")
                body += self._gen_generic_tag("item", f"ExcludeACLEntries={str(exclude_acl_entries).lower()}")
                body += self._gen_generic_tag_end()
            if filter is not None:
                body += self._gen_generic_tag("Filter", filter)

            resp = self._send_command("GetALU_LifeCycleStateChanges", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_LifeCycleStateChangesResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_LifeCycleStateChangesResponse', 'Records'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                li.append(AluLifeCycleStateChange(self._altium_api).from_dict(item))  # type: ignore
            return li
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def get_alu_life_cycle_state_transitions(self, seswork_guid: str, filter: Optional[str] = None,
                                             exclude_acl_entries: bool = False) -> List[AluLifeCycleStateTransition]:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)
            if exclude_acl_entries:
                body += self._gen_generic_tag_start("Options")
                body += self._gen_generic_tag("item", f"ExcludeACLEntries={str(exclude_acl_entries).lower()}")
                body += self._gen_generic_tag_end()
            if filter is not None:
                body += self._gen_generic_tag("Filter", filter)

            resp = self._send_command("GetALU_LifeCycleStateTransitions", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_LifeCycleStateTransitionsResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_LifeCycleStateTransitionsResponse', 'Records'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                li.append(AluLifeCycleStateTransition(self._altium_api).from_dict(item))  # type: ignore
            return li
        except (InternalConnectionException, DataException):
            raise ConnectionException()

    def add_alu_life_cycle_state_changes(self, seswork_guid: str, item_revision_guid: List[str], life_cycle_state_transition_guid: List[str],
                                         life_cycle_state_after_guid: List[str]) -> bool:
        try:
            if not (len(item_revision_guid) == len(life_cycle_state_transition_guid) == len(life_cycle_state_after_guid)):
                return False
            head = None
            body = self._gen_generic_tag_start("Records")
            for ind in range(len(item_revision_guid)):
                body += self._gen_generic_tag_start("item")
                body += self._gen_generic_tag("GUID")
                body += self._gen_generic_tag("HRID")
                body += self._gen_generic_tag("CreatedByGUID")
                body += self._gen_generic_tag("LastModifiedByGUID")
                body += self._gen_generic_tag("CreatedByName")
                body += self._gen_generic_tag("LastModifiedByName")
                body += self._gen_generic_tag("ItemRevisionGUID", item_revision_guid[ind])
                body += self._gen_generic_tag("LifeCycleStateTransitionGUID", life_cycle_state_transition_guid[ind])
                body += self._gen_generic_tag("LifeCycleStateAfterGUID", life_cycle_state_after_guid[ind])
                body += self._gen_generic_tag("Note")
                body += self._gen_generic_tag_end()
            body += self._gen_generic_tag_end()
            body += self._gen_generic_tag("SessionHandle", seswork_guid)

            resp = self._send_command("AddALU_LifeCycleStateChanges", head, body)
            self._check_method_result(resp, ['Body', 'AddALU_LifeCycleStateChangesResponse', 'MethodResult'])
            return True
        except (InternalConnectionException, DataException):
            return False

    def get_alu_item_revision_download_urls(self, seswork_guid: str, item_revision_guid: List[str]) -> List[str]:
        try:
            head = None
            body = self._gen_generic_tag_start("ItemRevisionGUIDList")
            for item_rev in item_revision_guid:
                body += self._gen_generic_tag("item", item_rev)
            body += self._gen_generic_tag_end()
            body += self._gen_generic_tag("SessionHandle", seswork_guid)
            body += self._gen_generic_tag_start("Options")
            body += self._gen_generic_tag("item", "GetDirectLinks=true")
            body += self._gen_generic_tag_end()

            resp = self._send_command("GetALU_ItemRevisionDownloadURLs", head, body)
            self._check_method_result(resp, ['Body', 'GetALU_ItemRevisionDownloadURLsResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_ItemRevisionDownloadURLsResponse', 'MethodResult', 'Results'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                if 'URL' in item:
                    li.append(item['URL'])
            return li
        except (InternalConnectionException, DataException):
            return []

    def get_alu_item_revision_links(self, seswork_guid: str, filter: Optional[str] = None) -> List[AluItemRevisionLink]:
        try:
            head = None
            body = self._gen_generic_tag("SessionHandle", seswork_guid)
            if filter is not None:
                body += self._gen_generic_tag("Filter", filter)

            resp = self._send_command("GetALU_ItemRevisionLinks", head, body)

            self._check_method_result(resp, ['Body', 'GetALU_ItemRevisionLinksResponse', 'MethodResult'])
            items = self._convert_et_to_dict(self._get_elm_by_path(resp, ['Body', 'GetALU_ItemRevisionLinksResponse', 'Records'], True), True)
            li = []
            for item in items['item'] if type(items['item']) is list else [items['item']]:
                li.append(AluItemRevisionLink(self._altium_api).from_dict(item))  # type: ignore
            return li
        except (InternalConnectionException, DataException):
            raise ConnectionException()
