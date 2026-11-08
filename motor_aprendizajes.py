import json
import os

FICHERO_APRENDIZAJES = "aprendizajes_hercules.json"

def cargar_aprendizajes():
    if os.path.exists(FICHERO_APRENDIZAJES):
        try:
            with open(FICHERO_APRENDIZAJES, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"preferencias_estilo": [], "correcciones_personajes": {}, "reglas_manga": []}

def guardar_aprendizajes(datos):
    with open(FICHERO_APRENDIZAJES, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def registrar_feedback_hercules(tipo, clave, nota):
    """
    Registra una corrección o preferencia para que Hércules la aprenda.
    tipo: 'estilo', 'personaje' o 'manga'
    clave: identificador (ej. 'Ezequiel', 'general', 'viñetas')
    nota: la instrucción de mejora dada por el usuario.
    """
    datos = cargar_aprendizajes()
    if tipo == 'estilo':
        datos["preferencias_estilo"].append(nota)
    elif tipo == 'personaje':
        if clave not in datos["correcciones_personajes"]:
            datos["correcciones_personajes"][clave] = []
        datos["correcciones_personajes"][clave].append(nota)
    elif tipo == 'manga':
        datos["reglas_manga"].append(nota)
    
    guardar_aprendizajes(datos)
    return datos