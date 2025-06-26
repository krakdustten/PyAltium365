from __future__ import annotations

import re
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Generic, List, Optional, Tuple, TypeVar, Union, TYPE_CHECKING

from pydantic import BaseModel, Field

from py_altium365.base.connection_handler import ConnectionHandler
from py_altium365.connection.json_con import JsonCon, JsonRequest, JsonReturn


if TYPE_CHECKING:
    from py_altium365.altium_api_workspace import AltiumApiWorkspace


class FacedType(str, Enum):
    """Faced type."""

    NO_TYPE = ""
    CAPACITANCE = "0629FA77_2DBB3E_2D4045_2D91F0_2DCC1164D3D0AADD420E8DDD8B445E911A0601BB2B6D53"
    RESISTANCE = "B90F0DAE_2DB695_2D41F5_2DBCB0_2D0DE5F75C9E50DD420E8DDD8B445E911A0601BB2B6D53"
    VOLTAGE = "28379228_2DD94F_2D4F3B_2D8038_2D3FE85C36E292DD420E8DDD8B445E911A0601BB2B6D53"
    TOLERANCE = "935791AE_2D95D8_2D4D5E_2DB810_2DE9B66A56E5A5DD420E8DDD8B445E911A0601BB2B6D53"
    FREQUENCY = "F4CAEC49_2DEE33_2D46C9_2DAF4A_2D260721F7AA26DD420E8DDD8B445E911A0601BB2B6D53"
    DISTANCE = "B0C104C5_2D1A99_2D4DE5_2DA539_2DD5FC817D4B3EDD420E8DDD8B445E911A0601BB2B6D53"
    POWER = "A40E567D_2D1324_2D4823_2D8379_2DFB7E896E18B9DD420E8DDD8B445E911A0601BB2B6D53"

    @classmethod
    def _missing_(cls, value):  # type: ignore
        return FacedType.NO_TYPE


encoding_decoding_naming = {
    "_5F": "_",
    "_20": " ",
    "_28": "(",
    "_29": ")",
    "_2C": ",",
    "_2D": "-",
    "_2E": ".",
    "_2F": "/",
    "_40": "@",
    "_5B": "[",
    "_5D": "]",
    "_5E": "^",
}


class JsonDtoSearchConditionBaseQuery(BaseModel):
    """Base class for search conditions."""


JsonDtoSearchConditionBaseQueryTypeT = TypeVar("JsonDtoSearchConditionBaseQueryTypeT", bound=JsonDtoSearchConditionBaseQuery)


class JsonDtoSearchConditionTerm(BaseModel):
    """Search condition term."""

    rtype: str = Field(alias="$type", default="DtoSearchConditionTerm")
    field: str = Field(alias="Field")
    value: str = Field(alias="Value")


class JsonDtoSearchConditionStrictQuery(JsonDtoSearchConditionBaseQuery):
    """Strict search query."""

    rtype: str = Field(alias="$type", default="DtoSearchConditionStrictQuery")
    term: JsonDtoSearchConditionTerm = Field(alias="Term")


class JsonDtoSearchConditionRangeQuery(JsonDtoSearchConditionBaseQuery):
    """Range search query."""

    rtype: str = Field(alias="$type", default="DtoSearchConditionRangeQuery")
    field: str = Field(alias="Field")
    field_type: int = Field(alias="FieldType", default=1)
    min: float = Field(alias="Min", default=0)
    max: float = Field(alias="Max", default=0)
    precision_step: int = Field(alias="PrecisionStep", default=0)
    min_inclusive: bool = Field(alias="MinInclusive", default=False)
    max_inclusive: bool = Field(alias="MaxInclusive", default=False)


class JsonDtoSearchConditionWildcardQuery(JsonDtoSearchConditionBaseQuery):
    """Wildcard search query."""

    rtype: str = Field(alias="$type", default="DtoSearchConditionWildcardQuery")
    term: JsonDtoSearchConditionTerm = Field(alias="Term")


class JsonDtoSearchConditionBooleanQueryItem(BaseModel, Generic[JsonDtoSearchConditionBaseQueryTypeT]):
    """Boolean search query item."""

    rtype: str = Field(alias="$type", default="DtoSearchConditionBooleanQueryItem")
    item: JsonDtoSearchConditionBaseQueryTypeT = Field(alias="Item")
    occur: int = Field(alias="Occur", default=0)


class JsonDtoSearchConditionBooleanQuery(JsonDtoSearchConditionBaseQuery):
    """Boolean search query."""

    rtype: str = Field(alias="$type", default="DtoSearchConditionBooleanQuery")
    items: List[JsonDtoSearchConditionBooleanQueryItem] = Field(alias="Items", default=[])


class JsonSearchAsyncRequest(JsonRequest):
    """JSON search async request."""

    rtype: str = Field(alias="$type", default="SearchRequest")
    condition: JsonDtoSearchConditionBooleanQuery = Field(alias="Condition")
    sort_fields: List[str] = Field(alias="SortFields", default=[])
    return_fields: List[str] = Field(alias="ReturnFields", default=[])
    start: int = Field(alias="Start", default=0)
    limit: int = Field(alias="Limit", default=0)
    include_facets: bool = Field(alias="IncludeFacets", default=True)
    use_only_best_facets: bool = Field(alias="UseOnlyBestFacets", default=False)
    include_debug_info: bool = Field(alias="IncludeDebugInfo", default=False)
    ingnore_case_field_names: bool = Field(alias="IgnoreCaseFieldNames", default=False)


class JsonField(BaseModel):
    """Field."""

    name: str = Field(alias="Name")
    value: str = Field(alias="Value")
    field_type: int = Field(alias="FieldType", default=0)


class JsonDocument(BaseModel):
    """Document."""

    score: float = Field(alias="Score")
    fields: List[JsonField] = Field(alias="Fields")


class JsonCounter(BaseModel):
    """Counter."""

    value: str = Field(alias="Value")
    count: int = Field(alias="Count")


class JsonFacetedCounter(BaseModel):
    """Faceted counter."""

    faced_name: str = Field(alias="FacetName")
    faced_type: FacedType = Field(default=FacedType.NO_TYPE)
    total_hit_count: int = Field(alias="TotalHitCount")
    counters: List[JsonCounter] = Field(alias="Counters")
    support_range: bool = Field(alias="SupportRange", default=False)


class JsonSearchAsyncReturn(JsonReturn):
    """JSON search async return."""

    documents: List[JsonDocument] = Field(alias="Documents", default=[])
    faceted_counters: List[JsonFacetedCounter] = Field(alias="FacetedCounters", default=[])
    total: int = Field(alias="Total", default=0)
    success: bool = Field(alias="Success", default=False)


class SearchDataBase(BaseModel):
    """Search data base. The base class for search data."""

    altium_workspace: object
    id: str = Field(alias="Id", default="")
    parameters: Dict[str, Union[str, float]] = Field(default_factory=lambda: {}, alias="Parameters")
    hrid: str = Field(alias="HRID", default="")
    created_at: datetime = Field(alias="CreatedAt", default=datetime(1899, 12, 31))
    created_by: str = Field(alias="CreatedBy", default="")
    modified_by: str = Field(alias="ModifiedBy", default="")
    latest_revision: bool = Field(alias="LatestRevision", default=False)
    updated: datetime = Field(alias="Updated", default=datetime(1899, 12, 31))
    created_by_guid: str = Field(alias="CreatedByGUID", default="")
    updated_by_guid: str = Field(alias="UpdatedByGUID", default="")
    app_type: str = Field(alias="AppType", default="")
    url: str = Field(alias="Url", default="")
    submit_date: datetime = Field(alias="SubmitDate", default=datetime(1899, 12, 31))
    language: str = Field(alias="Language", default="")
    folder_guid: str = Field(alias="FolderGUID", default="")
    folder_full_path: str = Field(alias="FolderFullPath", default="")
    description: str = Field(alias="Description", default="")
    naming_scheme_guid: str = Field(alias="NamingSchemeGuid", default="")
    cat: str = Field(alias="Cat", default="")
    content_type_guid: str = Field(alias="ContentTypeGUID", default="")
    text: str = Field(alias="Text", default="")
    life_cycle: str = Field(alias="LifeCycle", default="")
    acl: str = Field(alias="ACL", default="")
    item_hrid: str = Field(alias="ItemHRID", default="")
    comment: str = Field(alias="Comment", default="")
    life_cycle_state_guid: str = Field(alias="LifeCycleStateGUID", default="")
    item_guid: str = Field(alias="ItemGUID", default="")
    revision_id: str = Field(alias="RevisionId", default="")
    ancestor_revision_guid: str = Field(alias="AncestorRevisionGUID", default="")
    item_description: str = Field(alias="ItemDescription", default="")
    release_note: str = Field(alias="ReleaseNote", default="")
    release_date: datetime = Field(alias="ReleaseDate", default=datetime(1899, 12, 31))
    release_data_num: datetime = Field(alias="ReleaseDataNum", default=datetime(1899, 12, 31))
    life_cycle_definition_guid: str = Field(alias="LifeCycleDefinitionGUID", default="")
    update_date: datetime = Field(alias="Update Date", default=datetime(1899, 12, 31))
    content_type: str = Field(alias="ContentType", default="")

    def get_item(self) -> Optional[str]:
        if hasattr(self.altium_workspace, "get_item_from_guid"):
            return self.altium_workspace.get_item_from_guid(self.item_guid)


class SearchDataType(str, Enum):
    """Search data type."""

    NO_TYPE = ""
    COMPONENT = "Component"
    FOOTPRINT = "Footprint"
    SYMBOL = "Symbol"
    DATASHEET = "Datasheet"
    PROJECT_TEMPLATE = "Project Template"
    SCHEMATIC_TEMPLATE = "Schematic Template"
    COMPONENT_TEMPLATE = "Component Template"
    SCIPT = "Script"
    LAYERSTACK = "Layerstack"

    @classmethod
    def _missing_(cls, value):  # type: ignore
        return FacedType.NO_TYPE


NOT_COUNTED_SEARCH_PARAMETERS = [
    JsonFacetedCounter(FacetName="LatestRevision", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]),
    JsonFacetedCounter(FacetName="FolderFullPath", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]),
]


class JsonConSearchAsync(JsonCon):
    """JSON connection search async."""

    def __init__(self, altium_workspace: "AltiumApiWorkspace", url: str, session_guid: str, host: str):
        """
        Initialize the JsonConSearchAsync object
        :param url: The URL to send the JSON request to
        :param session_guid: The session GUID
        :param host: The host for the host parameter
        """
        super().__init__(ConnectionHandler.get_instance(), url + "/v1.0/searchasync", session_guid, host)
        self._altium_workspace = altium_workspace
        self._counters_up_to_date = False
        self._search_parameters: List[JsonDtoSearchConditionBooleanQueryItem] = []
        self._search_counters: List[JsonFacetedCounter] = []
        self._total_hits: int = 0

        self._update_search_names_and_counters()

    def add_search_parameter(self, name: str, value: Union[str, List[str]], dtype: FacedType = FacedType.NO_TYPE, remove_old: bool = False) -> bool:
        """
        Add a search parameter
        :param name:
        :param value:
        :param dtype:
        :param remove_old:
        :return:
        """
        self._update_search_names_and_counters()
        if isinstance(value, str):
            value = [value]
        counter: Optional[JsonFacetedCounter] = None
        for c in self._search_counters:
            if c.faced_name == name and c.faced_type == dtype:
                counter = c
                break
        if counter is None:
            return False
        full_name = self._get_index_name_from_name_and_type(counter.faced_name, counter.faced_type)
        s_param: Optional[JsonDtoSearchConditionBooleanQueryItem] = self._get_search_parameter(full_name)
        old_values: list[str] = []
        if s_param is not None and not remove_old:
            old_values = self.get_search_parameter(name, dtype)

        for v in old_values:
            if v not in value:
                value.append(v)
        if s_param is not None:
            self._search_parameters.remove(s_param)

        if len(value) == 0:
            return True

        querry_items = []
        occurance = 1 if len(value) > 1 else 0
        for v in value:
            querry_items.append(
                JsonDtoSearchConditionBooleanQueryItem(
                    Item=JsonDtoSearchConditionStrictQuery(Term=JsonDtoSearchConditionTerm(Field=full_name, Value=v)), Occur=occurance
                )
            )
        if len(querry_items) > 1:
            s_param = JsonDtoSearchConditionBooleanQueryItem(Item=JsonDtoSearchConditionBooleanQuery(Items=querry_items), Occur=0)
        else:
            s_param = querry_items[0]

        self._search_parameters.append(s_param)
        self._counters_up_to_date = False
        return True

    def remove_search_parameter(self, name: str, value: Union[str, List[str], None] = None, dtype: FacedType = FacedType.NO_TYPE) -> bool:
        """
        Remove a search parameter
        :param name: The name of the search parameter
        :param value: The specific value to remove, if None all values are removed
        :param dtype: The data type of the search parameter
        :return: If the search parameter was removed
        """
        old_values = []
        if value is not None:
            if isinstance(value, str):
                value = [value]
            old_values = self.get_search_parameter(name, dtype)
            for v in value:
                if v in old_values:
                    old_values.remove(v)
        self.add_search_parameter(name, old_values, dtype, remove_old=True)
        self._counters_up_to_date = False
        return True

    def get_search_parameter(self, name: str, dtype: FacedType = FacedType.NO_TYPE) -> List[str]:
        """
        Get the search parameter
        :param name: The name of the search parameter
        :param dtype: The data type of the search parameter
        :return: A list of the search parameter values
        """
        ret_val: list[str] = []
        full_name = self._get_index_name_from_name_and_type(name, dtype)
        s_param: Optional[JsonDtoSearchConditionBooleanQueryItem] = self._get_search_parameter(full_name)
        if s_param is not None:
            querry_item_base: JsonDtoSearchConditionBaseQuery = s_param.item
            if isinstance(querry_item_base, JsonDtoSearchConditionStrictQuery):
                ret_val.append(querry_item_base.term.value)

            elif isinstance(querry_item_base, JsonDtoSearchConditionBooleanQuery):
                querry_item_first: JsonDtoSearchConditionBaseQuery = querry_item_base.items[0].item
                if isinstance(querry_item_first, JsonDtoSearchConditionStrictQuery):
                    for item in querry_item_base.items:
                        ret_val.append(item.item.term.value)
        return ret_val

    def get_all_search_parameters(self) -> Dict[str, List[str]]:
        """
        Get all search parameters
        :return: A dictionary of search parameters with the name as the key and a list of values as the value
        """
        ret_val: Dict[str, List[str]] = {}
        for search_param in self._search_parameters:
            querry_item_base: JsonDtoSearchConditionBaseQuery = search_param.item
            if isinstance(querry_item_base, JsonDtoSearchConditionStrictQuery):
                name, _ = self._get_facet_name_and_type(querry_item_base.term.field)
                ret_val[name] = [querry_item_base.term.value]
            elif isinstance(querry_item_base, JsonDtoSearchConditionBooleanQuery):
                querry_item_first: JsonDtoSearchConditionBaseQuery = querry_item_base.items[0].item
                if isinstance(querry_item_first, JsonDtoSearchConditionStrictQuery):
                    name, _ = self._get_facet_name_and_type(querry_item_first.term.field)
                    ret_val[name] = []
                    for item in querry_item_base.items:
                        ret_val[name].append(item.item.term.value)
        return ret_val

    def clear_search_parameters(self) -> None:
        """
        Clear all search parameters
        """
        for i in range(len(self._search_parameters) - 1, -1, -1):
            search_param = self._search_parameters[i]
            querry_item_base: JsonDtoSearchConditionBaseQuery = search_param.item
            if isinstance(querry_item_base, JsonDtoSearchConditionStrictQuery):
                self._search_parameters.remove(search_param)
            elif isinstance(querry_item_base, JsonDtoSearchConditionBooleanQuery):
                querry_item_first: JsonDtoSearchConditionBaseQuery = querry_item_base.items[0].item
                if isinstance(querry_item_first, JsonDtoSearchConditionStrictQuery):
                    self._search_parameters.remove(search_param)
        self._counters_up_to_date = False

    def _get_search_parameter(self, full_name: str) -> Optional[JsonDtoSearchConditionBooleanQueryItem]:
        for search_param in self._search_parameters:
            querry_item_base: JsonDtoSearchConditionBaseQuery = search_param.item
            if isinstance(querry_item_base, JsonDtoSearchConditionStrictQuery):
                if querry_item_base.term.field != full_name:
                    continue
                return search_param
            if isinstance(querry_item_base, JsonDtoSearchConditionBooleanQuery):
                querry_item_first: JsonDtoSearchConditionBaseQuery = querry_item_base.items[0].item
                if isinstance(querry_item_first, JsonDtoSearchConditionStrictQuery):
                    if querry_item_first.term.field != full_name:
                        continue
                    return search_param
        return None

    def add_content_search_parameter(self, value: Union[SearchDataType, List[SearchDataType]], remove_old: bool = False) -> bool:
        """
        Add a content search parameter
        :param value: The content search parameter or a list of content search parameters
        :param remove_old: Remove the old search parameters
        :return: If the search parameter was added successfully
        """
        if not isinstance(value, List):
            value = [value]
        return self.add_search_parameter("ContentType", [v.value for v in value], FacedType.NO_TYPE, remove_old)

    def remove_content_search_parameter(self, value: Union[SearchDataType, List[SearchDataType], None]) -> bool:
        """
        Remove a content search parameter
        :param value: The content search parameter or a list of content search parameters to remove, if None all content search parameters are removed
        :return: If the search parameter was removed successfully
        """
        if value is None:
            return self.remove_search_parameter("ContentType", None, FacedType.NO_TYPE)
        if not isinstance(value, List):
            value = [value]
        return self.remove_search_parameter("ContentType", [v.value for v in value], FacedType.NO_TYPE)

    def add_search_parameter_range(
        self, name: str, min_value: float, max_value: float, min_inclusive: bool = True, max_inclusive: bool = True, dtype: FacedType = FacedType.NO_TYPE
    ) -> bool:
        """
        Add a search parameter range
        :param name: The name of the search parameter
        :param min_value: The minimum value
        :param max_value: The maximum value
        :param min_inclusive: Is the minimum value inclusive
        :param max_inclusive: Is the maximum value inclusive
        :param dtype: The data type of the search parameter
        :return: If the search parameter was added
        """
        counter: Optional[JsonFacetedCounter] = None
        for c in self._search_counters:
            if c.faced_name == name and c.faced_type == dtype:
                counter = c
                break
        if counter is None:
            return False
        if not counter.support_range:
            return False
        self.remove_search_parameter_range(name, dtype)
        full_name = self._get_index_name_from_name_and_type(name, dtype)
        s_param = JsonDtoSearchConditionBooleanQueryItem(
            Item=JsonDtoSearchConditionRangeQuery(Field=full_name, Min=min_value, Max=max_value, MinInclusive=min_inclusive, MaxInclusive=max_inclusive),
            Occur=0,
        )
        self._search_parameters.append(s_param)
        self._counters_up_to_date = False
        return True

    def remove_search_parameter_range(self, name: str, dtype: FacedType = FacedType.NO_TYPE) -> bool:
        """
        Remove a search parameter range
        :param name: The name of the search parameter
        :param dtype: The data type of the search parameter
        :return: If the search parameter was removed
        """
        full_name = self._get_index_name_from_name_and_type(name, dtype)
        s_param = self._get_search_parameter_range(full_name)
        if s_param is None:
            return False
        self._search_parameters.remove(s_param)
        self._counters_up_to_date = False
        return True

    def get_search_parameter_range(self, name: str, dtype: FacedType = FacedType.NO_TYPE) -> Optional[Tuple[float, float, bool, bool]]:
        """
        Get the search parameter range
        :param name: The name of the search parameter
        :param dtype: The data type of the search parameter
        :return: The search parameter range or None if it does not exist
        """
        full_name = self._get_index_name_from_name_and_type(name, dtype)
        s_param = self._get_search_parameter_range(full_name)
        if s_param is None:
            return None
        return s_param.item.min, s_param.item.max, s_param.item.min_inclusive, s_param.item.max_inclusive

    def get_all_search_parameters_range(self) -> Dict[str, Tuple[float, float, bool, bool]]:
        """
        Get all search parameters range
        :return: A dictionary of search parameters with the name as the key and a tuple of the min, max, min inclusive and max inclusive as the value
        """
        ret_val: Dict[str, Tuple[float, float, bool, bool]] = {}
        for search_param in self._search_parameters:
            querry_item_base: JsonDtoSearchConditionBaseQuery = search_param.item
            if isinstance(querry_item_base, JsonDtoSearchConditionRangeQuery):
                name, _ = self._get_facet_name_and_type(querry_item_base.field)
                ret_val[name] = (querry_item_base.min, querry_item_base.max, querry_item_base.min_inclusive, querry_item_base.max_inclusive)
        return ret_val

    def clear_search_parameters_range(self) -> None:
        """
        Clear all search parameters range
        :return: None
        """
        for i in range(len(self._search_parameters) - 1, -1, -1):
            search_param = self._search_parameters[i]
            querry_item_base: JsonDtoSearchConditionBaseQuery = search_param.item
            if isinstance(querry_item_base, JsonDtoSearchConditionRangeQuery):
                self._search_parameters.remove(search_param)
        self._counters_up_to_date = False

    def _get_search_parameter_range(self, full_name: str) -> Optional[JsonDtoSearchConditionBooleanQueryItem]:
        self._update_search_names_and_counters()
        for search_param in self._search_parameters:
            querry_item_base: JsonDtoSearchConditionBaseQuery = search_param.item
            if isinstance(querry_item_base, JsonDtoSearchConditionRangeQuery):
                if querry_item_base.field != full_name:
                    continue
                return search_param
        return None

    def add_search_parameter_wildcard(self, value: str) -> bool:
        """
        Add a search parameter wildcard
        :param value: The value of the wildcard
        :return: If the search parameter was added
        """
        self.remove_search_parameter_wildcard()
        s_param = JsonDtoSearchConditionBooleanQueryItem(
            Item=JsonDtoSearchConditionBooleanQuery(
                Items=[
                    JsonDtoSearchConditionBooleanQueryItem(
                        Item=JsonDtoSearchConditionWildcardQuery(Term=JsonDtoSearchConditionTerm(Field="TextC623975962814A5FAAD7FA1CD85DA0DB", Value=value)),
                        Occur=1,
                    ),
                    JsonDtoSearchConditionBooleanQueryItem(
                        Item=JsonDtoSearchConditionWildcardQuery(
                            Term=JsonDtoSearchConditionTerm(Field="DynamicDataC623975962814A5FAAD7FA1CD85DA0DB", Value=value)
                        ),
                        Occur=1,
                    ),
                ]
            ),
            Occur=0,
        )
        self._search_parameters.append(s_param)
        self._counters_up_to_date = False
        return True

    def remove_search_parameter_wildcard(self) -> bool:
        """
        Remove a search parameter wildcard
        :return: If the search parameter was removed
        """
        search_param = self._get_search_parameter_wildcard()
        if search_param is not None:
            self._search_parameters.remove(search_param)
            self._counters_up_to_date = False
            return True
        return False

    def get_search_parameter_wildcard(self) -> Optional[str]:
        """
        Get the search parameter wildcard
        :return: The search parameter wildcard or None if it does not exist
        """
        search_param = self._get_search_parameter_wildcard()
        if search_param is not None:
            return search_param.item.items[0].item.term.value
        return None

    def _get_search_parameter_wildcard(self) -> Optional[JsonDtoSearchConditionBooleanQueryItem]:
        for search_param in self._search_parameters:
            possible_wildcard_name = None
            querry_item_base: JsonDtoSearchConditionBaseQuery = search_param.item
            if isinstance(querry_item_base, JsonDtoSearchConditionBooleanQuery):
                if len(querry_item_base.items) != 2:
                    continue
                for item in querry_item_base.items:
                    if not isinstance(item.item.term, JsonDtoSearchConditionTerm):
                        continue
                    name, dtype = self._get_facet_name_and_type(item.item.term.field)
                    if dtype != FacedType.NO_TYPE:
                        continue
                    if name not in ["Text", "DynamicData"]:
                        continue
                    if possible_wildcard_name is None:
                        possible_wildcard_name = item.item.term.value
                    elif possible_wildcard_name == item.item.term.value:
                        return search_param
        return None

    def get_current_count(self) -> int:
        """
        Get the current count of the search
        :return: The current count of the search
        """
        self._update_search_names_and_counters()
        return self._total_hits

    def get_all_search_names_and_type(self) -> List[Tuple[str, FacedType]]:
        """
        Get all search names and types currently available
        :return: The search names and types currently available
        """
        self._update_search_names_and_counters()
        ret_val: List[Tuple[str, FacedType]] = []
        for counter in self._search_counters:
            ret_val.append((counter.faced_name, counter.faced_type))
        return ret_val

    def get_all_search_names(self) -> List[str]:
        """
        Get all search names currently available
        :return: The search names currently available
        """
        self._update_search_names_and_counters()
        ret_val: List[str] = []
        for counter in self._search_counters:
            ret_val.append(counter.faced_name)
        return ret_val

    def get_all_search_names_range(self) -> List[str]:
        """
        Get all search names that support range
        :return: The search names that support range
        """
        self._update_search_names_and_counters()
        ret_val: List[str] = []
        for counter in self._search_counters:
            if counter.support_range:
                ret_val.append(counter.faced_name)
        return ret_val

    def get_all_search_names_and_type_range(self) -> List[Tuple[str, FacedType]]:
        """
        Get all search names and types that support range
        :return: The search names and types that support range
        """
        self._update_search_names_and_counters()
        ret_val: List[Tuple[str, FacedType]] = []
        for counter in self._search_counters:
            if counter.support_range:
                ret_val.append((counter.faced_name, counter.faced_type))
        return ret_val

    def get_results(self, max_amount: int = 500) -> List[SearchDataBase]:
        """
        Get the search results
        :return: The search results
        """
        max_amount = min(max_amount, 10000)  # Max amount of results per request is 10000
        self._update_search_names_and_counters()
        results: List[SearchDataBase] = []
        while len(results) < max_amount:
            cmd_ret = self._send_command(
                JsonSearchAsyncRequest(
                    Condition=JsonDtoSearchConditionBooleanQuery(Items=self._search_parameters), Limit=min(max_amount - len(results), 10000), Start=len(results)
                ),
                JsonSearchAsyncReturn,
            )

            if not cmd_ret.success:
                raise ConnectionError("Failed to get search results")

            for doc in cmd_ret.documents:
                data = SearchDataBase(altium_workspace=self._altium_workspace)
                for field in doc.fields:
                    name, _ = self._get_facet_name_and_type(field.name)
                    value = field.value

                    for mf_name, mf_type in data.model_fields.items():
                        if mf_type.alias is not None and mf_type.alias == name:
                            name = mf_name
                            break
                    self._add_data_to_data_base(data, name, value)

                results.append(data)
            if len(cmd_ret.documents) < 10000:
                break
        return results

    def _add_data_to_data_base(self, data: SearchDataBase, name: str, value) -> None:
        if not hasattr(data, name):
            data.parameters[name] = value
            return
        if isinstance(getattr(data, name), datetime):
            if value.replace(".", "", 1).isdecimal():
                d = datetime(1899, 12, 31)
                setattr(data, name, d + timedelta(days=float(value)))
            else:
                setattr(data, name, datetime.strptime(value, "%m/%d/%Y %H:%M:%S"))
        elif isinstance(getattr(data, name), int):
            setattr(data, name, int(value))
        elif isinstance(getattr(data, name), bool):
            setattr(data, name, int(value) > 0)
        else:
            setattr(data, name, value)

    def _update_search_names_and_counters(self) -> None:
        if self._counters_up_to_date:
            return
        cmd_ret = self._send_command(
            JsonSearchAsyncRequest(
                Condition=JsonDtoSearchConditionBooleanQuery(Items=self._search_parameters),
            ),
            JsonSearchAsyncReturn,
        )

        if not cmd_ret.success:
            raise ConnectionError("Failed to get search names and counters")

        self._search_counters = cmd_ret.faceted_counters
        for counter in self._search_counters:
            if counter.faced_type == FacedType.NO_TYPE:
                counter.faced_name, counter.faced_type = self._get_facet_name_and_type(counter.faced_name)

        self._search_counters += NOT_COUNTED_SEARCH_PARAMETERS
        self._total_hits = cmd_ret.total
        self._counters_up_to_date = True

    def _get_facet_name_and_type(self, indexed_name: str) -> Tuple[str, FacedType]:
        m1 = re.match("^(.*)_5F([0-9A-F]{8}_[0-9A-F]{6}_[0-9A-F]{6}_[0-9A-F]{6}_[0-9A-F]{46})$", indexed_name)
        m2 = re.match("^(.*)([0-9A-F]{32})$", indexed_name)
        if m1 is not None:
            name = m1.group(1)
            ftype = m1.group(2)
        elif m2 is not None:
            name = m2.group(1)
            ftype = m2.group(2)
        else:
            name = indexed_name
            ftype = ""

        return self._decode_naming_chars(name), FacedType(ftype)

    def _get_index_name_from_name_and_type(self, name: str, ftype: FacedType) -> str:
        if ftype == FacedType.NO_TYPE:
            full_name = self._encode_naming_chars(name)
            full_name += "DD420E8DDD8B445E911A0601BB2B6D53"
        else:
            full_name = self._encode_naming_chars(name)
            full_name += "_5F" + ftype.value
        return full_name

    def _decode_naming_chars(self, inp: str) -> str:
        for key, val in encoding_decoding_naming.items():
            inp = inp.replace(key, val)
        return inp

    def _encode_naming_chars(self, inp: str) -> str:
        for key, val in encoding_decoding_naming.items():
            inp = inp.replace(val, key)
        return inp
