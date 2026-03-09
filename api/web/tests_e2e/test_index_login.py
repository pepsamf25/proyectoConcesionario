def test_index_login_page(driver, app_url):
    driver.get(f"{app_url}")
    assert "Aplicación de Concesionario" in driver.title
    driver.find_element(By.ID, "username")
    driver.find_element(By.ID, "password")
    assert not driver.find_element(By.CSS_SELECTOR, "label.error").is_displayed()
