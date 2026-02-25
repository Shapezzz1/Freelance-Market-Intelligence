import os
import time
import logging
from functools import wraps
from bs4 import BeautifulSoup

# Imports de Selenium organizados al inicio
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 1. Configuración Profesional de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 2. Decorador de Reintentos (Robustez de red)
def retry_on_failure(max_retries=3, delay=5):
    """
    Reintenta la ejecución de una función si lanza una excepción.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Intento {attempt + 1}/{max_retries} falló: {e}")
                    if attempt == max_retries - 1:
                        logger.error(f"Se alcanzó el límite de reintentos para {func.__name__}")
                        return None
                    time.sleep(delay)
        return wrapper
    return decorator

# 3. Función principal decorada
@retry_on_failure(max_retries=3, delay=5)
def get_html_with_selenium(url):
    edge_options = Options()
    
    # 4. Ruta Configurable vía Variables de Entorno
    # Si no existe la variable de entorno, usa el default de Windows
    default_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    binary_path = os.getenv('EDGE_BINARY_PATH', default_path)
    
    if os.path.exists(binary_path):
        edge_options.binary_location = binary_path
    else:
        logger.info("Binary no encontrado en ruta específica. Delegando a Selenium Manager.")
    
    # Argumentos de Evasión y Rendimiento
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    # edge_options.add_argument("--headless") # <-- Descomentar para ejecutar en background
    
    driver = None
    try:
        logger.info(f"Navegando a: {url}")
        driver = webdriver.Edge(options=edge_options)
        driver.get(url)

        # Espera explícita
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "project-title")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        logger.info("HTML renderizado y extraído exitosamente.")
        return soup

    finally:
        # 5. Cierre seguro garantizado
        if driver:
            driver.quit()