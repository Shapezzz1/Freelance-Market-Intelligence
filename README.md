# Inteligencia de Mercado Freelance (Data Pipeline)

## De qué trata este proyecto
Básicamente, armé un pipeline de datos (ETL) automatizado de punta a punta para extraer, limpiar y analizar ofertas de trabajo reales en plataformas freelance. 

El problema que resuelve es la falta de visibilidad rápida sobre lo que pide el mercado. En lugar de entrar a mirar ofertas a mano, este script monitorea en tiempo real las tendencias, los presupuestos y las tecnologías más demandadas en el sector de datos. Es una herramienta de inteligencia comercial construida enteramente con código.

## Cómo funciona

El sistema tiene una arquitectura modular para que sea escalable y fácil de mantener:

1. Ingesta (Web Scraping): Las plataformas modernas bloquean los scrapers simples. Para solucionarlo, usé Selenium y WebDriver. Esto me permite sortear protecciones y renderizar el contenido dinámico en JavaScript para extraer el HTML real.
2. Transformación (Parser): Con BeautifulSoup4 proceso el DOM. Le metí programación defensiva (try-except) para que el script no se rompa si faltan etiquetas, y filtros lógicos para descartar basura (por ejemplo, ofertas que tienen más de un mes de antigüedad).
3. Almacenamiento (Base de Datos): Toda la info limpia va a una base SQLite3. Para mantener la integridad de los datos, armé restricciones lógicas (UNIQUE e INSERT OR IGNORE) que evitan guardar ofertas duplicadas, y sumé índices para que las consultas sean rápidas.
4. Orquestación: Armé una interfaz de línea de comandos (CLI) con Argparse. Esto permite pasarle parámetros al script (qué buscar, cuántas páginas, qué idiomas) directamente desde la terminal, y lo dejé preparado para correr en background con un Scheduler.
5. Análisis: Una vez que los datos están en la base, uso Pandas para conectarme mediante SQL, hacer un análisis de frecuencia sobre las habilidades requeridas y sacar métricas limpias.

## Stack Tecnológico

* Lenguaje: Python 3.x
* Extracción (Scraping): Selenium, BeautifulSoup4, Requests
* Base de Datos: SQLite3
* Análisis de Datos: Pandas
* Orquestación: Argparse, Schedule

## Cómo levantar el proyecto localmente

Si querés correr el pipeline en tu pc, seguí estos pasos:

1. Cloná el repositorio:
   git clone https://github.com/Shapezzz1/Freelance-Market-Intelligence.git
   cd Freelance-Market-Intelligence

2. Instalá las dependencias:
   pip install -r requirements.txt

3. Ejecutá el orquestador (CLI):
   Podés parametrizar la búsqueda. Por ejemplo, para buscar ofertas de "Data Analysis" en 5 páginas y en tres idiomas distintos (español, inglés y portugués):
   python main.py --query "data analysis" --pages 5 --langs "es,en,pt"

4. Generá el reporte analítico:
   python analyze.py
   (Esto lee la base de datos, te muestra en consola el Top 10 de habilidades más demandadas y te escupe un CSV limpio listo para meter en Power BI).
