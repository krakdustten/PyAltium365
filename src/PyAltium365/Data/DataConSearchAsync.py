import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Tuple, Union, TYPE_CHECKING, Optional
from PyAltium365.Connections import JsonConSearchAsync
from PyAltium365.Data.DataConVault import AluItem

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class SearchType(Enum):
    CONDITIONAL_QUERY = "DtoSearchConditionStrictQuery"
    CONDITIONAL_RANGE_QUERY = "DtoSearchConditionRangeQuery"
    CONDITIONAL_WILDCARD = "DtoSearchConditionWildcardQuery"


class DataType(Enum):
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
        return DataType.NO_TYPE


@dataclass
class Counter:
    Name: str = ""
    Type: DataType = DataType.NO_TYPE
    Count: int = 0
    Values: Dict[str, int] = field(default_factory=lambda: {})


class CounterRange(Counter):
    Values: Dict[float, int] = field(default_factory=lambda: {})  # type: ignore
    MinValue: float = 0
    MaxValue: float = 0


@dataclass
class Counters:
    TotalCount: int = 0
    Counters: List[Counter] = field(default_factory=lambda: [])


@dataclass
class SearchDataBase:
    altium_api: AltiumApi
    Id: str = ""
    Parameters: Dict[str, Union[str, float]] = field(default_factory=lambda: {})
    HRID: str = ""
    CreatedAt: datetime = datetime(1, 1, 1)
    CreatedBy: str = ""
    ModifiedBy: str = ""
    LatestRevision: bool = False
    Updated: datetime = datetime(1, 1, 1)
    CreatedByGUID: str = ""
    UpdatedByGUID: str = ""
    AppType: str = ""
    Url: str = ""
    SubmitDate: datetime = datetime(1, 1, 1)
    Language: str = ""
    FolderGUID: str = ""
    FolderFullPath: str = ""
    Description: str = ""
    NamingSchemeGuid: str = ""
    Cat: str = ""
    ContentTypeGUID: str = ""
    Text: str = ""
    LifeCycle: str = ""
    ACL: str = ""
    ItemHRID: str = ""
    Comment: str = ""
    LifeCycleStateGUID: str = ""
    ItemGUID: str = ""
    RevisionId: int = -1
    AncestorRevisionGUID: str = ""
    ItemDescription: str = ""
    ReleaseNote: str = ""
    ReleaseDate: datetime = datetime(1, 1, 1)
    ReleaseDateNum: datetime = datetime(1, 1, 1)
    LifeCycleDefinitionGUID: str = ""

    def get_folder(self) -> None:
        raise NotImplementedError()

    def get_created_by(self) -> None:
        raise NotImplementedError()

    def get_updated_by(self) -> None:
        raise NotImplementedError()

    def get_content_type(self) -> None:
        raise NotImplementedError()

    def get_item(self) -> Optional[AluItem]:
        return self.altium_api.get_item_from_guid(self.ItemGUID)

    def get_life_cycle_state(self) -> None:
        raise NotImplementedError()

    def get_life_cycle_definition(self) -> None:
        raise NotImplementedError()

    def get_ancestor_revision(self) -> None:
        raise NotImplementedError()


@dataclass
class SearchDataComponent(SearchDataBase):
    FootprintName: List[str] = field(default_factory=lambda: [])
    FootprintDescription: List[str] = field(default_factory=lambda: [])


@dataclass
class SearchDataFootprint(SearchDataBase):
    pass


@dataclass
class SearchDataSymbol(SearchDataBase):
    pass


@dataclass
class SearchDataDatasheet(SearchDataBase):
    FileName: str = ""
    Caption: str = ""
    FileHash: str = ""
    FileSize: str = ""
    DynamicData: str = ""


@dataclass
class SearchDataProjectTemplate(SearchDataBase):
    MainFilename: str = ""
    Kind: str = ""
    DynamicData: str = ""


@dataclass
class SearchDataSchematicTemplate(SearchDataBase):
    pass


@dataclass
class SearchDataComponentTemplate(SearchDataBase):
    DynamicData: str = ""


@dataclass
class SearchDataScript(SearchDataBase):
    DynamicData: str = ""
    MainFilename: str = ""
    Kind: str = ""


@dataclass
class SearchDataLayerstack(SearchDataBase):
    pass


class SearchDataType(Enum):
    NO_TYPE = ("", SearchDataBase)
    COMPONENT = ("Component", SearchDataComponent)
    FOOTPRINT = ("Footprint", SearchDataFootprint)
    SYMBOL = ("Symbol", SearchDataSymbol)
    DATASHEET = ("Datasheet", SearchDataDatasheet)
    PROJECT_TEMPLATE = ("Project Template", SearchDataProjectTemplate)
    SCHEMATIC_TEMPLATE = ("Schematic Template", SearchDataSchematicTemplate)
    COMPONENT_TEMPLATE = ("Component Template", SearchDataComponentTemplate)
    SCRIPT = ("Script", SearchDataScript)
    LAYERSTACK = ("Layerstack", SearchDataLayerstack)

    @classmethod
    def _missing_(cls, value):  # type: ignore
        return SearchDataType.NO_TYPE

    def get_from_str(self, value: str):  # type: ignore
        for orig in SearchDataType:
            if orig.value[0].lower() == value.lower():
                return orig
        return SearchDataType._missing_(None)


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


not_counted_search_parameters = [
    Counter(Name="LatestRevision"),
    Counter(Name="FolderFullPath")
]


class AsyncSearchObject:
    def __init__(self, searcher: JsonConSearchAsync, altium_api: AltiumApi):  # type: ignore
        self._searcher: JsonConSearchAsync = searcher  # type: ignore
        self._altium_api = altium_api
        self._search_parameters: List[Dict] = []
        self._counters: Counters = Counters()
        self._counters_up_to_date = False
        self._update_search_names_and_counters()

    def add_search_parameter(self, name: str, value: Union[str, List[str]], dtype: DataType = DataType.NO_TYPE, remove_old: bool = False) -> bool:
        self._update_search_names_and_counters()
        if type(value) == str:
            value = [value]
        counter = None
        for c in self._counters.Counters:
            if c.Name == name and c.Type == dtype:
                counter = c
                break
        if counter is None:
            return False
        full_name = self._get_index_name_from_name_and_type(counter.Name, counter.Type)
        for parameter in self._search_parameters:
            if parameter['Field'] == full_name:
                if remove_old:
                    parameter['Field'] = []
                for val in value:
                    if val not in parameter['Value']:
                        parameter['Value'].append(val)
                return True
        self._search_parameters.append({
            'Type': SearchType.CONDITIONAL_QUERY,
            'Field': full_name,
            'Value': value
        })
        self._counters_up_to_date = False
        return True

    def add_search_content_type(self, data_type: Union[SearchDataType, List[SearchDataType]], remove_old: bool = False) -> bool:
        if type(data_type) is not List:
            data_type = [data_type]  # type: ignore
        search_l = []
        for d_type in data_type:
            search_l.append(d_type.value[0])
        return self.add_search_parameter('ContentType', search_l, remove_old=remove_old)

    def add_search_parameter_range(self, name: str, minv: float, maxv: float, dtype: DataType = DataType.NO_TYPE, max_included: bool = True,
                                   min_included: bool = True, remove_old: bool = False) -> bool:
        self._update_search_names_and_counters()
        counter = None
        for c in self._counters.Counters:
            if c.Name == name and c.Type == dtype:
                counter = c
                break
        if counter is None:
            return False
        if remove_old:
            self.remove_search_parameter(name, dtype)
        full_name = self._get_index_name_from_name_and_type(counter.Name, counter.Type)
        for parameter_i in range(len(self._search_parameters)):
            parameter = self._search_parameters[parameter_i]
            if parameter['Field'] == full_name:
                self._search_parameters.pop(parameter_i)
                break

        self._search_parameters.append({
            'Type': SearchType.CONDITIONAL_RANGE_QUERY,
            'Field': full_name,
            'Min': minv,
            'Max': maxv,
            'MinInc': min_included,
            'MaxInc': max_included
        })
        self._counters_up_to_date = False
        return True

    def set_search_wildcard(self, wildcard: Optional[str]) -> bool:
        param = None
        for parameter_i in range(len(self._search_parameters)):
            parameter = self._search_parameters[parameter_i]
            if parameter['Type'] == SearchType.CONDITIONAL_WILDCARD:
                if wildcard is None:
                    self._search_parameters.pop(parameter_i)
                    return True
                param = parameter
        if wildcard is None:
            return True
        if param is None:
            param = {
                'Type': SearchType.CONDITIONAL_WILDCARD,
                'Field': []
            }
            self._search_parameters.append(param)
        param['Value'] = wildcard
        return True

    def remove_search_parameter(self, name: str, dtype: DataType = DataType.NO_TYPE) -> bool:
        counter = None
        for c in self._counters.Counters:
            if c.Name == name and c.Type == dtype:
                counter = c
                break
        if counter is None:
            return False
        full_name = self._get_index_name_from_name_and_type(counter.Name, counter.Type)
        for i in range(len(self._search_parameters)):
            if self._search_parameters[i]['Field'] == full_name:
                self._search_parameters.pop(i)
                return True
        return False

    def get_current_count(self) -> int:
        self._update_search_names_and_counters()
        return self._counters.TotalCount

    def get_all_search_names_and_type(self) -> List[Tuple[str, DataType]]:
        l: List[Tuple[str, DataType]] = []
        for c in self._counters.Counters:
            l.append((c.Name, c.Type))
        return l

    def get_all_search_names(self) -> List[str]:
        l: List[str] = []
        for c in self._counters.Counters:
            l.append(c.Name)
        return l

    def get_all_search_names_and_type_without_unusefull(self) -> List[Tuple[str, DataType]]:
        l: List[Tuple[str, DataType]] = []
        for c in self._counters.Counters:
            if len(c.Values) == 1:
                if c.Values.values()[0] == c.Count:  # type: ignore
                    l.append((c.Name, c.Type))
        return l

    def get_all_search_names_and_type_without_usefull(self) -> List[Tuple[str, DataType]]:
        l: List[Tuple[str, DataType]] = []
        for c in self._counters.Counters:
            if len(c.Values) > 1:
                l.append((c.Name, c.Type))
        return l

    def get_results(self, max_amount: int = 500) -> List[SearchDataBase]:
        if max_amount <= 0 or max_amount > 10000:
            max_amount = 10000
        converting = True
        results: List[SearchDataBase] = []
        while converting:
            raw_results = self._searcher.get_search_interface(self, len(results), min(10000, max_amount - len(results)))  # type: ignore
            if 'Documents' not in raw_results:
                return []
            for item in raw_results['Documents']:
                fields = item['Fields']

                part: SearchDataBase = SearchDataBase(self._altium_api)
                for field1 in fields:
                    raw_name = field1['Name']
                    value = field1['Value']
                    name, _ = self._get_facet_name_and_type(raw_name)
                    if name == 'ContentType':
                        part = SearchDataType.get_from_str(SearchDataType.NO_TYPE, value).value[1](self._altium_api)
                        break

                for field1 in fields:
                    raw_name = field1['Name']
                    value = field1['Value']
                    name, _ = self._get_facet_name_and_type(raw_name)

                    if name == 'ContentType':
                        continue

                    m = re.search(r'\d+$', name)
                    if m is not None:
                        sub_name = name[:-len(m.group())]
                        if hasattr(part, sub_name):
                            if type(getattr(part, sub_name)) == list:
                                li = getattr(part, sub_name)
                                index = int(m.group())
                                while len(li) < index:
                                    li.append("")
                                li[index - 1] = value
                                continue
                    if hasattr(part, name):
                        if type(getattr(part, name)) == datetime:
                            if value.replace('.', '', 1).isdecimal():
                                d = datetime(1899, 12, 31)
                                setattr(part, name, d + timedelta(days=float(value)))
                            else:
                                setattr(part, name, datetime.strptime(value, "%m/%d/%Y %H:%M:%S"))
                        elif type(getattr(part, name)) == int:
                            setattr(part, name, int(value))
                        elif type(getattr(part, name)) == bool:
                            setattr(part, name, int(value) > 0)
                        else:
                            setattr(part, name, value)
                        continue
                    part.Parameters[name] = value

                results.append(part)

            if len(results) == min(max_amount, raw_results['Total']):
                converting = False
        return results

    def _update_search_names_and_counters(self) -> None:
        if not self._counters_up_to_date:
            temp_counters = self._searcher.get_part_counters(self)  # type: ignore
            new_counters = Counters()
            new_counters.Counters.extend(not_counted_search_parameters)
            try:
                new_counters.TotalCount = temp_counters['Total']
                temp_counter = temp_counters['FacetedCounters']
                if type(temp_counter) is not list:
                    temp_counter = [temp_counter]
                for temp_c in temp_counter:
                    if 'SupportRange' in temp_c:
                        n_counter = CounterRange()
                        n_counter.MaxValue = float(temp_c['MaxValue'])
                        n_counter.MinValue = float(temp_c['MinValue'])
                    else:
                        n_counter = Counter()  # type: ignore
                    n_counter.Name, n_counter.Type = self._get_facet_name_and_type(temp_c['FacetName'])
                    if n_counter.Name.endswith('_T@x^'):
                        continue
                    n_counter.Count = temp_c['TotalHitCount']
                    for temp_cv in temp_c['Counters']:
                        if 'SupportRange' in temp_c:
                            val = float(temp_cv['Value'])
                        else:
                            val = temp_cv['Value']
                        n_counter.Values[val] = temp_cv['Count']
                    new_counters.Counters.append(n_counter)
                self._counters = new_counters
                self._counters_up_to_date = True
            except Exception:
                print("Data error")

    def _get_facet_name_and_type(self, indexed_name: str) -> Tuple[str, DataType]:
        m1 = re.match("^(.*)_5F([0-9A-F]{8}_[0-9A-F]{6}_[0-9A-F]{6}_[0-9A-F]{6}_[0-9A-F]{46})$", indexed_name)
        m2 = re.match("^(.*)([0-9A-F]{32})$", indexed_name)
        if m1 is not None:
            name = m1.group(1)
            index = m1.group(2)
        elif m2 is not None:
            name = m2.group(1)
            index = m2.group(2)
        else:
            name = indexed_name
            index = ""
        dtype = DataType(index)
        name = self._decode_naming_chars(name)
        return name, dtype

    def _get_index_name_from_name_and_type(self, name: str, dtype: DataType) -> str:
        if dtype == DataType.NO_TYPE:
            full_name = self._encode_naming_chars(name)
            full_name += "DD420E8DDD8B445E911A0601BB2B6D53"
        else:
            full_name = self._encode_naming_chars(name)
            full_name += "_5F" + dtype.value
        return full_name

    def _decode_naming_chars(self, inp: str) -> str:
        for key, val in encoding_decoding_naming.items():
            inp = inp.replace(key, val)
        return inp

    def _encode_naming_chars(self, inp: str) -> str:
        for key, val in encoding_decoding_naming.items():
            inp = inp.replace(val, key)
        return inp
