import json
import os

FICHERO_APRENDIZAJES = "aprendizajes_hercules.json"

def cargar_aprendizajes():
    """Carga el historial completo de aprendizajes y correcciones de Hércules."""
    if os.path.exists(FICHERO_APRENDIZAJES):
        try:
            with open(FICHERO_APRENDIZAJES, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "preferencias_estilo": [], 
        "correcciones_personajes": {}, 
        "reglas_manga": [],
        "historial_correcciones": []
    }

def guardar_aprendizajes(datos):
    """Guarda la memoria de aprendizaje en disco."""
    with open(FICHERO_APRENDIZAJES, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def registrar_feedback_hercules(tipo, clave, nota):
    """
    Registra directrices detalladas para que Hércules aprenda de cada corrección.
    tipo: 'estilo', 'personaje' o 'manga'
    clave: identificador específico (ej. nombre de personaje o 'general')
    nota: la instrucción exacta dada por el usuario.
    """
    datos = cargar_aprendizajes()
    
    registro_entrada = {
        "tipo": tipo,
        "clave": clave,
        "instruccion": nota
    }
    datos["historial_correcciones"].append(registro_entrada)

    if tipo == 'estilo':
        if nota not in datos["preferencias_estilo"]:
            datos["preferencias_estilo"].append(nota)
    elif tipo == 'personaje':
        if clave not in datos["correcciones_personajes"]:
            datos["correcciones_personajes"][clave] = []
        if nota not in datos["correcciones_personajes"][clave]:
            datos["correcciones_personajes"][clave].append(nota)
    elif tipo == 'manga':
        if nota not in datos["reglas_manga"]:
            datos["reglas_manga"].append(nota)
    
    guardar_aprendizajes(datos)
    return datos

def obtener_prompt_aprendido_para_hercules():
    """Compila todas las reglas aprendidas para inyectarlas en los prompts de Hércules."""
    datos = cargar_aprendizajes()
    prompt_adicional = ""
    if datos["preferencias_estilo"]:
        prompt_adicional += " Estilo preferido por el autor: " + "; ".join(datos["preferencias_estilo"]) + "."
    if datos["reglas_manga"]:
        prompt_adicional += " Reglas de manga estrictas: " + "; ".join(datos["reglas_manga"]) + "."
    return prompt_adicional