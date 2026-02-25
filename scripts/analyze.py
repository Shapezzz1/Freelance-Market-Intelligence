import sqlite3
import pandas as pd

def analyze_market_trends():
    print("📊 Iniciando Análisis de Inteligencia de Mercado...\n")
    
    # 1. Conexión y carga de datos
    try:
        with sqlite3.connect('market_intelligence.db') as conn:
            # Leemos toda la tabla directamente a un DataFrame de Pandas
            df = pd.read_sql_query("SELECT * FROM job_market", conn)
    except Exception as e:
        print(f"❌ Error conectando a la BD: {e}")
        return

    if df.empty:
        print("⚠️ La base de datos está vacía. Ejecuta main.py primero.")
        return

    print(f"✅ Analizando un total de {len(df)} ofertas de trabajo en el mercado.\n")

    # 2. Análisis de Skills (NLP Básico)
    if 'skills' in df.columns:
        # Lógica: Las skills están como "Python, SQL, Excel". 
        # Las separamos por coma, explotamos la lista en filas y quitamos espacios.
        all_skills = df['skills'].dropna().str.split(',').explode().str.strip()
        
        # Filtramos los valores nulos o no especificados
        all_skills = all_skills[~all_skills.isin(['Not specified', '', 'None'])]
        
        # Contamos las frecuencias
        top_skills = all_skills.value_counts().head(10)
        
        print("🔥 TOP 10 HABILIDADES MÁS DEMANDADAS (Frecuencia de aparición):")
        print("-" * 50)
        for skill, count in top_skills.items():
            print(f"  {count} veces | {skill.upper()}")
        print("-" * 50)
    else:
        print("⚠️ La columna 'skills' no existe en la base de datos.")

    # 3. Guardar un reporte limpio para Power BI
    # Guardamos los datos limpios en un CSV por si queremos usarlos en otra herramienta
    report_name = 'cleaned_market_data.csv'
    df.to_csv(report_name, index=False)
    print(f"\n💾 Reporte completo exportado a '{report_name}' para visualización avanzada.")

if __name__ == "__main__":
    analyze_market_trends()