import os
import glob
import time
import google.generativeai as genai

class MotorDiario:
    def __init__(self, carpeta_capitulos="."):
        self.carpeta_capitulos = carpeta_capitulos
        self.lore_personajes = {
            "Hugo": {
                "rol": "Protagonista",
                "descripcion": "Joven delgado, alto, de pelo negro y ojos azul celeste.",
                "color_tema": "#FFD700" # Dorado / Amarillo
            },
            "Esther": {
                "rol": "Protagonista",
                "descripcion": "Protagonista principal de la saga Los Cinco Reinos.",
                "color_tema": "#FFC107" # Amarillo cálido
            }
        }

    def listar_capitulos(self):
        patron = os.path.join(self.carpeta_capitulos, "*.txt")
        archivos = glob.glob(patron)
        return [os.path.basename(f) for f in archivos] if archivos else ["capitulo_0.txt"]

    def leer_capitulo(self, nombre_archivo):
        ruta_completa = os.path.join(self.carpeta_capitulos, nombre_archivo)
        if os.path.exists(ruta_completa):
            try:
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error al leer el archivo {nombre_archivo}: {e}"
        return ""

    def aura_escanear_capitulos_automatico_ia(self, api_key):
        if not api_key:
            return {"error": "Se requiere una API Key válida."}

        genai.configure(api_key=api_key)
        modelo = genai.GenerativeModel("gemini-3.8-flash")

        archivos = self.listar_capitulos()
        texto_resumido = ""
        for arq in archivos[:8]: 
            contenido = self.leer_capitulo(arq)
            texto_resumido += f"\n[{arq}]: {contenido[:1500]}\n"

        prompt = (
            "Eres Aura, analista textual de 'Los Cinco Reinos'. "
            "Extrae una lista ÚNICA con los nombres de los PERSONAJES principales o secundarios que aparezcan. "
            "Devuelve los nombres separados estrictamente por comas (ejemplo: Hugo, Esther, Albia):\n\n"
            f"{texto_resumido}"
        )

        try:
            time.sleep(1)
            respuesta = modelo.generate_content(prompt)
            nombres_sugeridos = [n.strip() for n in respuesta.text.split(",") if n.strip()]
            
            nuevos_añadidos = []
            for nombre in nombres_sugeridos:
                nombre_limpio = nombre.replace("-", "").title()
                if len(nombre_limpio) > 2 and nombre_limpio not in self.lore_personajes:
                    self.lore_personajes[nombre_limpio] = {
                        "rol": "Personaje extraído por Aura",
                        "descripcion": "Detectado mediante análisis semántico.",
                        "color_tema": "#FFD700"
                    }
                    nuevos_añadidos.append(nombre_limpio)

            return {
                "archivos_leidos": len(archivos),
                "personajes_totales": list(self.lore_personajes.keys()),
                "nuevos_añadidos": nuevos_añadidos
            }
        except Exception as e:
            return {"error": str(e)}

    def hercules_generar_avatar_svg(self, personaje_activo, cambios_usuario=""):
        """Genera un escudo/avatar en SVG local con tonos dorados/amarillos y las modificaciones del usuario."""
        info = self.lore_personajes.get(personaje_activo, {})
        desc = info.get("descripcion", "")
        
        mod_texto = f" | Mod: {cambios_usuario}" if cambios_usuario.strip() else ""
        
        # SVG dinámico autocontenido en tonos oscuros y dorados (amarillos)
        svg_code = f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
            <defs>
                <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#111111" />
                    <stop offset="100%" stop-color="#2c2200" />
                </linearGradient>
                <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#FFC107" />
                    <stop offset="50%" stop-color="#FFD700" />
                    <stop offset="100%" stop-color="#FFA000" />
                </linearGradient>
            </defs>
            <rect width="400" height="600" fill="url(#bg)" rx="15"/>
            <rect x="20" y="20" width="360" height="560" fill="none" stroke="url(#gold)" stroke-width="3" rx="10"/>
            <!-- Símbolo / Escudo central -->
            <circle cx="200" cy="200" r="80" fill="url(#gold)" opacity="0.15"/>
            <circle cx="200" cy="200" r="70" fill="none" stroke="url(#gold)" stroke-width="2" stroke-dasharray="6,4"/>
            <text x="200" y="190" fill="#FFD700" font-family="Georgia, serif" font-size="64" font-weight="bold" text-anchor="middle">👑</text>
            <!-- Títulos y Textos -->
            <text x="200" y="320" fill="#FFD700" font-family="Georgia, serif" font-size="26" font-weight="bold" text-anchor="middle">{personaje_activo}</text>
            <text x="200" y="355" fill="#FFE082" font-family="Arial, sans-serif" font-size="14" text-anchor="middle">LOS CINCO REINOS</text>
            <line x1="60" y1="380" x2="340" y2="380" stroke="#FFD700" stroke-width="1" opacity="0.4"/>
            <!-- Descripción y Modificaciones -->
            <foreignObject x="40" y="405" width="320" height="150">
                <div xmlns="http://www.w3.org/1999/xhtml" style="color: #FFF8E1; font-family: Arial, sans-serif; font-size: 13px; text-align: center; line-height: 1.4;">
                    <p><b>Rol:</b> {info.get('rol', '')}</p>
                    <p>{desc}</p>
                    <p style="color: #FFD700; font-style: italic;">{mod_texto}</p>
                </div>
            </foreignObject>
        </svg>
        """
        return svg_code

    def sincronizar_hercules_lore(self, personaje_activo):
        info = self.lore_personajes.get(personaje_activo, {"descripcion": "Personaje de Los Cinco Reinos."})
        return f"🎨 [HÉRCULES] Render activo para {personaje_activo} ({info.get('rol')}) en gama dorada/amarilla."

    def agregar_personaje(self, nombre, rol, descripcion):
        if nombre and nombre not in self.lore_personajes:
            self.lore_personajes[nombre] = {"rol": rol, "descripcion": descripcion, "color_tema": "#FFD700"}
            return True
        return False

    def eliminar_personaje(self, nombre):
        if nombre in self.lore_personajes:
            del self.lore_personajes[nombre]
            return True
        return False

    def procesar_agentes_autonomos(self, capitulo_sel, personaje_sel, formato_sel):
        return {
            "estado": "Validado",
            "aura_analisis": f"Análisis de `{capitulo_sel}` completado para {personaje_sel}.",
            "hercules_render": self.sincronizar_hercules_lore(personaje_sel),
            "dante_copy": f"✨ [LOS CINCO REINOS] Descubre los secretos de {personaje_sel}. 🔥📖 #{personaje_sel} #FantasíaÉpica #BookTok",
            "kira_tags": "#LosCincoReinos #FantasíaOscura #WritersOfTikTok #Bookstagram"
        }

motor = MotorDiario()