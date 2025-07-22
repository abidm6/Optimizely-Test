import os
import sys
import pytest
from selenium import webdriver
from utils.app_constants import AppConstant
from utils.config_parser import ConfigParser


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    url = config.getoption('--url')
    browser = config.getoption('--browser')

    configs = ConfigParser()

    configs.add_file(AppConstant.SYSTEM_CONFIG)
    configs.load_configs()

    if url is not None:
        configs.set_config('url', url)


    #   Other settings is cached here
    pytest.configs = configs
    pytest.url = configs.get_config('url')
    pytest.browser = browser
    pytest.browser_version = config.getoption("browser_version")

def get_driver():
    """
    Initialize driver & yield it to currently running test suite. If any suite uses @pytest.mark.no_auto
    mark then no driver will be returned.
    """
    driver = get_requested_browser(pytest.browser)
    driver.get(pytest.url)

    browser_version = driver.capabilities['browserVersion']
    os.environ['browser_version'] = browser_version
    print('browser opened')
    return driver


def get_requested_browser(requested_browser_name='chrome'):
    if requested_browser_name == 'chrome':
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--use-fake-device-for-media-stream')
        chrome_options.add_argument('--use-fake-ui-for.media-stream')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()), options=chrome_options)

    elif requested_browser_name == 'debugging':
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()
        options.add_experimental_option('debuggerAddress', 'localhost:9222')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    else:
        print('Invalid browser type. Please try with Chrome or Firefox.')
        sys.exit()

    driver.maximize_window()

    return driver


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='dev',
                     help='env: dev, staging or prod/live')
    parser.addoption('--url', action='store', help='url: dev, staging or production url. If it is provided,'
                                                   'this value will override the value provided by config file.')
    parser.addoption('--browser', action='store', default='chrome',
                     help='browser: chrome/firefox/hc/headless-chrome. Used for browser selection,')
    parser.addoption('--browser-version', action='store',
                     help='browser-version: 116/117/118/119/120. Used for selecting '
                          'chrome browser version to execute test cases.')

