import json
import os
import glob
import google.generativeai as genai
from motor_aprendizajes import cargar_aprendizajes

FICHERO_DATOS = "datos_saga.json"

def inicializar_datos():
    if not os.path.exists(FICHERO_DATOS):
        datos_iniciales = {
            "credenciales": {"gemini": "", "instagram": "", "tiktok": "", "twitter": ""},
            "personajes": [],
            "capitulos_auditados": [],
            "manga_progreso": {}
        }
        guardar_datos_saga(datos_iniciales)

def cargar_datos_saga():
    inicializar_datos()
    try:
        with open(FICHERO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        inicializar_datos()
        with open(FICHERO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)

def guardar_datos_saga(datos):
    with open(FICHERO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def listar_archivos_capitulos():
    """Busca todos los archivos .txt de capítulos disponibles (los 25 capítulos)."""
    ficheros = glob.glob("capitulos/*.txt") + glob.glob("*.txt")
    cap_files = [f for f in ficheros if "capitulo" in f.lower() or "cap" in f.lower() or "c_" in f.lower()]
    return sorted(list(set(cap_files)))

def aura_auditar_capitulo_real(fichero_path):
    """
    Aura lee el archivo real del capítulo usando Gemini, extrae los personajes
    y los clasifica jerárquicamente de forma automática.
    """
    datos = cargar_datos_saga()
    api_key = datos.get("credenciales", {}).get("gemini", "")
    
    if not api_key:
        return False, "Error: Introduce primero tu API Key de Gemini en la pestaña 'Credenciales Aisladas'."
    
    if not os.path.exists(fichero_path):
        return False, f"Error: No se encuentra el archivo {fichero_path}"

    with open(fichero_path, "r", encoding="utf-8") as f:
        texto_capitulo = f.read()

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Eres Aura, la analista literaria de la saga 'Los Cinco Reinos'. 
    Lee atentamente el texto del capítulo y extrae TODOS los personajes que aparezcan o sean mencionados.
    Presta absoluta atención a los detalles (por ejemplo, Esther es una niña pequeña rubia de 4 años, Hugo es protagonista, etc.).
    Para cada personaje indica:
    - Nombre exacto
    - Jerarquía estricta (Protagonista, Secundario, Antagonista o Terciario)
    - Edad/Tipo aproximado
    - Descripción física y de personalidad basada estrictamente en el texto.

    Responde ÚNICAMENTE en formato JSON válido con la siguiente estructura exacta:
    [
      {{
        "nombre": "Nombre",
        "rol": "Protagonista",
        "edad": "Edad o tipo",
        "descripcion": "Descripción detallada",
        "estado": "Activo",
        "notas": ""
      }}
    ]

    Texto del capítulo:
    {texto_capitulo}
    """

    try:
        response = model.generate_content(prompt)
        text_resp = response.text.strip()
        if text_resp.startswith("```json"):
            text_resp = text_resp[7:]
        if text_resp.endswith("```"):
            text_resp = text_resp[:-3]
            
        nuevos_personajes = json.loads(text_resp.strip())
        
        personajes_existentes = {p["nombre"].lower(): i for i, p in enumerate(datos["personajes"])}
        
        for p in nuevos_personajes:
            nombre_lower = p["nombre"].lower()
            if nombre_lower in personajes_existentes:
                idx = personajes_existentes[nombre_lower]
                datos["personajes"][idx]["descripcion"] = p["descripcion"]
                datos["personajes"][idx]["rol"] = p["rol"]
            else:
                datos["personajes"].append(p)
                
        if fichero_path not in datos["capitulos_auditados"]:
            datos["capitulos_auditados"].append(fichero_path)
            
        guardar_datos_saga(datos)
        return True, f"Aura ha analizado '{os.path.basename(fichero_path)}' y ha actualizado los personajes con éxito."
    except Exception as e:
        return False, f"Error al procesar con Aura: {str(e)}"