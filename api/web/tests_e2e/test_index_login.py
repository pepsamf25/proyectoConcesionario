def test_index_login_page(driver):
    driver.get(f"{APP_URL}")
    assert "Aplicación de Concesionario" in driver.title
    driver.find_element(By.ID, "username")
    driver.find_element(By.ID, "password")
    assert not driver.find_element(By.CSS_SELECTOR, "label.error").is_displayed()
