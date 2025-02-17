import os
from dotenv import load_dotenv  # type: ignore

from py_altium365.altium_api import AltiumApi


def test_user_login_correct():
    api = AltiumApi()
    load_dotenv()
    test_user = os.environ.get("ALTIUM_USER")
    test_pass = os.environ.get("ALTIUM_PASS")
    assert api.login(test_user, test_pass)


def test_user_login_incorrect():
    api = AltiumApi()
    test_user = "test"
    test_pass = "test"
    assert not api.login(test_user, test_pass)
