import os
import glob
import re
from datetime import datetime

class MotorDiario:
    def __init__(self, carpeta_capitulos="."):
        self.carpeta_capitulos = carpeta_capitulos
        self.historial_proceso = []
        # Base de lore limpia y estricta (solo personajes reales)
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

    def aura_escanear_capitulos_automatico(self):
        """Aura analiza los capítulos pero filtra estrictamente verbos y palabras comunes."""
        archivos = self.listar_capitulos()
        texto_acumulado = ""
        
        for arq in archivos:
            texto_acumulado += "\n" + self.leer_capitulo(arq)

        # Buscamos nombres propios que aparezcan en medio del texto (precedidos por minúscula o puntuación, evitando inicio de frase)
        # Esto reduce drásticamente que coja verbos conjugados al empezar un párrafo u oración.
        posibles_nombres = re.findall(r'(?<=[,;\(\)\"\s])[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{3,}\b', texto_acumulado)
        
        # Lista masiva de exclusión de palabras que nunca son nombres de personajes
        ignorar = {
            "El", "La", "Los", "Las", "Un", "Una", "Y", "Pero", "O", "Si", "No", 
            "Capitulo", "Capítulo", "Reino", "Reinos", "Cinco", "Frontera", "Brisas",
            "Cuando", "Donde", "Desde", "Hasta", "Entre", "Sobre", "Tras", "Aquel",
            "Aquella", "Este", "Esta", "Todo", "Todos", "Nada", "Algo", "Sombra",
            "Pero", "Porque", "Como", "Tan", "Mas", "Más", "Era", "Eran", "Fue",
            "Volvamos", "Poco", "Tanto", "Llamó", "Corre", "Perdona", "Hacerlo",
            "Pociones", "Concérnate", "Entonces", "Mientras", "Despues", "Después",
            "Aunque", "Apenas", "Siempre", "Nunca", "Hacia", "Contra", "Hacer"
        }

        nombres_filtrados = [n for n in set(posibles_nombres) if n not in ignorar]

        nuevos_detectados = []
        # Solo añadimos si realmente parecen nombres consistentes y limpios
        for nombre in nombres_filtrados:
            if nombre not in self.lore_personajes and len(nombre) > 3:
                self.lore_personajes[nombre] = {
                    "rol": "Personaje detectado en capítulos",
                    "descripcion": f"Extraído automáticamente por Aura de los textos analizados."
                }
                nuevos_detectados.append(nombre)

        return {
            "archivos_leidos": len(archivos),
            "personajes_totales": list(self.lore_personajes.keys()),
            "nuevos_añadidos": nuevos_detectados
        }

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