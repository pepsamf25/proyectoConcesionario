from selenium.webdriver.common.by import By

def test_agregar_coche_form(driver, app_url):
    driver.get(f"{app_url}agregar_coche.html")
    assert "Agregar coches" in driver.title
    
    # Verificar todos los campos del formulario
    driver.find_element(By.ID, "nombre")
    driver.find_element(By.ID, "descripcion")
    driver.find_element(By.ID, "precio")
    driver.find_element(By.ID, "foto")
    driver.find_element(By.ID, "filefoto")
    
    # Navbar navegación
    driver.find_element(By.XPATH, "//a[contains(., 'Coche')]")
    
    # Botones principales
    driver.find_element(By.XPATH, "//button[contains(., 'Guardar')]")
