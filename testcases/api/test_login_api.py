import requests
import json
import pytest
from testcases.api.base_test import BaseTest
from pages.api.authentication_api_page import AuthenticationApiPage
from resources.data import Data
from jsonschema import validate

class TestLoginApi(BaseTest):
    def setup_class(self):
        self.login_api = AuthenticationApiPage()
        self.data = Data()
        self.url = self.login_api.login_base_url

    @pytest.mark.api
    def test_login_success(self):
        payload = self.login_api.create_auth_payload(self.data.user_email, self.data.user_password)

        response = requests.post(self.url, json=payload)

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
        data = response.json()
        
        assert "token" in data and isinstance(data["token"], str) and data["token"], "Token missing or empty"
        assert data.get("email") == payload["email"], "Returned email does not match"
        assert data.get("fullName"), "User name missing in response"
        assert "id" in data, "Login response does not contain id"
        assert data.get("type") == "Bearer", f"Expected token type 'Bearer', got {data.get('type')}"
        assert data.get("role") == "ROLE_USER", "Role mismatch"

    @pytest.mark.api
    def test_login_schema_from_file(self):
        with open("resources/schema/login_response_schema.json") as f:
            schema = json.load(f)

        payload = self.login_api.create_auth_payload(self.data.user_email, self.data.user_password)

        response = requests.post(self.url, json=payload)
        assert response.status_code == 200

        response_data = response.json()
        validate(instance=response_data, schema=schema)