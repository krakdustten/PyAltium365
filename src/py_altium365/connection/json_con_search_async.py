from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

from py_altium365.base.connection_handler import ConnectionHandler
from py_altium365.connection.json_con import JsonCon, JsonRequest, JsonReturn


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
    field_type: int = Field(alias="FieldType", default=0)
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
    total_hit_count: int = Field(alias="TotalHitCount")
    counters: List[JsonCounter] = Field(alias="Counters")
    support_range: bool = Field(alias="SupportRange", default=False)


class JsonSearchAsyncReturn(JsonReturn):
    """JSON search async return."""

    documents: List[JsonDocument] = Field(alias="Documents", default=[])
    faceted_counters: List[JsonFacetedCounter] = Field(alias="FacetedCounters", default=[])
    total: int = Field(alias="Total", default=0)
    success: bool = Field(alias="Success", default=False)


class JsonConSearchAsync(JsonCon):
    """JSON connection search async."""

    def __init__(self, url: str, session_guid: str, host: str):
        """
        Initialize the JsonConSearchAsync object
        :param url: The URL to send the JSON request to
        :param session_guid: The session GUID
        :param host: The host for the host parameter
        """
        super().__init__(ConnectionHandler.get_instance(), url + "/v1.0/searchasync", session_guid, host)

    def get_search_interface(self):
        """
        Get a new search interface
        :return: The search interface
        """
        request = JsonSearchAsyncRequest(
            Limit=2,
            Condition=JsonDtoSearchConditionBooleanQuery(
                Items=[
                    JsonDtoSearchConditionBooleanQueryItem[JsonDtoSearchConditionStrictQuery](
                        Item=JsonDtoSearchConditionStrictQuery(
                            Term=JsonDtoSearchConditionTerm(Field="ContentTypeDD420E8DDD8B445E911A0601BB2B6D53", Value="Component")
                        )
                    )
                ]
            ),
        )

        ret = self._send_command(request, JsonSearchAsyncReturn)
        print(ret)
