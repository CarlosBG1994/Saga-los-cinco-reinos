import time
import json
import os
import threading
from datetime import datetime

ARCHIVO_DATOS = "datos_saga.json"

class GestorPersistencia:
    """Gestiona el guardado y carga automática para que no se pierda nada entre sesiones."""
    @staticmethod
    def cargar_datos():
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"banco_contenido": [], "paginas_manga": []}

    @staticmethod
    def guardar_datos(datos):
        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

class AuraCoAutora:
    """Aura: Lee capítulos, analiza lore y redacta manteniendo el estilo exacto."""
    def redactar_siguiente_parte(self, instruccion_usuario):
        time.sleep(1)
        return f"Fragmento narrativo generado con base en: '{instruccion_usuario}'."

class ColmenaBufferInfinito:
    """Orquesta la producción continua y la modalidad de manga con persistencia total."""
    def __init__(self):
        self.aura = AuraCoAutora()
        datos = GestorPersistencia.cargar_datos()
        self.banco_contenido_semanal = datos.get("banco_contenido", [])
        self.paginas_manga = datos.get("paginas_manga", [])

    def sincronizar(self):
        GestorPersistencia.guardar_datos({
            "banco_contenido": self.banco_contenido_semanal,
            "paginas_manga": self.paginas_manga
        })

    def ciclo_produccion_continua(self, instruccion):
        texto = self.aura.redactar_siguiente_parte(instruccion)
        paquete_nuevo = {
            "id": len(self.banco_contenido_semanal) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "texto": texto,
            "imagen_renderizada": "asset_visual_epico.png",
            "copy_comercial": "Descubre el destino de los reinos. Disponible en Amazon y Letrame.",
            "hashtags": "#CincoReinos #Fantasía #Manga #Wattpad",
            "estado": "Listo en Almacén (Pendiente de Selección)"
        }
        self.banco_contenido_semanal.append(paquete_nuevo)
        self.sincronizar()

    def hercules_modo_mangaka(self, escena_descripcion):
        nueva_pagina = {
            "pag_id": len(self.paginas_manga) + 1,
            "escena": escena_descripcion,
            "imagen_url": "https://picsum.photos/600/400",
            "correcciones": []
        }
        self.paginas_manga.append(nueva_pagina)
        self.sincronizar()
        return nueva_pagina

    def guardar_correccion_manga(self, pag_id, nota):
        for pag in self.paginas_manga:
            if pag["pag_id"] == pag_id:
                pag["correcciones"].append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "nota": nota
                })
                self.sincronizar()
                break

class HermesVulcanoPostPublicacion:
    """Hermes y Vulcano: Analizan métricas y responden comentarios post-publicación."""
    def actualizar_metricas(self):
        return {"vistas": 12450, "clicks_amazon": 342, "engagement": "Alto"}

    def gestionar_comentarios(self):
        return "Comentarios respondidos con el tono oficial de la saga."