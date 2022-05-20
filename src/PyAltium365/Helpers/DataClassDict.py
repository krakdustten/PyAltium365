import re

from dataclasses import MISSING, Field
from datetime import datetime
from typing import Dict, no_type_check


@no_type_check
def _convert_data_to_type(self, input, to_type, cnv_str='%Y-%m-%dT%H:%M:%S'):
    if type(cnv_str) is tuple:
        try:
            m = re.match(cnv_str[0], input)
            input = m.group(1)
        except Exception:
            pass
        cnv_str = cnv_str[1]

    if type(input) is to_type:
        return input
    if type(input) is str:
        if to_type is bool:
            if input.lower() in ('1', 't', 'true', 'y', 'yes'):
                return True
            return False
        if to_type is int:
            return int(input)
        if to_type is float:
            return float(input)
        if to_type is datetime:
            return datetime.strptime(input, cnv_str)
    if type(input) is bool or type(input) is int or type(input) is float:
        if to_type is str:
            return str(input)
    if type(input) is datetime:
        if to_type is str:
            return input.strftime(cnv_str)
    return input


@no_type_check
def _to_dict(self, items: Dict[str, str], to_str: str = False) -> None:
    return None


@no_type_check
def _from_dict(self, items: Dict[str, str]) -> None:
    return None


@no_type_check
def _process_classdict(cls, to_dict, from_dict, check_parameter_sub_list):
    setattr(cls, 'from_dict', None)

    cls_fields = _get_all_fields(cls)
    _gen_to_dict_function(cls, cls_fields)
    _gen_from_dict_function(cls, cls_fields, check_parameter_sub_list)

    setattr(cls, "_convert_data_to_type", _convert_data_to_type)
    if not hasattr(cls, "_to_dict"):
        setattr(cls, "_to_dict", _to_dict)
    if not hasattr(cls, "_from_dict"):
        setattr(cls, "_from_dict", _from_dict)
    return cls


@no_type_check
def dataclassdict(cls=None, /, *, to_dict=True, from_dict=True, check_parameter_sub_list=()):
    def wrap(cls):
        return _process_classdict(cls, to_dict, from_dict, check_parameter_sub_list)

    if cls is None:
        return wrap

    return wrap(cls)


@no_type_check
def _get_all_fields(cls):
    cls_annotations = cls.__dict__.get('__annotations__', {})

    cls_fields = []
    for name, type in cls_annotations.items():
        field = getattr(cls, name, MISSING)
        if isinstance(field, FieldDict):
            field.name = name
            field.type = type
            cls_fields.append(field)

    for base in cls.__bases__:
        if base is not object.__class__:
            cls_fields += _get_all_fields(base)
    return cls_fields


@no_type_check
def _gen_to_dict_function(cls, cls_fields):
    name = 'to_dict'
    args = 'self, to_str=False'
    body = '  items = {}\n'
    for base in cls.__bases__:
        if base is not object:
            body += f'  from {base.__module__} import {base.__name__}\n'
            body += f'  sub = {base.__name__}.to_dict(self, to_str)\n'
            body += '  if sub is not None:\n'
            body += '    items.update(sub)\n'
    for field in cls_fields:
        dict_name = field.dict_name
        if dict_name is None:
            continue
        if isinstance(dict_name, list) or isinstance(dict_name, tuple):
            if len(dict_name) <= 0:
                continue
            dict_name = dict_name[0]
        if not isinstance(dict_name, str):
            continue
        body += '  if to_str:\n'
        if field.dict_conv_str is None:
            body += f'   items[\'{dict_name}\'] = _convert_data_to_type(self.{field.name}, str)\n'
        elif type(field.dict_conv_str) is tuple:
            body += f'   items[\'{dict_name}\'] = _convert_data_to_type(self.{field.name}, str, {field.dict_conv_str})\n'
        else:
            body += f'   items[\'{dict_name}\'] = _convert_data_to_type(self.{field.name}, str, "{field.dict_conv_str}")\n'
        body += '  else:\n'
        body += f'   items[\'{dict_name}\'] = self.{field.name}\n'
    body += '  self._to_dict(items, to_str)\n'
    body += '  return items'
    return_annotation = ''

    # Compute the text of the entire function.
    txt = f' def {name}({args}){return_annotation}:\n{body}'
    txt = f"def __create_fn__():\n{txt}\n return {name}"

    ns = {}
    exec(txt, None, ns)
    function = ns['__create_fn__']()

    setattr(cls, name, function)


@no_type_check
def _gen_from_dict_function(cls, cls_fields, check_parameter_sub_list=()):
    f_name = 'from_dict'
    args = 'self, items:dict'
    body = ''
    for base in cls.__bases__:
        if base is not object:
            body += f'  from {base.__module__} import {base.__name__}\n'
            body += f'  {base.__name__}.from_dict(self, items)\n'
    for field in cls_fields:
        dict_name = field.dict_name
        if dict_name is None:
            continue
        if isinstance(dict_name, list) or isinstance(dict_name, tuple):
            if len(dict_name) <= 0:
                continue
            if not isinstance(dict_name[0], str):
                continue
        elif isinstance(dict_name, str):
            dict_name = [dict_name]
        else:
            continue

        for d_name in dict_name:
            body += f'  if \'{d_name}\' in items:\n'
            if field.dict_conv_str is None:
                body += f'   self.{field.name} = self._convert_data_to_type(items[\'{d_name}\'], {field.type.__name__})\n'
            elif type(field.dict_conv_str) is tuple:
                body += f'   self.{field.name} = self._convert_data_to_type(items[\'{d_name}\'], {field.type.__name__}, {field.dict_conv_str})\n'
            else:
                body += f'   self.{field.name} = self._convert_data_to_type(items[\'{d_name}\'], {field.type.__name__}, "{field.dict_conv_str}")\n'

    if len(check_parameter_sub_list) == 3:
        path, name, value = check_parameter_sub_list
        if type(path) is str:
            path = [path]
        if len(path) > 0:
            i = 0
            sp = "  "
            for p in path:
                body += f'{sp}if \'{p}\' in items{"" if i == 0 else i}:\n'
                sp += " "
                body += f'{sp}items{i + 1} = items{"" if i == 0 else i}["{p}"]\n'
                i += 1
            body += f'{sp}if type(items{i}) is list:\n'
            body += f'{sp} item_sl = items{i}\n'
            body += f'{sp}else:\n'
            body += f'{sp} item_sl = [items{i}]\n'
            body += f'{sp}for item in item_sl:\n'
            sp += " "
        for field in cls_fields:
            dict_name = field.dict_name
            if dict_name is None:
                continue
            if isinstance(dict_name, list) or isinstance(dict_name, tuple):
                if len(dict_name) <= 0:
                    continue
                if not isinstance(dict_name[0], str):
                    continue
            elif isinstance(dict_name, str):
                dict_name = [dict_name]
            else:
                continue

            for d_name in dict_name:
                body += f'{sp}if \'{name}\' in item and \'{value}\' in item:\n'
                body += f'{sp} if item[\'{name}\'] == "{d_name}":\n'
                if field.dict_conv_str is None:
                    body += f'{sp}  self.{field.name} = self._convert_data_to_type(item[\'{value}\'], {field.type.__name__})\n'
                elif type(field.dict_conv_str) is tuple:
                    body += f'{sp}  self.{field.name} = self._convert_data_to_type(item[\'{value}\'], {field.type.__name__}, {field.dict_conv_str})\n'
                else:
                    body += f'{sp}  self.{field.name} = self._convert_data_to_type(item[\'{value}\'], {field.type.__name__}, "{field.dict_conv_str}")\n'

    body += '  self._from_dict(items)\n'
    body += '  return self'
    return_annotation = ''

    # Compute the text of the entire function.
    txt = f' def {f_name}({args}){return_annotation}:\n{body}'
    txt = f"def __create_fn__():\n{txt}\n return {f_name}"

    ns = {}
    exec(txt, None, ns)
    function = ns['__create_fn__']()

    setattr(cls, f_name, function)


class FieldDict(Field):
    __slots__ = ('dict_name', 'dict_conv_str')

    @no_type_check
    def __init__(self, dict_name, dict_conv_str, default, default_factory, init, repr, hash, compare, metadata):
        super().__init__(default, default_factory, init, repr, hash, compare, metadata)
        self.dict_name = dict_name
        self.dict_conv_str = dict_conv_str

    @no_type_check
    def __repr__(self) -> str:
        return ('Field('
                f'name={self.name!r},'
                f'type={self.type!r},'
                f'dict_name={self.dict_name!r},'
                f'dict_conv_str={self.dict_conv_str!r},'
                f'default={self.default!r},'
                f'default_factory={self.default_factory!r},'
                f'init={self.init!r},'
                f'repr={self.repr!r},'
                f'hash={self.hash!r},'
                f'compare={self.compare!r},'
                f'metadata={self.metadata!r},'
                f'_field_type={self._field_type}'
                ')')


@no_type_check
def field_dict(*, dict_name=(), dict_conv_str=None, default=MISSING,
               default_factory=MISSING, init=True, repr=True, hash=None,
               compare=True, metadata=None):
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('cannot specify both default and default_factory')
    return FieldDict(dict_name, dict_conv_str, default, default_factory, init, repr, hash, compare, metadata)
