from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from pydantic_xml import BaseXmlModel, element, wrapped, attr

from py_altium365.base.connection_handler import ConnectionHandler
from py_altium365.connection.soapy_con import SoapyCon

if TYPE_CHECKING:
    from py_altium365.altium_api_workspace import AltiumApiWorkspace


class SoapMethodOption(str, Enum):
    """Enum for SOAP method options."""

    INCLUDE_ALL_CHILD_OBJECTS = "IncludeAllChildObjects=True"
    EXCLUDE_ACL_ENTRIES = "ExcludeACLEntries=True"
    SUPPORT_OWNER_ACL_TYPE = "SupportOwnerAclType=True"


class AluObject(BaseXmlModel, tag="item", nsmap={"temp": "http://tempuri.org/"}, ns="temp"):
    """Base class for Altium Vault objects."""

    guid: Optional[str] = element(tag="GUID", default=None)
    hrid: Optional[str] = element(tag="HRID", default=None)
    created_at: Optional[datetime] = element(tag="CreatedAt", default=None)
    last_modified_at: Optional[datetime] = element(tag="LastModifiedAt", default=None)
    created_by_guid: Optional[str] = element(tag="CreatedByGUID", default=None)
    last_modified_by_guid: Optional[str] = element(tag="LastModifiedByGUID", default=None)
    created_by_name: Optional[str] = element(tag="CreatedByName", default=None)
    last_modified_by_name: Optional[str] = element(tag="LastModifiedByName", default=None)


class AluShareableObject(AluObject):
    """Base class for shareable Altium Vault objects."""

    sharing_control: Optional[int] = element(tag="SharingControl", default=None)
    access_rights: Optional[int] = element(tag="AccessRights", default=None)


class AluItemRevisionParameter(AluObject):
    """Class representing an item revision parameter in Altium Vault."""

    parameter_value: Optional[str] = element(tag="ParameterValue", default=None)
    item_revision_guid: Optional[str] = element(tag="ItemRevisionGUID", default=None)
    parameter_type_guid: Optional[str] = element(tag="ParameterTypeGUID", default=None)
    parameter_real_value: Optional[float] = element(tag="ParameterRealValue", default=None)


class AluLifeCycleStateChange(AluObject):
    """Class representing a life cycle state change in Altium Vault."""

    item_revision_guid: Optional[str] = element(tag="ItemRevisionGUID", default=None)
    life_cycle_state_transition_guid: Optional[str] = element(tag="LifeCycleStateTransitionGUID", default=None)
    life_cycle_state_after_guid: Optional[str] = element(tag="LifeCycleStateAfterGUID", default=None)
    note: Optional[str] = element(tag="Note", default=None)


class AluItemRevision(AluShareableObject, tag="item", nsmap={"temp": "http://tempuri.org/"}, ns="temp"):
    """Class representing an item revision in Altium Vault."""

    revision_id: Optional[str] = element(tag="RevisionId", default=None)
    ancestor_item_revision_guid: Optional[str] = element(tag="AncestorItemRevisionGUID", default=None)
    description: Optional[str] = element(tag="Description", default=None)
    comment: Optional[str] = element(tag="Comment", default=None)
    lifecycle_state_guid: Optional[str] = element(tag="LifeCycleStateGUID", default=None)
    item_guid: Optional[str] = element(tag="ItemGUID", default=None)
    release_date: Optional[datetime] = element(tag="ReleaseDate", default=None)
    item_hrid: Optional[str] = element(tag="ItemHRID", default=None)
    item_description: Optional[str] = element(tag="ItemDescription", default=None)
    content_type_guid: Optional[str] = element(tag="ContentTypeGUID", default=None)
    folder_guid: Optional[str] = element(tag="FolderGUID", default=None)
    revision_id_levels: List[str] = wrapped(path="RevisionIdLevels", entity=element(tag="item", default=None), default=[])
    revision_id_separators: List[str] = wrapped(
        path="RevisionIdSeparators",
        entity=element(tag="item", default=None),
        default=[],
    )
    revision_parameters: List[AluItemRevisionParameter] = wrapped(
        path="RevisionParameters",
        default=[],
    )
    state_changes: List[AluLifeCycleStateChange] = wrapped(
        path="StateChanges",
        default=[],
    )
    is_shared: Optional[bool] = element(tag="IsShared", default=None)
    is_payload_shared: Optional[bool] = element(tag="IsPayloadShared", default=None)
    source_vault_guid: Optional[str] = element(tag="SourceVaultGUID", default=None)
    source_guid: Optional[str] = element(tag="SourceGUID", default=None)
    is_visible: Optional[bool] = element(tag="IsVisible", default=None)
    is_applicable: Optional[bool] = element(tag="IsApplicable", default=None)
    is_active: Optional[bool] = element(tag="IsActive", default=None)


class AluTag(AluObject):
    """Class representing a tag in Altium Vault."""

    tag_family_guid: Optional[str] = element(tag="TagFamilyGUID", default=None)
    parant_tag_guid: Optional[str] = element(tag="ParentTagGUID", default=None)
    sub_tags: List[AluTag] = wrapped(
        path="SubTags",
        default=[],
    )


class AluItemParameter(AluObject):
    """Class representing an item parameter in Altium Vault."""

    parameter_value: Optional[str] = element(tag="ParameterValue", default=None)
    item_guid: Optional[str] = element(tag="ItemGUID", default=None)
    parameter_type_guid: Optional[str] = element(tag="ParameterTypeGUID", default=None)
    parameter_real_value: Optional[float] = element(tag="ParameterRealValue", default=None)


class AluItem(AluShareableObject, tag="item", nsmap={"temp": "http://tempuri.org/"}, ns="temp"):
    """Class representing an item in Altium Vault."""

    description: Optional[str] = element(tag="Description", default=None)
    folder_guid: Optional[str] = element(tag="FolderGUID", default=None)
    lifecycle_definition_guid: Optional[str] = element(tag="LifeCycleDefinitionGUID", default=None)
    revision_naming_scheme_guid: Optional[str] = element(tag="RevisionNamingSchemeGUID", default=None)
    content_type_guid: Optional[str] = element(tag="ContentTypeGUID", default=None)
    revisions: List[AluItemRevision] = wrapped(
        path="Revisions",
        default=[],
    )
    is_shared: bool = element(tag="IsShared", default=False)
    tags: List[AluTag] = wrapped(
        path="Tags",
        default=[],
    )
    item_parameters: List[AluItemParameter] = wrapped(
        path="ItemParameters",
        default=[],
    )
    is_active: bool = element(tag="IsActive", default=False)

    def get_folder(self, altium_workspace: "AltiumApiWorkspace") -> Optional[AluFolder]:
        """
        Get the folder associated with this item.
        :param altium_workspace: The Altium API workspace object.
        :return: An AluFolder object if found, otherwise None.
        """
        if self.folder_guid:
            return altium_workspace.get_folder_from_guid(self.folder_guid)
        return None


class AluFolderParameter(AluObject):
    """Class representing an item parameter in Altium Vault."""

    folder_guid: Optional[str] = element(tag="FolderGUID", default=None)
    default_value: Optional[str] = element(tag="DefaultValue", default=None)


class AluFolder(AluShareableObject, tag="item", nsmap={"temp": "http://tempuri.org/"}, ns="temp"):
    """Class representing a folder in Altium Vault."""

    description: Optional[str] = element(tag="Description", default=None)
    shared_name: Optional[str] = element(tag="SharedName", default=None)
    is_shared: bool = element(tag="IsShared", default=False)
    folder_type_guid: Optional[str] = element(tag="FolderTypeGUID", default=None)
    parent_folder_guid: Optional[str] = element(tag="ParentFolderGUID", default=None)
    facet_count: Optional[int] = element(tag="FacetCount", default=None)
    attributes: Optional[int] = element(tag="Attributes", default=None)
    folder_parameters: List[AluFolderParameter] = wrapped(
        path="FolderParameters",
        default=[],
    )
    sub_folders: List[AluFolder] = wrapped(
        path="SubFolders",
        default=[],
    )
    weight: Optional[int] = element(tag="Weight", default=None)
    is_active: bool = element(tag="IsActive", default=False)

    def get_parent_folder(self, altium_workspace: "AltiumApiWorkspace") -> Optional[AluFolder]:
        """
        Get the parent folder of this folder.
        :param altium_workspace: The Altium API workspace object.
        :return: An AluFolder object if found, otherwise None.
        """
        if self.parent_folder_guid:
            return altium_workspace.get_folder_from_guid(self.parent_folder_guid)
        return None

    def get_child_folders(self, altium_workspace: "AltiumApiWorkspace") -> List[AluFolder]:
        """
        Get all child folders of this folder.
        :param altium_workspace: The Altium API workspace object.
        :return: A list of AluFolder objects representing the child folders.
        """
        return altium_workspace.get_folders_in_folder(self)

    def get_items(self, altium_workspace: "AltiumApiWorkspace") -> List[AluItem]:
        """
        Get all items in this folder.
        :param altium_workspace: The Altium API workspace object.
        :return: A list of AluItem objects in this folder.
        """
        return altium_workspace.get_items_in_folder(self)


class SoapConVaultBase(SoapyCon):
    """Base class for SOAP connection to Altium Vault."""

    def __init__(self, altium_workspace: "AltiumApiWorkspace"):
        """
        Initialize the SOAP connection to Altium Vault.
        :param altium_workspace: The Altium API workspace object.
        """
        super().__init__(ConnectionHandler.get_instance(), altium_workspace.workspace_url + "/vault/?cls=soap")
        self._altium_workspace = altium_workspace
