def test_coches_page(driver, app_url):
    driver.get(f"{app_url}coches.html")
    assert "Visualizar coches" in driver.title
    
    # Navbar con enlaces funcionales
    coches_link = driver.find_element(By.XPATH, "//a[contains(., 'Coches')]")
    archivos_link = driver.find_element(By.XPATH, "//a[contains(., 'Archivos')]")
    logout_link = driver.find_element(By.XPATH, "//a[contains(., 'Cerrar sesión')]")
    
    # Tabla coches (tbody vacío inicialmente está bien)
    table_tbody = driver.find_element(By.TAG_NAME, "tbody")
    assert table_tbody.tag_name == "tbody"
    
    # Botón Agregar
    agregar_btn = driver.find_element(By.ID, "enlaceAgregar")
    assert agregar_btn.get_attribute("href").endswith("agregar_coche.html")
