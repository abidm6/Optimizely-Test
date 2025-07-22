import pytest
from pages.api.base_page import BasePage
import json


class AuthenticationApiPage(BasePage):
    login_base_url = pytest.configs.get_config('login_base_url')

    def create_auth_payload(self, email_id: str, password: str):
        auth_body = {
            "email": email_id,
            "password": password,
            "rememberMe": True
        }

        return auth_body