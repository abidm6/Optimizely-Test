from selenium.webdriver.common.by import By
from pages.ui.base_page import BasePage
from resources.data import Data


class LoginPage(BasePage):
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Sign in']")
    EMAIL_FIELD = (By.XPATH, "//input[contains(@class, 'mantine-TextInput-input')]")
    PASSWORD_FIELD = (By.XPATH, "//input[contains(@class, 'mantine-PasswordInput-innerInput')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.data = Data()

    