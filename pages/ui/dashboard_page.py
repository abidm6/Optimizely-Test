from selenium.webdriver.common.by import By
from pages.ui.base_page import BasePage
from resources.data import Data


class DashboardPage(BasePage):
    CONTENT_MANAGER_TITLE = (By.XPATH, "//a[text()='Content Manager']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.data = Data()
