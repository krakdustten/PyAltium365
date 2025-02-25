# type: ignore
import os

from dotenv import load_dotenv

from py_altium365.altium_api import AltiumApi
from py_altium365.base.enums import PrtGlobalService


load_dotenv()

api = AltiumApi()
print(api.login(os.environ.get("ALTIUM_USER"), os.environ.get("ALTIUM_PASS")))
print(api.get_service_url(PrtGlobalService.WORKSPACE))
ws = api.get_user_workspaces()
cws = api.login_workspace(ws[1], os.environ.get("ALTIUM_USER"), os.environ.get("ALTIUM_PASS"))
print(cws.create_search_object())
