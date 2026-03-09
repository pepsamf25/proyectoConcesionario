import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def app_url():
    """URL de la app desde variable de entorno"""
    return os.environ.get("APP_URL", "http://apache-waf:80/")

@pytest.fixture(scope="function")
def driver(app_url):
    """Navegador Chrome headless con Selenium Manager"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
