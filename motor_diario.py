import os
import glob
from datetime import datetime

class MotorDiario:
    def __init__(self, carpeta_capitulos="."):
        self.carpeta_capitulos = carpeta_capitulos
        self.historial_proceso = []
        # Base de lore interna gestionada por el motor
        self.lore_personajes = {
            "Hugo": {
                "rol": "Protagonista",
                "descripcion": "Joven delgado, alto, de pelo negro y ojos azul celeste."
            },
            "Esther": {
                "rol": "Protagonista",
                "descripcion": "Protagonista principal de la saga Los Cinco Reinos."
            }
        }

    def listar_capitulos(self):
        """Escanea dinámicamente la carpeta en busca de archivos de texto de la saga."""
        patron = os.path.join(self.carpeta_capitulos, "*.txt")
        archivos = glob.glob(patron)
        return [os.path.basename(f) for f in archivos] if archivos else ["capitulo_0.txt"]

    def leer_capitulo(self, nombre_archivo):
        """Lee el contenido del capítulo seleccionado para que Aura lo analice."""
        ruta_completa = os.path.join(self.carpeta_capitulos, nombre_archivo)
        if os.path.exists(ruta_completa):
            try:
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error al leer el archivo {nombre_archivo}: {e}"
        return f"Aviso: El archivo '{nombre_archivo}' no se encuentra en el directorio raíz."

    def sincronizar_hercules_lore(self, personaje_activo):
        """Prepara el paquete de directrices visuales para Hércules basado en el lore."""
        info = self.lore_personajes.get(personaje_activo, {"descripcion": "Personaje secundario de Los Cinco Reinos."})
        directriz = (
            f"[MOTOR SYNC HÉRCULES] Personaje: {personaje_activo} | "
            f"Rasgos clave: {info['descripcion']} | "
            f"Mandato: Mantener fidelidad estética absoluta al universo de la saga."
        )
        return directriz

    def procesar_agentes_autonomos(self, capitulo_sel, personaje_sel, formato_sel):
        """Simula la ejecución coordinada de toda la oficina de agentes."""
        texto = self.leer_capitulo(capitulo_sel)
        directriz_hercules = self.sincronizar_hercules_lore(personaje_sel)
        
        resultado = {
            "estado": "Éxito",
            "aura_analisis": f"Extracción completada de {capitulo_sel}. Se han detectado ganchos de misterio y tensiones en la frontera.",
            "hercules_render": directriz_hercules,
            "dante_copy": f"✨ [LOS CINCO REINOS] Un paso más cerca del abismo... Descubre lo que esconde {personaje_sel}. 🔥📖 #{personaje_sel} #Fantasía Épica",
            "kira_tags": "#LosCincoReinos #BookTok #FantasíaOscura #Lectores #Writers"
        }
        return resultado

# Instancia global para importar en app.py
motor = MotorDiario()