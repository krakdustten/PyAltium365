from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from pydantic_xml import element, wrapped

from py_altium365.connection.soapy_con import SoapMethod, SoapResponse
from py_altium365.connection.vault.soapy_con_vault_base import SoapConVaultBase, SoapMethodOption, AluItem

if TYPE_CHECKING:
    from py_altium365.altium_api_workspace import AltiumApiWorkspace


class SoapMethodVaultGetAluItems(
    SoapMethod,
    tag="GetALU_Items",
    nsmap={"temp": "http://tempuri.org/"},
    ns="temp",
):
    session_handle: str = element(tag="SessionHandle")
    p_filter: Optional[str] = element(tag="Filter", default=None)
    options: List[SoapMethodOption] = wrapped(
        path="Options",
        entity=element(tag="item"),
        default=[],
    )


class SoapResponseVaultGetAluItems(
    SoapResponse,
    tag="GetALU_ItemsResponse",
    nsmap={"temp": "http://tempuri.org/"},
    ns="temp",
):
    records: List[AluItem] = wrapped(
        path="Records",
        tag="item",
        default=[],
    )


class SoapConVault(SoapConVaultBase):
    def __init__(self, altium_workspace: "AltiumApiWorkspace"):
        super().__init__(altium_workspace)

    def get_alu_items(self, p_filter: Optional[str] = None, options: List[SoapMethodOption] = None):
        if options is None:
            options = []
        response = self._send_command(
            header=None,
            method=SoapMethodVaultGetAluItems(
                session_handle=self._altium_workspace.session_guid,
                p_filter="GUID = 'ab3273c1-ae47-4e32-a683-47e6da10a920'",
                options=options
            ),
            return_method=SoapResponseVaultGetAluItems,
        )

        return response


