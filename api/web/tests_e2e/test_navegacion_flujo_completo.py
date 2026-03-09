def test_full_user_flow(driver):
    # 1. Login page → Ver comentarios
    driver.get(f"{APP_URL}")
    ver_comentarios = driver.find_element(By.XPATH, "//button[contains(., 'Ver comentarios')]")
    ver_comentarios.click()
    assert "comentarios.html" in driver.current_url
    
    # 2. Desde comentarios, navegar a coches (asumiendo enlace en navbar)
    driver.get(f"{APP_URL}coches.html")
    assert "Visualizar coches" in driver.title
    
    # 3. Desde coches, ir a agregar coche
    agregar = driver.find_element(By.ID, "enlaceAgregar")
    agregar.click()
    assert "agregar_coche.html" in driver.current_url
    
    # 4. Volver a coches funciona
    volver = driver.find_element(By.XPATH, "//a[contains(., 'Volver')]")
    volver.click()
    assert "coches.html" in driver.current_url
