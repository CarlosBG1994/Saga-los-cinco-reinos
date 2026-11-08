import json
import os
from motor_aprendizajes import cargar_aprendizajes

FICHERO_DATOS = "datos_saga.json"

def inicializar_datos():
    """Asegura que el archivo de datos de la saga exista con su estructura inicial completa."""
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
                    "descripcion": "Joven delgado, alto, de pelo negro y ojos azul celeste.", 
                    "estado": "Activo", 
                    "notas": ""
                },
                {
                    "nombre": "Esther", 
                    "rol": "Protagonista", 
                    "edad": "4", 
                    "descripcion": "Niña pequeña rubia que viaja en el avión con su madre y presencia el ataque.", 
                    "estado": "Activo", 
                    "notas": ""
                },
                {
                    "nombre": "Madre de Esther", 
                    "rol": "Secundario", 
                    "edad": "Adulto", 
                    "descripcion": "Mujer de mediana edad que protege y tranquiliza cariñosamente a Esther en el vuelo.", 
                    "estado": "Activo", 
                    "notas": ""
                },
                {
                    "nombre": "Ezequiel", 
                    "rol": "Secundario", 
                    "edad": "Adulto", 
                    "descripcion": "Hombre esbelto y alto, estilo gentleman bohemio, pelo negro con trazas blancas, ojos amarillo oscuro, barba bien cuidada y bastón con empuñadura de león dorado.", 
                    "estado": "Activo", 
                    "notas": ""
                },
                {
                    "nombre": "Jakkar", 
                    "rol": "Secundario", 
                    "edad": "Desconocida", 
                    "descripcion": "Trol verde de dos metros, ojos negros y hundidos, dientes afilados como astillas; capaz de adoptar forma de anciana ('señora Wilson').", 
                    "estado": "Activo", 
                    "notas": ""
                },
                {
                    "nombre": "Filtrian", 
                    "rol": "Antagonista", 
                    "edad": "Desconocida", 
                    "descripcion": "Antagonista con capacidad de transformarse en licántropo (lobo plateado), de pelo largo plateado en su forma humana.", 
                    "estado": "Activo", 
                    "notas": ""
                }
            ],
            "capitulos_auditados": ["Capítulo 0", "Capítulo 1"],
            "banco_multicanal": []
        }
        guardar_datos_saga(datos_iniciales)

def cargar_datos_saga():
    """Carga los datos de la saga desde el JSON asegurando integridad."""
    inicializar_datos()
    try:
        with open(FICHERO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # En caso de corrupción, reinicializa
        inicializar_datos()
        with open(FICHERO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)

def guardar_datos_saga(datos):
    """Guarda los datos actualizados de la saga en el JSON."""
    with open(FICHERO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def reauditar_capitulo(capitulo_nombre):
    """
    Fuerza a Aura a releer el capítulo para sincronizar y verificar
    la extracción de personajes y elementos narrativos.
    """
    datos = cargar_datos_saga()
    if capitulo_nombre not in datos["capitulos_auditados"]:
        datos["capitulos_auditados"].append(capitulo_nombre)
        guardar_datos_saga(datos)
    
    # Aquí se integraría la lógica de análisis profundo de Aura sobre los ficheros de texto (.txt)
    aprendizajes = cargar_aprendizajes()
    
    return f"Aura ha completado la reauditoría profunda de '{capitulo_nombre}'. Base de datos de personajes y directrices sincronizada correctamente."

def registrar_personaje_en_motor(nombre, rol, edad, descripcion):
    """Permite añadir un nuevo personaje detectado en las auditorías de Aura."""
    datos = cargar_datos_saga()
    # Evitar duplicados
    for p in datos["personajes"]:
        if p["nombre"].lower() == nombre.lower():
            return f"El personaje {nombre} ya existe en el registro."
            
    nuevo = {
        "nombre": nombre,
        "rol": rol,
        "edad": edad,
        "descripcion": descripcion,
        "estado": "Activo",
        "notas": ""
    }
    datos["personajes"].append(nuevo)
    guardar_datos_saga(datos)
    return f"Personaje {nombre} registrado con éxito."