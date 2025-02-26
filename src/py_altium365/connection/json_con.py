from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from requests import Session


class JsonRequest(BaseModel):
    """Base class for SOAP method."""


RequestT = TypeVar("RequestT", bound=JsonRequest)


class JsonBase(BaseModel, Generic[RequestT]):
    """Base class for JSON method."""

    request: RequestT


class JsonReturn(BaseModel):
    """Base class for JSON return."""


class JsonCon:
    """Base class for JSON connection."""

    def __init__(self, session: Session, url: str, session_guid: str, host: str):
        """
        Initialize the JsonCon object
        :param session: The main connection session
        :param url: The URL to send the JSON request to
        :param session_guid: The session GUID
        :param host: The host for the host parameter
        """
        self._session: Session = session
        self._url: str = url
        self._session_guid: str = session_guid
        self._host: str = host

    ReturnMethodT = TypeVar("ReturnMethodT", bound=JsonReturn)

    def _send_command(self, request: JsonRequest, return_method: Type[ReturnMethodT]) -> ReturnMethodT:
        headers = {
            "Accept": "application/json",
            "Authorization": f"AFSSessionID {self._session_guid}",
            "host": self._host,
            "content-type": "application/json; charset=utf-8",
            "User-Agent": "Altium Designer",
        }

        json_data = JsonBase(request=request).json(by_alias=True)

        response = self._session.request("REPORT", self._url, data=json_data, headers=headers)

        if response.status_code != 200:
            raise ConnectionError("Failed to send JSON command!")

        return return_method.parse_raw(response.content.decode("utf-8-sig"))
