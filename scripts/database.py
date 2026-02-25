import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

# 1. Configurabilidad: Permite cambiar la DB según el entorno (Dev/Prod)
DB_PATH = os.getenv('DB_PATH', 'market_intelligence.db')

def init_db():
    """Inicializa la base de datos, tablas e índices."""
    try:
        # 2. Context Manager: Maneja el commit/rollback automáticamente
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # 3. Esquema enriquecido (alineado con parser.py)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_market (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE, 
                    budget TEXT,
                    skills TEXT,
                    published_date TEXT,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 4. Índices para optimizar consultas futuras en Power BI o Pandas
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_extracted_at ON job_market(extracted_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_skills ON job_market(skills)')
            
            logger.info(f"Base de datos lista en: {DB_PATH}")
            
    except sqlite3.OperationalError as e:
        logger.error(f"Error operativo en BD (¿Lockeada?): {e}")
    except Exception as e:
        logger.critical(f"Error fatal inicializando la base de datos: {e}")

def save_jobs(jobs):
    """Guarda una lista de diccionarios en la base de datos."""
    if not jobs:
        logger.warning("No se recibieron datos para guardar.")
        return

    try:
        # Context Manager para la transacción
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            query = """
                INSERT OR IGNORE INTO job_market 
                (title, budget, skills, published_date) 
                VALUES (?, ?, ?, ?)
            """
            
            # Transformamos los diccionarios en tuplas de forma segura
            values = [
                (j.get('title'), j.get('budget'), j.get('skills'), j.get('published_date')) 
                for j in jobs
            ]
            
            # executemany es infinitamente más rápido que un bucle for
            cursor.executemany(query, values)
            
            logger.info(f"Transacción completada: Se procesaron {len(jobs)} registros.")
            
    except sqlite3.Error as e:
        # 5. Manejo de errores específicos de SQL
        logger.error(f"Fallo al ejecutar la inserción SQL: {e}")