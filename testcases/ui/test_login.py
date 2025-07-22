import allure
import pytest
from testcases.ui.base_test import BaseTest
from resources.data import Data
from pages.ui.login_page import LoginPage
from pages.ui.dashboard_page import DashboardPage
from conftest import get_driver
import time

class TestLogin(BaseTest):

    def setup_class(self):
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.data = Data()
    
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.sanity
    def test_login_with_valid_credentials(self):
        with allure.step("Enter valid email and password and verify user logs in"):
            self.login_page.wait_for_visibility_of(self.login_page.LOGIN_BUTTON, 10)
            self.login_page.enter_text_at(self.data.user_email,self.login_page.EMAIL_FIELD)
            assert self.login_page.get_attribute(self.login_page.EMAIL_FIELD,
                                                            'value') == self.data.user_email

            self.login_page.enter_text_at(self.data.user_password, self.login_page.PASSWORD_FIELD)
            assert self.login_page.get_attribute(self.login_page.PASSWORD_FIELD,
                                                    'value') == self.data.user_password
            self.login_page.click_and_wait_for_invisibility(self.login_page.LOGIN_BUTTON, 10)
            assert not self.login_page.is_element_visible(self.login_page.LOGIN_BUTTON, 2)
            assert self.login_page.is_element_visible(self.dashboard_page.CONTENT_MANAGER_TITLE, 5)
            