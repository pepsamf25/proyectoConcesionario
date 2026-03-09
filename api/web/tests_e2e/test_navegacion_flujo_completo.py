def test_full_user_flow(driver, app_url):
    driver.get(f"{app_url}")
    ver_comentarios = driver.find_element(By.XPATH, "//button[contains(., 'Ver comentarios')]")
    ver_comentarios.click()
    assert "comentarios.html" in driver.current_url
    
    driver.get(f"{app_url}coches.html")
    assert "Visualizar coches" in driver.title
    
    agregar = driver.find_element(By.ID, "enlaceAgregar")
    agregar.click()
    assert "agregar_coche.html" in driver.current_url
    
    volver = driver.find_element(By.XPATH, "//a[contains(., 'Volver')]")
    volver.click()
    assert "coches.html" in driver.current_url
