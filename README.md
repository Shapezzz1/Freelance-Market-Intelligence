# 🚀 Freelance Market Intelligence Pipeline

Un pipeline de datos (ETL) automatizado de extremo a extremo diseñado para extraer, limpiar y analizar ofertas de trabajo en plataformas freelance (SPA/Renderizado Dinámico). El objetivo de este proyecto es monitorear en tiempo real las tendencias del mercado, presupuestos y tecnologías más demandadas en el sector de los datos.

## 🧠 Arquitectura del Proyecto

El sistema está construido bajo una arquitectura modular para asegurar escalabilidad y fácil mantenimiento:

1. **Ingesta (Scraper):** Utiliza `Selenium` y `WebDriver` para sortear protecciones anti-bots y renderizar contenido dinámico en JavaScript, extrayendo el HTML crudo.
2. **Transformación (Parser):** `BeautifulSoup4` procesa el DOM aplicando programación defensiva (`try-except`) para manejar etiquetas faltantes. Implementa filtros lógicos para descartar ofertas obsoletas (ej. > 1 mes de antigüedad).
3. **Almacenamiento (Database):** Base de datos `SQLite3` transaccional (usando Context Managers). Implementa restricciones `UNIQUE` e `INSERT OR IGNORE` para evitar duplicados, junto con índices para optimizar futuras consultas.
4. **Orquestación (Main):** Interfaz de Línea de Comandos (CLI) construida con `argparse` que permite parametrizar búsquedas, páginas e idiomas, además de integrar un *Scheduler* para ejecuciones en background.
5. **Análisis (Analyze):** Integración directa entre SQL y `Pandas` para realizar análisis de frecuencia (NLP básico) sobre las habilidades requeridas.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.x
* **Extracción:** Selenium, BeautifulSoup4, Requests
* **Base de Datos:** SQLite3 (SQL Crudo)
* **Análisis de Datos:** Pandas
* **Orquestación:** Argparse, Schedule

## ⚙️ Instalación y Uso

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/Shapezzz1/Freelance-Market-Intelligence.git](https://github.com/Shapezzz1/Freelance-Market-Intelligence.git)
   cd Freelance-Market-Intelligence
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar el orquestador (CLI):
   Puedes personalizar la búsqueda usando argumentos. Ejemplo para buscar ofertas de "Data Analysis" en 5 páginas abarcando español, inglés y portugués:
   ```bash
   python main.py --query "data analysis" --pages 5 --langs "es,en,pt"
   ```

4. Generar el reporte de mercado:
   ```bash
   python analyze.py
   ```
   *Esto leerá la base de datos y mostrará en consola el Top 10 de habilidades más demandadas, exportando un archivo CSV limpio para su visualización en herramientas como Power BI.*

## 📈 Próximos Pasos (Roadmap)
- [ ] Conectar el archivo CSV/SQLite directamente a un dashboard de Power BI.
- [ ] Migrar de SQLite a PostgreSQL usando SQLAlchemy para despliegue en la nube.
- [ ] Implementar rotación de User-Agents y Proxies para mayor resiliencia.