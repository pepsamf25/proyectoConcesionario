def test_comentarios_page(driver, app_url):
    driver.get(f"{app_url}comentarios.html")
    assert "Comentarios" in driver.title
    driver.find_element(By.ID, "usuario")
    driver.find_element(By.ID, "descripcion")
    driver.find_element(By.XPATH, "//button[contains(., 'Guardar')]")