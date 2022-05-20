import json
from typing import List, Dict, Any, TYPE_CHECKING, Union
from requests import Session

if TYPE_CHECKING:
    from PyAltium365.AltiumApi import AltiumApi
else:
    from PyAltium365.Fix import AltiumApi


class JsonCon:
    def __init__(self, session: Session, url: str):
        self._session: Session = session
        self._url: str = url

    def _send_command(self, api: AltiumApi, data: Union[Dict[str, Any], List[Any]]) -> Dict[str, Any]:
        headers = {
            'Accept': 'application/json',
            'Authorization': f'AFSSessionID {api._seswork_guid}',
            'host': 'magics-instruments-nv.365.altium.com',
            'content-type': 'application/json; charset=utf-8',
            'User-Agent': "Altium Designer"
        }

        ret = self._session.request('REPORT', self._url, data='{"request":' + json.dumps(data, separators=(',', ':')) + '}', headers=headers)

        return json.loads(ret.content.decode('utf-8-sig'))  # type: ignore
