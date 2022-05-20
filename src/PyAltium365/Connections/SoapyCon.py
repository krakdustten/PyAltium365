from typing import List, Dict, Union, Any, Optional, Tuple

from PyAltium365.Connections.ConnectionExceptions import InternalConnectionException, ElementItemNotFoundException
from PyAltium365.Exceptions import DataException
from PyAltium365.Helpers.DataConvHelper import convert_data_to_type
from requests import Session

import xml.etree.ElementTree as ET


class SoapyCon:
    def __init__(self, session: Session, url: str):
        self._session: Session = session
        self._url: str = url
        self._tag_buffer: List[str] = []

    def _send_command(self, soap_action: str, head: Optional[str], body: Optional[str], soap_action_body: str = None, body_xmlns: str = "http://tempuri.org/")\
            -> ET.Element:
        if soap_action_body is None:
            soap_action_body = soap_action

        headers = {
            'content-type': 'text/xml',
            'SOAPAction': soap_action,
            'User-Agent': "Altium Designer"
        }
        re = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">\n'
        if head is not None:
            re += '<soapenv:Header>\n'
            re += head
            re += '</soapenv:Header>\n'
        if body is not None:
            re += '<soapenv:Body>\n'
            re += f'<{soap_action_body} xmlns="{body_xmlns}">\n'
            re += body
            re += '</' + soap_action_body + '>\n'
            re += '</soapenv:Body>\n'
        re += '</soapenv:Envelope>\n'

        response = self._session.post(self._url, data=re, headers=headers)
        if response.status_code == 200:
            return ET.fromstring(response.text)
        raise InternalConnectionException()

    def _gen_generic_tag(self, name: str, value: Any = None, xmlns: str = None) -> str:
        if value is None:
            return f"<{name} />\n"
        if xmlns is None:
            return f"<{name}>{str(value)}</{name}>\n"
        return f"<{name} xmlns=\"{xmlns}\">{str(value)}</{name}>\n"

    def _gen_generic_tag_start(self, name: str, xmlns: str = None) -> str:
        self._tag_buffer.append(name)
        if xmlns is None:
            return f"<{name}>\n"
        return f"<{name} xmlns=\"{xmlns}\">\n"

    def _gen_generic_tag_end(self) -> str:
        if len(self._tag_buffer) == 0:
            return ""
        tag = self._tag_buffer.pop(len(self._tag_buffer) - 1)
        return f"</{tag}>\n"

    def _get_elm_by_name(self, et: ET.Element, cname: str, cleanname: bool = False, exceptions: bool = True)\
            -> Union[ET.Element, None]:
        for child in et:
            name = child.tag
            if cleanname:
                name = name.split('}')[-1]
            if name == cname:
                return child
        if exceptions:
            raise ElementItemNotFoundException()
        return None

    def _get_elm_by_path(self, et: ET.Element, pnames: List[str], cleanname: bool = False) -> ET.Element:
        sub = et
        for name in pnames:
            elm = self._get_elm_by_name(sub, name, cleanname, False)
            if isinstance(elm, ET.Element):
                sub = elm
            else:
                raise ElementItemNotFoundException()
        return sub

    def _convert_et_to_dict(self, et: ET.Element, cleanname: bool = False) -> Dict[str, Union[Dict, List, str]]:
        d = {}  # type: Dict[str, Union[Dict, List, str]]
        for child in et:
            name = child.tag
            if cleanname:
                name = name.split('}')[-1]
            if len(child) > 0:
                to_add = self._convert_et_to_dict(child, cleanname)  # type: Union[Dict, List[str], str]
            else:
                to_add = str(child.text)
            if name in d:
                value = d[name]
                if isinstance(value, list):
                    value.append(to_add)
                else:
                    d[name] = [value, to_add]
            else:
                d[name] = to_add
        return d

    def _check_method_result(self, et: ET.Element, pnames: List[str]) -> Tuple[str, bool]:
        et = self._get_elm_by_path(et, pnames, True)
        d = self._convert_et_to_dict(et, True)
        if "Success" not in d:
            raise ElementItemNotFoundException()
        if convert_data_to_type(d["Success"], bool) is False:
            raise DataException()
        message = ""
        more_data = False
        if "Message" in d:
            if d["Message"] is not None:
                message = d["Message"]  # type: ignore
        if "MoreDataAvailable" in d:
            more_data = convert_data_to_type(d["MoreDataAvailable"], bool)

        return message, more_data
