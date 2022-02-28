import re

from datetime import datetime
from typing import Any, TypeVar, Union, Tuple, no_type_check, Type

from PyAltium365.Exceptions import DataException

T = TypeVar('T')


@no_type_check
def convert_data_to_type(inp: Any, to_type: Type[T], cnv_str: Union[str, Tuple[str, str]] = '%Y-%m-%dT%H:%M:%S') -> T:
    if type(cnv_str) is tuple:
        try:
            m = re.match(cnv_str[0], inp)
            inp = m.group(1)
        except Exception:
            pass
        cnv_str2 = cnv_str[1]
    else:
        cnv_str2 = cnv_str

    if type(inp) is to_type:
        return inp
    if type(inp) is str:
        if to_type is bool:
            if inp.lower() in ('1', 't', 'true', 'y', 'yes'):
                return True
            return False
        if to_type is int:
            return int(inp)
        if to_type is float:
            return float(inp)
        if to_type is datetime:
            return datetime.strptime(inp, cnv_str2)
    if type(inp) is bool or type(inp) is int or type(inp) is float:
        if to_type is str:
            return str(inp)
    if type(inp) is datetime:
        if to_type is str:
            return str(inp.strftime(cnv_str2))
    raise DataException()
