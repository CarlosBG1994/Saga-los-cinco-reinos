import json
import os

FICHERO_APRENDIZAJES = "aprendizajes_equipo.json"

def cargar_aprendizajes():
    """Carga la memoria persistente del equipo y el estado en vivo de cada agente."""
    if os.path.exists(FICHERO_APRENDIZAJES):
        try:
            with open(FICHERO_APRENDIZAJES, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Estructura maestra inicial de los 7 agentes y sus registros
    return {
        "agentes": {
            "Aura": {"estado": "Analizando textos y extrayendo ideas", "bloqueo": None, "feedback": []},
            "Hércules": {"estado": "Preparando diseños y vídeos", "bloqueo": None, "feedback": []},
            "Dante": {"estado": "Redactando copys y guiones", "bloqueo": None, "feedback": []},
            "Kira": {"estado": "Optimizando hashtags y alcance", "bloqueo": None, "feedback": []},
            "Hermes": {"estado": "Monitoreando interacciones", "bloqueo": None, "feedback": []},
            "Vulcano": {"estado": "Analizando métricas de eficiencia", "bloqueo": None, "feedback": []},
            "Crono": {"estado": "Sincronizando el calendario editorial", "bloqueo": None, "feedback": []}
        },
        "historial_correcciones": []
    }

def guardar_aprendizajes(datos):
    """Guarda los aprendizajes y estados del equipo en disco."""
    with open(FICHERO_APRENDIZAJES, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def registrar_feedback_agente(agente, nota):
    """Registra una directriz de mejora o corrección para un agente específico."""
    datos = cargar_aprendizajes()
    if agente in datos["agentes"]:
        datos["agentes"][agente]["feedback"].append(nota)
        datos["historial_correcciones"].append({
            "agente": agente, 
            "instruccion": nota
        })
    guardar_aprendizajes(datos)
    return datos

def actualizar_estado_agente(agente, estado, bloqueo=None):
    """Actualiza en tiempo real el estado o bloqueo de un agente para la sala de máquinas."""
    datos = cargar_aprendizajes()
    if agente in datos["agentes"]:
        datos["agentes"][agente]["estado"] = estado
        if bloqueo is not None:
            datos["agentes"][agente]["bloqueo"] = bloqueo
    guardar_aprendizajes(datos)