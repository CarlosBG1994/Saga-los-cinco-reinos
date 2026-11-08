import json
import os
import glob
import google.generativeai as genai
from motor_aprendizajes import cargar_aprendizajes, obtener_prompt_aprendido_para_hercules

FICHERO_DATOS = "datos_saga.json"

def inicializar_datos():
    """Asegura la existencia del JSON con toda la estructura maestra inicial."""
    if not os.path.exists(FICHERO_DATOS):
        datos_iniciales = {
            "credenciales": {
                "gemini": "",
                "instagram": "",
                "tiktok": "",
                "twitter": ""
            },
            "personajes": [
                {
                    "nombre": "Hugo",
                    "rol": "Protagonista",
                    "edad": "16",
                    "descripcion": "Joven delgado, alto, de pelo negro y ojos azul celeste, protagonista de la saga.",
                    "estado": "Activo",
                    "notas": "Mantener siempre el diseño coherente en todas las ilustraciones."
                },
                {
                    "nombre": "Esther",
                    "rol": "Protagonista",
                    "edad": "4",
                    "descripcion": "Niña pequeña rubia que viaja en el avión con su madre y presencia el ataque de los seres oscuros.",
                    "estado": "Activo",
                    "notas": "Cuidar estrictamente que su aspecto sea de una niña infantil de 4 años."
                }
            ],
            "capitulos_auditados": [],
            "banco_multicanal": [],
            "manga_progreso": {}
        }
        guardar_datos_saga(datos_iniciales)

def cargar_datos_saga():
    """Carga los datos de la saga asegurando manejo de excepciones y resiliencia."""
    inicializar_datos()
    try:
        with open(FICHERO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        inicializar_datos()
        with open(FICHERO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)

def guardar_datos_saga(datos):
    """Guarda los datos de la saga en el archivo JSON maestro."""
    with open(FICHERO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def listar_archivos_capitulos():
    """
    Escanea de forma robusta la carpeta de trabajo para localizar
    todos los archivos de texto correspondientes a los 25 capítulos.
    """
    ficheros = glob.glob("capitulos/*.txt") + glob.glob("*.txt")
    cap_files = [
        f for f in ficheros 
        if "capitulo" in f.lower() or "cap" in f.lower() or "c_" in f.lower() or "episodio" in f.lower()
    ]
    return sorted(list(set(cap_files)))

def aura_auditar_capitulo_real(fichero_path):
    """
    Aura lee de forma autónoma y profunda el archivo de texto real del capítulo mediante Gemini,
    extrayendo los personajes, respetando jerarquías y actualizando la base de datos oficial.
    """
    datos = cargar_datos_saga()
    api_key = datos.get("credenciales", {}).get("gemini", "")
    
    if not api_key:
        return False, "⚠️ Error crítico: Introduce tu clave API de Google AI Studio (Gemini) en la pestaña 'Credenciales Aisladas'."
    
    if not os.path.exists(fichero_path):
        return False, f"⚠️ Error: No se encuentra el archivo físico '{fichero_path}' en el servidor."

    try:
        with open(fichero_path, "r", encoding="utf-8") as f:
            texto_capitulo = f.read()
    except Exception as e:
        return False, f"Error al leer el archivo de texto: {str(e)}"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Actúa como AURA, la analista literaria de máxima precisión de la saga 'Los Cinco Reinos'.
    Tu misión es realizar una auditoría exhaustiva del texto del capítulo proporcionado.
    Extrae ABSOLUTAMENTE TODOS los personajes que aparezcan, tengan diálogo o sean mencionados de forma relevante.
    
    REGLAS ESTRICTAS DE EXTRACCIÓN:
    1. Respeta los perfiles clave preexistentes (por ejemplo: Esther es una niña pequeña rubia de 4 años; Hugo es el protagonista de 16 años, etc.).
    2. Clasifica a cada personaje estrictamente en una de estas cuatro jerarquías: 'Protagonista', 'Secundario', 'Antagonista' o 'Terciario'.
    3. Proporciona una descripción física, de edad/tipo y de personalidad basada de manera fidedigna en el texto del capítulo.

    DEBES RESPONDER ÚNICAMENTE EN FORMATO JSON VÁLIDO (sin texto adicional fuera del JSON), con la siguiente estructura de lista de objetos:
    [
      {{
        "nombre": "Nombre del personaje",
        "rol": "Protagonista / Secundario / Antagonista / Terciario",
        "edad": "Edad o clasificación (ej: 4 años, adulto, desconocido)",
        "descripcion": "Descripción detallada extraída del texto",
        "estado": "Activo",
        "notas": ""
      }}
    ]

    TEXTO COMPLETO DEL CAPÍTULO A ANALIZAR:
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
                if not datos["personajes"][idx].get("edad"):
                    datos["personajes"][idx]["edad"] = p.get("edad", "")
            else:
                datos["personajes"].append(p)
                
        if fichero_path not in datos["capitulos_auditados"]:
            datos["capitulos_auditados"].append(fichero_path)
            
        guardar_datos_saga(datos)
        return True, f"✨ Aura ha auditado con éxito '{os.path.basename(fichero_path)}': Se han sincronizado los personajes en la base de datos."
    except Exception as e:
        return False, f"⚠️ Error en la auditoría de Aura con Gemini: {str(e)}"