import pytest


class BasePage:
    base_url = pytest.configs.get_config('base_url')