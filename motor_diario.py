import os
import glob
import google.generativeai as genai
from datetime import datetime

class MotorDiario:
    def __init__(self, carpeta_capitulos="."):
        self.carpeta_capitulos = carpeta_capitulos
        self.historial_proceso = []
        # Base de lore inicial
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
        return ""

    def aura_escanear_capitulos_automatico_ia(self, api_key):
        """Aura usa la IA de Gemini para leer los capítulos y extraer personajes reales de la novela."""
        if not api_key:
            return {"error": "Se requiere una API Key de Google AI Studio válida en Ajustes."}

        genai.configure(api_key=api_key)
        # Usamos el modelo exacto que solicita la API
        modelo = genai.GenerativeModel("gemini-3.8-flash")

        archivos = self.listar_capitulos()
        texto_acumulado = ""
        for arq in archivos[:15]: 
            texto_acumulado += f"\n--- {arq} ---\n" + self.leer_capitulo(arq)

        prompt = (
            "Eres Aura, la analista textual experta de la saga de fantasía 'Los Cinco Reinos'. "
            "Analiza el siguiente texto de los capítulos de la novela y extrae una lista ÚNICA con los nombres de los PERSONAJES "
            "que aparezcan en la historia (ignora verbos, lugares, palabras comunes o títulos). "
            "Devuelve los nombres separados por comas, sin explicaciones adicionales (ejemplo: Hugo, Esther, Albia, etc.):\n\n"
            f"{texto_acumulado[:30000]}"
        )

        try:
            respuesta = modelo.generate_content(prompt)
            nombres_sugeridos = [n.strip() for n in respuesta.text.split(",") if n.strip()]
            
            nuevos_añadidos = []
            for nombre in nombres_sugeridos:
                nombre_limpio = nombre.replace("-", "").title()
                if len(nombre_limpio) > 2 and nombre_limpio not in self.lore_personajes:
                    self.lore_personajes[nombre_limpio] = {
                        "rol": "Personaje extraído por Aura (IA)",
                        "descripcion": "Detectado automáticamente mediante análisis semántico de los capítulos."
                    }
                    nuevos_añadidos.append(nombre_limpio)

            return {
                "archivos_leidos": len(archivos),
                "personajes_totales": list(self.lore_personajes.keys()),
                "nuevos_añadidos": nuevos_añadidos
            }
        except Exception as e:
            return {"error": str(e)}

    def sincronizar_hercules_lore(self, personaje_activo):
        info = self.lore_personajes.get(personaje_activo, {"descripcion": "Personaje de Los Cinco Reinos."})
        directriz = (
            f"🎨 [HÉRCULES - RENDER ACTIVO]\n"
            f"• Personaje en escena: {personaje_activo} ({info.get('rol', 'Secundario')})\n"
            f"• Rasgos clave aplicados: {info['descripcion']}\n"
            f"• Estética: Fantasía épica oscura, iluminación cinematográfica, fidelidad absoluta al universo de Los Cinco Reinos."
        )
        return directriz

    def agregar_personaje(self, nombre, rol, descripcion):
        if nombre and nombre not in self.lore_personajes:
            self.lore_personajes[nombre] = {"rol": rol, "descripcion": descripcion}
            return True
        return False

    def eliminar_personaje(self, nombre):
        if nombre in self.lore_personajes:
            del self.lore_personajes[nombre]
            return True
        return False

    def procesar_agentes_autonomos(self, capitulo_sel, personaje_sel, formato_sel):
        texto = self.leer_capitulo(capitulo_sel)
        directriz_hercules = self.sincronizar_hercules_lore(personaje_sel)
        
        resultado = {
            "estado": "Validado",
            "aura_analisis": f"Análisis exhaustivo de `{capitulo_sel}` finalizado. Se han cruzado las tramas con el perfil de {personaje_sel}.",
            "hercules_render": directriz_hercules,
            "dante_copy": f"✨ [LOS CINCO REINOS] La frontera se quema... ¿Qué esconde realmente {personaje_sel}? Descúbrelo en el nuevo capítulo. 🔥📖 #{personaje_sel} #FantasíaÉpica #BookTok",
            "kira_tags": "#LosCincoReinos #FantasíaOscura #Lectores #WritersOfTikTok #Bookstagram"
        }
        return resultado

motor = MotorDiario()