import datetime as dt
import pathlib
from typing import Generic, TypeVar, Optional

from pydantic import HttpUrl

from pydantic_xml import BaseXmlModel, element

AuthType = TypeVar('AuthType')


class SoapHeader(
    BaseXmlModel,
    tag='Header',
    ns='soap',
):
    pass


class SoapMethod(BaseXmlModel):
    pass


MethodType = TypeVar('MethodType', bound=SoapMethod)


class SoapBody(
    BaseXmlModel, Generic[MethodType],
    tag='Body',
    ns='soap',
):
    method: MethodType


HeaderType = TypeVar('HeaderType', bound=SoapHeader)
BodyType = TypeVar('BodyType', bound=SoapBody)


class SoapEnvelope(
    BaseXmlModel,
    Generic[HeaderType, BodyType],
    tag='Envelope',
    ns='soap',
    nsmap={
        'soap': 'http://www.w3.org/2003/05/soap-envelope/',
    },
):
    header: Optional[HeaderType] = element(default=None)
    body: BodyType


class LoginResult(
    BaseXmlModel,
    tag='LoginResult',
    ns='',
    nsmap={'i': 'http://www.w3.org/2001/XMLSchema-instance'}
):
    success: str = element(tag='Success', nsmap={'': 'https://www.company.com/co'})


LoginResultType = TypeVar('LoginResultType', bound=LoginResult)


class SoapLoginResponse(
    SoapMethod,
    Generic[LoginResultType],
    tag='LoginResponse',
    ns='',
    nsmap={
        '': 'https://www.company.com/co',
    },
):
    login_result: LoginResultType


CreateCompanyRequest = SoapEnvelope[
    SoapHeader,
    SoapBody[
        SoapLoginResponse[
            LoginResult
        ]
    ],
]

xml_doc = pathlib.Path('./test.xml').read_text()

request = CreateCompanyRequest.from_xml(xml_doc)

print(request)