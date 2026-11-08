import json
import os
import glob
import google.generativeai as genai

FICHERO_DATOS = "datos_agencia_completo.json"

def inicializar_datos():
    if not os.path.exists(FICHERO_DATOS):
        datos_iniciales = {
            "credenciales": {
                "instagram": {"app_id": "", "app_secret": "", "access_token": "", "instagram_account_id": ""},
                "tiktok": {"client_key": "", "client_secret": "", "access_token": ""},
                "twitter": {"api_key": "", "api_secret": "", "access_token": "", "access_secret": ""},
                "gemini": {"api_key": ""}
            },
            "personajes": [
                {"nombre": "Hugo", "rol": "Protagonista", "edad": "16", "descripcion": "Joven delgado, alto, de pelo negro y ojos azul celeste.", "estado": "Activo", "notas": ""},
                {"nombre": "Esther", "rol": "Protagonista", "edad": "4", "descripcion": "Niña pequeña rubia que viaja en avión y presencia el ataque.", "estado": "Activo", "notas": ""}
            ],
            "bestiario": [],
            "mapas_accesorios": [],
            "capitulos_auditados": [],
            "banco_multicanal": []
        }
        guardar_datos_agencia(datos_iniciales)

def cargar_datos_agencia():
    inicializar_datos()
    try:
        with open(FICHERO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        inicializar_datos()
        with open(FICHERO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)

def guardar_datos_agencia(datos):
    with open(FICHERO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def listar_archivos_capitulos():
    ficheros = glob.glob("capitulos/*.txt") + glob.glob("*.txt")
    cap_files = [f for f in ficheros if "capitulo" in f.lower() or "cap" in f.lower() or "c_" in f.lower()]
    return sorted(list(set(cap_files)))

def aura_analizar_capitulo_y_generar_ideas(fichero_path, tipo_publicacion="Reel Semanal / Vídeo"):
    datos = cargar_datos_agencia()
    api_key = datos.get("credenciales", {}).get("gemini", {}).get("api_key", "")
    
    if not api_key:
        return False, "⚠️ Falta la clave API de Gemini en la pestaña de Credenciales."
    
    if not os.path.exists(fichero_path):
        return False, f"⚠️ No se encuentra el fichero {fichero_path}"

    try:
        with open(fichero_path, "r", encoding="utf-8") as f:
            texto = f.read()
    except Exception as e:
        return False, f"Error al leer el archivo: {str(e)}"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Actúa como AURA, analista literaria de 'Los Cinco Reinos', coordinando a Hércules, Dante, Kira, Hermes, Vulcano y Crono.
    Lee el texto y extrae en formato JSON puro:
    1. "personajes": Lista de objetos con [nombre, rol (Protagonista/Secundario/Antagonista/Terciario), edad, descripcion].
    2. "bestiario": Lista de criaturas [nombre, descripcion].
    3. "mapas_accesorios": Lista de objetos/lugares [nombre, tipo, descripcion].
    4. "propuesta_marketing": Objeto con el contenido solicitado de tipo '{tipo_publicacion}' que contenga:
       - "tipo": "{tipo_publicacion}"
       - "idea_visual": "Guion o concepto visual para Hércules (incluyendo generación de vídeos o imágenes de personajes)",
       - "copy": "Texto o guion persuasivo redactado por Dante",
       - "hashtags": "Hashtags optimizados por Kira para máximo alcance"

    ESTRUCTURA JSON EXACTA:
    {{
      "personajes": [{{"nombre": "", "rol": "", "edad": "", "descripcion": ""}}],
      "bestiario": [{{"nombre": "", "descripcion": ""}}],
      "mapas_accesorios": [{{"nombre": "", "tipo": "", "descripcion": ""}}],
      "propuesta_marketing": {{
        "tipo": "{tipo_publicacion}",
        "idea_visual": "",
        "copy": "",
        "hashtags": ""
      }}
    }}

    Texto del capítulo:
    {texto}
    """

    try:
        response = model.generate_content(prompt)
        text_resp = response.text.strip()
        if text_resp.startswith("```json"):
            text_resp = text_resp[7:]
        if text_resp.endswith("```"):
            text_resp = text_resp[:-3]
            
        resultado = json.loads(text_resp.strip())
        
        # Sincronización de base de datos
        for p in resultado.get("personajes", []):
            if not any(x["nombre"].lower() == p["nombre"].lower() for x in datos["personajes"]):
                datos["personajes"].append(p)
        for b in resultado.get("bestiario", []):
            if not any(x["nombre"].lower() == b["nombre"].lower() for x in datos["bestiario"]):
                datos["bestiario"].append(b)
        for m in resultado.get("mapas_accesorios", []):
            if not any(x["nombre"].lower() == m["nombre"].lower() for x in datos["mapas_accesorios"]):
                datos["mapas_accesorios"].append(m)
                
        if "propuesta_marketing" in resultado:
            datos["banco_multicanal"].append(resultado["propuesta_marketing"])
            
        if fichero_path not in datos["capitulos_auditados"]:
            datos["capitulos_auditados"].append(fichero_path)
            
        guardar_datos_agencia(datos)
        return True, "✨ Aura y el equipo han procesado el capítulo, actualizado el lore y generado el contenido en el banco multicanal de Crono."
    except Exception as e:
        return False, f"Error en la IA: {str(e)}"