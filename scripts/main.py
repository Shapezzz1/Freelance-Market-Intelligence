import argparse
import logging
import time
import random
import schedule

# Importamos nuestros módulos refactorizados
from scraper import get_html_with_selenium
from parser import parse_jobs
from database import init_db, save_jobs

# 1. Configuración unificada de Logging para el orquestador
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger("Orchestrator")

def run_pipeline(query, pages, langs):
    """Ejecuta el ciclo de vida completo de los datos."""
    logger.info(f"🚀 Iniciando Pipeline: Búsqueda='{query}', Idiomas='{langs}', Páginas={pages}")
    
    init_db() 
    
    total_jobs_found = 0
    formatted_query = query.replace(" ", "+")
    # Limpiamos los espacios por si el usuario escribe "es, en, pt"
    formatted_langs = langs.replace(" ", "") 
    
    for page in range(1, pages + 1):
        # Pausa ética (Rate-Limiting)
        sleep_time = random.uniform(3.0, 6.0)
        logger.info(f"⏳ Esperando {sleep_time:.1f}s (Rate-Limit)...")
        time.sleep(sleep_time)

        logger.info(f"📄 Procesando Página {page}/{pages}...")
        
        # 🧠 LA NUEVA URL: Le inyectamos el parámetro &language=
        url = f"https://www.workana.com/jobs?query={formatted_query}&language={formatted_langs}&page={page}"
        
        # Ingesta
        soup = get_html_with_selenium(url)
        
        if soup:
            # Transformación
            job_data = parse_jobs(soup)
            jobs_count = len(job_data)
            logger.info(f"✅ Se extrajeron {jobs_count} trabajos de la página {page}.")
            
            # Almacenamiento
            if jobs_count > 0:
                save_jobs(job_data)
                total_jobs_found += jobs_count
        else:
            logger.error(f"❌ Falló la carga de la página {page}. Saltando a la siguiente...")
        
        sleep_time = random.uniform(3.0, 7.0)
        logger.info(f"⏳ Esperando {sleep_time:.2f} segundos para no saturar el servidor (Rate-Limiting)...")
        time.sleep(sleep_time)
        
    logger.info(f"🏁 Pipeline Finalizado. Total de trabajos procesados/guardados: {total_jobs_found}")

# ... (Mantenemos job_scheduler igual, pero pasándole langs si lo usas) ...

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Freelance Market Intelligence Scraper")
    
    parser.add_argument("-q", "--query", type=str, default="data analysis", 
                        help="Término de búsqueda (ej. 'data science', 'python')")
    parser.add_argument("-p", "--pages", type=int, default=3, 
                        help="Cantidad de páginas a scrapear")
    
    # 🌟 NUEVO ARGUMENTO: Idiomas
    parser.add_argument("-l", "--langs", type=str, default="es,en,pt",
                        help="Idiomas separados por coma (ej. 'es,en,pt')")
                        
    parser.add_argument("-s", "--schedule", type=int, default=0,
                        help="Horas entre ejecuciones (0 = corre una vez y termina)")
    
    args = parser.parse_args()
    
    if args.schedule > 0:
        # Si usas el scheduler, asegúrate de actualizar la función para que reciba langs también
        job_scheduler(args.query, args.pages, args.langs, args.schedule)
    else:
        # Ejecución normal
        run_pipeline(args.query, args.pages, args.langs)