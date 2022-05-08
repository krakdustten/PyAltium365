from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from PyAltium365.Helpers.DataClassDict import dataclassdict, field_dict

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi
    from PyAltium365.Data.DataConVaultPredef import AluLifeCycleDefinition, AluItemRevision, AluLifeCycleStateChange, AluLifeCycleStateTransition


@dataclass
@dataclassdict
class AluBase:
    altium_api: AltiumApi
    GUID: str = field_dict(dict_name=["GUID"], default=None)
    HRID: str = field_dict(dict_name=["HRID"], default=None)
    CreatedAt: datetime = field_dict(dict_name=["CreatedAt"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    CreatedByGUID: str = field_dict(dict_name=["CreatedByGUID"], default=None)
    LastModifiedAt: datetime = field_dict(dict_name=["LastModifiedAt"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    LastModifiedByGUID: str = field_dict(dict_name=["LastModifiedByGUID"], default=None)
    LastModifiedByName: str = field_dict(dict_name=["LastModifiedByName"], default=None)
    AccessRights: int = field_dict(dict_name=["AccessRights"], default=None)
    Description: str = field_dict(dict_name=["Description"], default=None)

    def get_created_by(self) -> None:
        raise NotImplementedError()

    def get_last_modified_by(self) -> None:
        raise NotImplementedError()


@dataclass
@dataclassdict
class AluVault(AluBase):
    CreateDate: datetime = field_dict(dict_name=["createdate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    AcquisitionServiceURL: str = field_dict(dict_name=["AcquisitionServiceURL"], default=None)
    AppRegistryServiceURL: str = field_dict(dict_name=["AppRegistryServiceURL"], default=None)
    EventChannel: str = field_dict(dict_name=["EventChannel"], default=None)
    Parameters: str = field_dict(dict_name=["Parameters"], default=None)
    VersionId: str = field_dict(dict_name=["VersionId"], default=None)


@dataclass
@dataclassdict
class AluItem(AluBase):
    CreatedByName: str = field_dict(dict_name=["CreatedByName"], default=None)
    SharingControl: int = field_dict(dict_name=["SharingControl"], default=None)
    FolderGUID: str = field_dict(dict_name=["FolderGUID"], default=None)
    LifeCycleDefinitionGUID: str = field_dict(dict_name=["LifeCycleDefinitionGUID"], default=None)
    RevisionNamingSchemeGUID: str = field_dict(dict_name=["RevisionNamingSchemeGUID"], default=None)
    ContentTypeGUID: str = field_dict(dict_name=["ContentTypeGUID"], default=None)
    IsShared: bool = field_dict(dict_name=["IsShared"], default=None)
    IsActive: bool = field_dict(dict_name=["IsActive"], default=None)

    def get_folder(self) -> None:
        raise NotImplementedError()

    def get_life_cycle_definition(self) -> Optional[AluLifeCycleDefinition]:
        return self.altium_api.get_life_cycle_definition_from_guid(self.LifeCycleDefinitionGUID)

    def get_revision_naming_schema(self) -> None:
        raise NotImplementedError()

    def get_content_type(self) -> None:
        raise NotImplementedError()

    def get_item_revisions(self) -> List[AluItemRevision]:
        return self.altium_api.get_item_revisions_from_item(self)

    def get_latest_item_revision(self) -> Optional[AluItemRevision]:
        return self.altium_api.get_latest_item_revisions_from_item(self)


@dataclass
@dataclassdict
class AluTag(AluBase):
    pass


@dataclass
@dataclassdict
class AluLifeCycleState(AluBase):
    StateIndex: int = field_dict(dict_name=["StateIndex"], default=None)
    LifeCycleStageGUID: str = field_dict(dict_name=["LifeCycleStageGUID"], default=None)
    LifeCycleDefinitionGUID: str = field_dict(dict_name=["LifeCycleDefinitionGUID"], default=None)
    IsInitialState: bool = field_dict(dict_name=["IsInitialState"], default=None)
    Color: str = field_dict(dict_name=["Color"], default=None)
    TextColor: str = field_dict(dict_name=["TextColor"], default=None)
    IsVisible: bool = field_dict(dict_name=["IsVisible"], default=None)
    IsApplicable: bool = field_dict(dict_name=["IsApplicable"], default=None)

    def get_life_cycle_stage(self) -> None:
        raise NotImplementedError()

    def get_life_cycle_definition(self) -> Optional[AluLifeCycleDefinition]:
        return self.altium_api.get_life_cycle_definition_from_guid(self.LifeCycleDefinitionGUID)


@dataclass
@dataclassdict
class AluItemRevision(AluBase):
    SharingControl: int = field_dict(dict_name=["SharingControl"], default=None)
    RevisionId: int = field_dict(dict_name=["RevisionId"], default=None)
    AncestorItemRevisionGUID: str = field_dict(dict_name=["AncestorItemRevisionGUID"], default=None)
    LifeCycleStateGUID: str = field_dict(dict_name=["LifeCycleStateGUID"], default=None)
    ItemGUID: str = field_dict(dict_name=["ItemGUID"], default=None)
    ReleaseDate: datetime = field_dict(dict_name=["ReleaseDate"], default=datetime.min, dict_conv_str='%Y-%m-%dT%H:%M:%S')
    ItemHRID: str = field_dict(dict_name=["ItemHRID"], default=None)
    ItemDescription: str = field_dict(dict_name=["ItemDescription"], default=None)
    ContentTypeGUID: str = field_dict(dict_name=["ContentTypeGUID"], default=None)
    FolderGUID: str = field_dict(dict_name=["FolderGUID"], default=None)
    IsShared: bool = field_dict(dict_name=["IsShared"], default=None)
    IsPayloadShared: bool = field_dict(dict_name=["IsPayloadShared"], default=None)
    IsVisible: bool = field_dict(dict_name=["IsVisible"], default=None)
    IsApplicable: bool = field_dict(dict_name=["IsApplicable"], default=None)
    IsActive: bool = field_dict(dict_name=["IsActive"], default=None)

    def get_ancestor_item_revision(self) -> None:
        raise NotImplementedError()

    def get_life_cycle_state(self) -> Optional[AluLifeCycleState]:
        return self.altium_api.get_life_cycle_state_from_guid(self.LifeCycleStateGUID)

    def get_life_cycle_state_changes(self) -> List[AluLifeCycleStateChange]:
        return self.altium_api.get_life_cycle_state_changes_from_item_revision(self)

    def get_possible_life_cycle_state_transitions(self) -> List[AluLifeCycleStateTransition]:
        return self.altium_api.get_possible_life_cycle_state_transitions_from_item_revision(self)

    def get_item(self) -> Optional[AluItem]:
        return self.altium_api.get_item_from_guid(self.ItemGUID)

    def get_content_type(self) -> None:
        raise NotImplementedError()

    def get_folder(self) -> None:
        raise NotImplementedError()

    def change_life_cycle_state(self, life_cycle_transition: AluLifeCycleStateTransition) -> bool:
        return self.altium_api.change_life_cycle_state([self], [life_cycle_transition])

    def download(self, path: str, rename: Optional[str] = None) -> Optional[str]:
        return self.altium_api.download_item_revision(self, path, rename)

    def get_child_item_revisions(self) -> List[AluItemRevision]:
        return self.altium_api.get_child_item_revisions_from_item_revision(self)

    def get_parent_item_revisions(self) -> List[AluItemRevision]:
        return self.altium_api.get_parent_item_revisions_from_item_revision(self)


@dataclass
@dataclassdict
class AluLifeCycleDefinition(AluBase):
    SharingControl: int = field_dict(dict_name=["SharingControl"], default=None)
    LifeCycleManagement: str = field_dict(dict_name=["LifeCycleManagement"], default=None)
    LinkToRevisionScheme: bool = field_dict(dict_name=["LinkToRevisionScheme"], default=None)
    ControlPerContentType: bool = field_dict(dict_name=["ControlPerContentType"], default=None)


@dataclass
@dataclassdict
class AluLifeCycleStateChange(AluBase):
    CreatedByName: str = field_dict(dict_name=["CreatedByName"], default=None)
    ItemRevisionGUID: str = field_dict(dict_name=["ItemRevisionGUID"], default=None)
    LifeCycleStateTransitionGUID: str = field_dict(dict_name=["LifeCycleStateTransitionGUID"], default=None)
    LifeCycleStateAfterGUID: str = field_dict(dict_name=["LifeCycleStateAfterGUID"], default=None)
    Note: str = field_dict(dict_name=["Note"], default=None)

    def get_item_revision(self) -> Optional[AluItemRevision]:
        return self.altium_api.get_item_revision_from_guid(self.ItemRevisionGUID)

    def get_life_cycle_state_transition(self) -> Optional[AluLifeCycleStateTransition]:
        return self.altium_api.get_life_cycle_state_transition_guid(self.LifeCycleStateTransitionGUID)

    def get_life_cycle_state_after(self) -> None:
        raise NotImplementedError()


@dataclass
@dataclassdict
class AluLifeCycleStateTransition(AluBase):
    CreatedByName: str = field_dict(dict_name=["CreatedByName"], default=None)
    MenuTextFormat: str = field_dict(dict_name=["MenuTextFormat"], default=None)
    LifeCycleStateBeforeGUID: str = field_dict(dict_name=["LifeCycleStateBeforeGUID"], default=None)
    LifeCycleStateAfterGUID: str = field_dict(dict_name=["LifeCycleStateAfterGUID"], default=None)
    LifeCycleDefinitionGUID: str = field_dict(dict_name=["LifeCycleDefinitionGUID"], default=None)
    TransitionIndex: int = field_dict(dict_name=["TransitionIndex"], default=None)
    PermissionType: int = field_dict(dict_name=["PermissionType"], default=None)

    def get_life_cycle_state_before(self) -> Optional[AluLifeCycleState]:
        return self.altium_api.get_life_cycle_state_from_guid(self.LifeCycleStateBeforeGUID)

    def get_life_cycle_state_after(self) -> Optional[AluLifeCycleState]:
        return self.altium_api.get_life_cycle_state_from_guid(self.LifeCycleStateAfterGUID)

    def get_life_cycle_definition(self) -> Optional[AluLifeCycleDefinition]:
        return self.altium_api.get_life_cycle_definition_from_guid(self.LifeCycleDefinitionGUID)


@dataclass
@dataclassdict
class AluItemRevisionLink(AluBase):
    CreatedByName: str = field_dict(dict_name=["CreatedByName"], default=None)
    ChildItemRevisionGUID: str = field_dict(dict_name=["ChildItemRevisionGUID"], default=None)
    ChildVaultGUID: str = field_dict(dict_name=["ChildVaultGUID"], default=None)
    ParentItemRevisionGUID: str = field_dict(dict_name=["ParentItemRevisionGUID"], default=None)
    ParentVaultGUID: str = field_dict(dict_name=["ParentVaultGUID"], default=None)

    def get_parent_item(self) -> Optional[AluItemRevision]:
        return self.altium_api.get_item_revision_from_guid(self.ParentItemRevisionGUID)

    def get_child_item(self) -> Optional[AluItemRevision]:
        return self.altium_api.get_item_revision_from_guid(self.ChildItemRevisionGUID)
