import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

APP_URL = os.environ.get("APP_URL", "http://apache-waf:80/")

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
