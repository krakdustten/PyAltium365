from typing import TYPE_CHECKING, Dict, Any
from PyAltium365.Connections.JsonCon import JsonCon
from PyAltium365.Data.DataConSearchAsync import AsyncSearchObject, SearchType
from requests import Session


if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class JsonConSearchAsync(JsonCon):
    def __init__(self, session: Session, url: str, altium_api: AltiumApi):
        super().__init__(session, url + "/v1.0/searchasync")
        self._altium_api = altium_api

    def get_part_counters(self, search_object: AsyncSearchObject) -> Dict[str, Any]:
        return self.get_search_interface(search_object)

    def get_search_interface(self, search_object: AsyncSearchObject, start: int = 0, limit: int = 0) -> Dict[str, Any]:
        obj_s_l = []
        for so in search_object._search_parameters:
            if so["Type"] == SearchType.CONDITIONAL_QUERY:
                if len(so["Value"]) == 1:
                    dso = {
                        "$type": "DtoSearchConditionBooleanQueryItem",
                        "Item": {
                            "$type": so["Type"].value,
                            "Term": {
                                "$type": "DtoSearchConditionTerm",
                                "Field": so["Field"],
                                "Value": so["Value"][0]
                            }
                        },
                        "Occur": 0
                    }
                else:
                    item_list = []
                    for value in so["Value"]:
                        item_list.append({
                            "$type": "DtoSearchConditionBooleanQueryItem",
                            "Item": {
                                "$type": so["Type"].value,
                                "Term": {
                                    "$type": "DtoSearchConditionTerm",
                                    "Field": so["Field"],
                                    "Value": value
                                }
                            },
                            "Occur": 1
                        })

                    dso = {
                        "$type": "DtoSearchConditionBooleanQueryItem",
                        "Item": {
                            "$type": "DtoSearchConditionBooleanQuery",
                            'Items': item_list,
                        },
                        "Occur": 0
                    }
            elif so["Type"] == SearchType.CONDITIONAL_RANGE_QUERY:
                dso = {
                    "$type": "DtoSearchConditionBooleanQueryItem",
                    "Item": {
                        "$type": so["Type"].value,
                        "Field": so["Field"],
                        "FieldType": 1,
                        "Min": so["Min"],
                        "Max": so["Max"],
                        "PrecisionStep": 0,
                        "MinInclusive": so["MinInc"],
                        "MaxInclusive": so["MaxInc"]
                    },
                    "Occur": 0
                }
            elif so["Type"] == SearchType.CONDITIONAL_WILDCARD:
                dso = {
                    "$type": "DtoSearchConditionBooleanQueryItem",
                    "Item": {
                        "$type": "DtoSearchConditionBooleanQuery",
                        "Items": [
                            {
                                "$type": "DtoSearchConditionBooleanQueryItem",
                                "Item": {
                                    "$type": "DtoSearchConditionWildcardQuery",
                                    "Term": {
                                        "$type": "DtoSearchConditionTerm",
                                        "Field": "TextC623975962814A5FAAD7FA1CD85DA0DB",
                                        "Value": so["Value"]
                                    }
                                },
                                "Occur": 1
                            },
                            {
                                "$type": "DtoSearchConditionBooleanQueryItem",
                                "Item": {
                                    "$type": "DtoSearchConditionWildcardQuery",
                                    "Term": {
                                        "$type": "DtoSearchConditionTerm",
                                        "Field": "DynamicDataC623975962814A5FAAD7FA1CD85DA0DB",
                                        "Value": so["Value"]
                                    }
                                },
                                "Occur": 1
                            }
                        ]
                    },
                    "Occur": 0
                }
            obj_s_l.append(dso)

        obj_s = {
            "$type": "SearchRequest",
            "Condition": {
                "$type": "DtoSearchConditionBooleanQuery",
                "Items": obj_s_l
            },
            "SortFields": [],
            "ReturnFields": [],
            "Start": start,
            "Limit": limit,
            "IncludeFacets": True,
            "UseOnlyBestFacets": False,
            "IncludeDebugInfo": False,
            "IgnoreCaseFieldNames": False
        }
        return self._send_command(self._altium_api, obj_s)
