import logging

logger = logging.getLogger(__name__)

def safe_extract(element, selector, attribute=None, default="N/A"):
    # ... (Esta función se mantiene exactamente igual que la versión anterior) ...
    try:
        target = element.select_one(selector)
        if not target:
            return default
        if attribute:
            return target.get(attribute, default).strip()
        return target.get_text(separator=" ", strip=True)
    except Exception as e:
        logger.debug(f"Error extrayendo {selector}: {e}")
        return default

def is_recent(date_str):
    """
    Filtro lógico para descartar ofertas mayores a 1 mes.
    """
    date_lower = date_str.lower()
    # Si contiene "año", "años" o "meses" en plural, es mayor a 1 mes.
    if "año" in date_lower or "meses" in date_lower:
        return False
    # Permite "horas", "días", "semanas" y "un mes" / "1 mes"
    return True

def parse_jobs(soup):
    jobs = []
    
    projects = soup.select('.project-item')
    if not projects:
        projects = soup.select('h3.project-title')
        
    logger.info(f"Se encontraron {len(projects)} tarjetas de trabajo para procesar.")

    for project in projects:
        title = safe_extract(project, '.project-title')
        
        if title == "N/A":
            continue 
            
        budget = safe_extract(project, '.values', default="Negotiable")
        date_published = safe_extract(project, '.date', default="Unknown")
        
        # 🛡️ NUEVO: Aplicamos el filtro de antigüedad
        if not is_recent(date_published):
            # logger.debug(f"Descartado por antigüedad: {title[:30]}... ({date_published})")
            continue # Salta a la siguiente iteración del bucle, ignorando este trabajo
        
        try:
            skill_elements = project.select('.skills-wrapper label, .skills a, .skill')
            skills_list = [s.get_text(strip=True) for s in skill_elements]
            skills_str = ", ".join(skills_list) if skills_list else "Not specified"
        except Exception as e:
            logger.debug(f"Error extrayendo skills para '{title}': {e}")
            skills_str = "Not specified"

        jobs.append({
            "title": title,
            "budget": budget,
            "skills": skills_str,
            "published_date": date_published
        })
        
    return jobs