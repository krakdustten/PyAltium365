from typing import TypeVar, Dict, Union, Type

from PyAltium365.Exceptions import DataException
from PyAltium365.Helpers.DataConvHelper import convert_data_to_type

T = TypeVar('T')
U = TypeVar('U')
R = TypeVar('R')


def get_from_dict_and_check_type(input: Dict, name: str, check: Type[T]) -> T:
    if name in input:
        val = input[name]
        if type(val) is check:
            return val
    raise DataException()


def get_from_dict_and_check_type2(input: Dict, name: str, check1: Type[T], check2: Type[U]) -> Union[T, U]:
    if name in input:
        val = input[name]
        if type(val) is check1:
            return val
        if type(val) is check2:
            return val
    raise DataException()


def get_from_dict_and_check_type_r(input: Dict, name: str, check: Type[T], retdif: R) -> Union[T, R]:
    if name in input:
        val = input[name]
        if type(val) is check:
            return val
    return retdif


def get_from_dict_and_check_type2_r(input: Dict, name: str, check1: Type[T], check2: Type[U], retdif: R) -> Union[T, U, R]:
    if name in input:
        val = input[name]
        if type(val) is check1:
            return val
        if type(val) is check2:
            return val
    return retdif


def check_data_in_dict(input: Dict, name: str, check_type: Type[T], value: T) -> None:
    if name in input:
        v = convert_data_to_type(input[name], check_type)
        if v == value:
            return None
    raise DataException()
