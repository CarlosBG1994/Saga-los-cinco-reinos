import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

ARCHIVO_DATOS = "datos_saga.json"

class GestorPersistencia:
    @staticmethod
    def cargar_datos():
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "banco_contenido": [], 
            "paginas_manga": [], 
            "videos_tiktok": [],
            "estado_agentes": "Autodidactas y Proactivos", 
            "lore_wattpad": "", 
            "dudas_agentes": [],
            "lore_universo": [],
            "credenciales": {},
            "metricas_redes": {
                "Instagram": {"seguidores": 0, "rendimiento_principal": 0, "interacciones": 0, "ultima_actualizacion": "Pendiente"},
                "TikTok": {"seguidores": 0, "rendimiento_principal": 0, "interacciones": 0, "ultima_actualizacion": "Pendiente"},
                "Twitter (X)": {"seguidores": 0, "rendimiento_principal": 0, "interacciones": 0, "ultima_actualizacion": "Pendiente"}
            }
        }

    @staticmethod
    def guardar_datos(datos):
        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

class AuraCoAutora:
    def leer_wattpad(self, url_wattpad):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url_wattpad, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                parrafos = soup.find_all('p')
                return " ".join([p.get_text() for p in parrafos])[:3000]
            return "No se pudo extraer texto estructurado."
        except Exception as e:
            return f"Error: {e}"

    def redactar_estrategia_multicanal(self, instruccion_usuario, capitulo_texto):
        extracto = capitulo_texto[:1200] if capitulo_texto else "Sin capítulo."
        return {
            "feed": f"[Publicación Feed Proactiva]\n{extracto[:300]}...\n\n👉 Adéntrate en Los Cinco Reinos.\n#LosCincoReinos #DarkFantasy #MangaArt #BookTok",
            "tiktok_reel": f"[Vídeo / Reel / TikTok]\n(Escena inmersiva):\n\"Imagina estar leyendo un libro y de repente vivir la escena...\"\n\n{extracto[:250]}...\n\n#BookTokEspaña #FantasíaOscura #WritingCommunity",
            "historia": f"[Historia / Story]\n⚡ Análisis automático completado. ¡Descubre el nuevo avance!",
            "instruccion_base": instruccion_usuario
        }

    def describir_personaje_detallado(self, nombre_pj, contexto_obra):
        prompt_visual = f"detailed character design sheet of {nombre_pj}, dark fantasy aesthetic, manga style line art, expressive face, detailed clothing, concept art, monochrome with ink details, {contexto_obra[:400]}"
        return prompt_visual

class HerculesMangaka:
    def generar_boceto_personaje(self, nombre_pj, descripcion_aura):
        prompt_encoded = requests.utils.quote(f"character concept sketch, manga style, {descripcion_aura}")
        imagen_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=600&height=800&nologo=true"
        return imagen_url

    def estructurar_pagina_manga_avanzada(self, num_cap, capitulo_texto, estilo_narrativo=""):
        extracto = capitulo_texto[:400] if capitulo_texto else "Trama del capítulo."
        
        if "biblioteca" in estilo_narrativo.lower() or num_cap % 2 == 0:
            escena_desc = "Viñeta 1: Un lector en una atmósfera silenciosa de una biblioteca antigua. Viñeta 2: Transición visual donde el fondo se desvanece en un pensamiento con la escena del libro en acción."
            prompt_manga = f"manga page layout, split panel, a reader in an antique library transitioning into an epic fantasy battle thought bubble, detailed ink lines, black and white comic book style, {extracto}"
        else:
            escena_desc = "Secuencia de viñetas dinámicas adaptadas fielmente al clímax del capítulo."
            prompt_manga = f"manga comic page layout, multiple panels, action and dialogue, cinematic ink lines, dark fantasy, {extracto}"

        prompt_encoded = requests.utils.quote(prompt_manga)
        pagina_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=1200&nologo=true"

        return {
            "pag_id": num_cap,
            "escena_resumen": escena_desc,
            "guion_viñetas": f"Guion técnico autónomo de Hércules para Cap {num_cap}: {extracto[:200]}...",
            "imagen_url": pagina_url,
            "estado": "Borrador de Manga Generado de forma Autónoma"
        }

    def generar_video_vertical_profesional(self, num_cap, capitulo_texto, nuevo_id=1):
        extracto = capitulo_texto[:300] if capitulo_texto else "Trama impactante."
        prompt_vid = f"vertical 9:16 mobile video frame, dark fantasy anime aesthetic, intense dramatic lighting, motion blur, {extracto}"
        prompt_encoded = requests.utils.quote(prompt_vid)
        video_preview = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=720&height=1280&nologo=true"

        return {
            "id": nuevo_id,
            "tipo": "Vídeo / Reel / TikTok (9:16)",
            "capitulo": num_cap,
            "preview_url": video_preview,
            "guion_voz": f"Locución autónoma: '¿Y si el libro que lees cobra vida ante ti?' (Capítulo {num_cap}).",
            "estado": "Pendiente de tu revisión"
        }

class ColmenaBufferInfinito:
    def __init__(self):
        self.aura = AuraCoAutora()
        self.hercules = HerculesMangaka()
        datos = GestorPersistencia.cargar_datos()
        self.banco_contenido = datos.get("banco_contenido", [])
        self.paginas_manga = datos.get("paginas_manga", [])
        self.videos_tiktok = datos.get("videos_tiktok", [])
        self.lore_wattpad = datos.get("lore_wattpad", "")
        self.dudas_agentes = datos.get("dudas_agentes", [])
        self.lore_universo = datos.get("lore_universo", [])
        self.credenciales = datos.get("credenciales", {})
        self.metricas_redes = datos.get("metricas_redes", {})
        self.estado_agentes = "Autodidactas y Proactivos"

    def sincronizar(self):
        GestorPersistencia.guardar_datos({
            "banco_contenido": self.banco_contenido,
            "paginas_manga": self.paginas_manga,
            "videos_tiktok": self.videos_tiktok,
            "estado_agentes": self.estado_agentes,
            "lore_wattpad": self.lore_wattpad,
            "dudas_agentes": self.dudas_agentes,
            "lore_universo": self.lore_universo,
            "credenciales": self.credenciales,
            "metricas_redes": self.metricas_redes
        })

    def asimilar_historia_wattpad(self, url):
        texto = self.aura.leer_wattpad(url)
        self.lore_wattpad = texto
        self.sincronizar()
        return texto

    def obtener_capitulo(self, num):
        rutas = [f"capitulo {num}.txt", f"capitulo_{num}.txt", os.path.join("capitulos", f"capitulo {num}.txt")]
        desc = ""
        encontrado = False
        for r in rutas:
            if os.path.exists(r):
                try:
                    with open(r, "r", encoding="utf-8") as f:
                        desc = f.read()
                        encontrado = True
                        break
                except Exception as e:
                    desc = f"Error: {e}"
                    encontrado = True
                    break
        if not encontrado:
            desc = f"Capítulo {num} pendiente de carga en la raíz."
        return {"titulo": f"Capítulo {num}: Los Cinco Reinos", "descripcion": desc}

    def procesar_autonomia_capitulo(self, num_cap, capitulo_texto):
        # Aura y Hércules analizan de forma autodidacta y generan propuestas automáticamente si detectan texto nuevo
        existentes = [d for d in self.dudas_agentes if f"Capítulo {num_cap}" in d.get("pregunta", "")]
        if not existentes and len(capitulo_texto) > 150 and "pendiente" not in capitulo_texto.lower():
            # Plantean duda proactiva al usuario
            self.dudas_agentes.append({
                "id": len(self.dudas_agentes) + 1,
                "agente": "Aura & Hércules (Autodidactas)",
                "pregunta": f"[Capítulo {num_cap}] Hemos escaneado el capítulo de forma autónoma. ¿Consideras que debemos enfatizar más la atmósfera oscura o pasamos a generar los recursos de manga y redes con nuestro criterio?",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "respondida": False,
                "respuesta": ""
            })
            
            # Generación autónoma preliminar de página de manga y paquete de redes
            estilo_auto = "Especial: Lector en Biblioteca + Pensamiento con Escena del Libro"
            pag_autonoma = self.hercules.estructurar_pagina_manga_avanzada(num_cap, capitulo_texto, estilo_auto)
            if not any(p["pag_id"] == num_cap for p in self.paginas_manga):
                self.paginas_manga.append(pag_autonoma)

            copys_auto = self.aura.redactar_estrategia_multicanal("Análisis automático autónomo", capitulo_texto)
            if not any(b.get("cap_asociado") == num_cap for b in self.banco_contenido):
                self.banco_contenido.append({
                    "id": len(self.banco_contenido) + 1,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "cap_asociado": num_cap,
                    "copys": copys_auto,
                    "estado": "Propuesta Autónoma Pendiente de Revisión"
                })
        self.sincronizar()

    def guardar_personaje_con_boceto(self, nombre, descripcion):
        prompt_visual = self.aura.describir_personaje_detallado(nombre, descripcion)
        boceto_url = self.hercules.generar_boceto_personaje(nombre, prompt_visual)

        self.lore_universo.append({
            "id": len(self.lore_universo) + 1,
            "categoria": "Personaje",
            "nombre": nombre,
            "descripcion": descripcion,
            "prompt_visual": prompt_visual,
            "boceto_url": boceto_url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self.sincronizar()

    def actualizar_boceto_personaje(self, personaje_id, nueva_descripcion):
        for p in self.lore_universo:
            if p["id"] == personaje_id and p["categoria"] == "Personaje":
                p["descripcion"] = nueva_descripcion
                p["prompt_visual"] = self.aura.describir_personaje_detallado(p["nombre"], nueva_descripcion)
                p["boceto_url"] = self.hercules.generar_boceto_personaje(p["nombre"], p["prompt_visual"])
                self.sincronizar()
                break

    def generar_pagina_manga_capitulo(self, num_cap, estilo_narrativa=""):
        info = self.obtener_capitulo(num_cap)
        nueva_pagina = self.hercules.estructurar_pagina_manga_avanzada(num_cap, info["descripcion"], estilo_narrativa)
        self.paginas_manga.append(nueva_pagina)
        self.sincronizar()

    def generar_paquete_creativo_completo(self, instruccion, num_cap):
        info = self.obtener_capitulo(num_cap)
        texto_cap = info["descripcion"]

        copys = self.aura.redactar_estrategia_multicanal(instruccion, texto_cap)
        
        nuevo_vid_id = len(self.videos_tiktok) + 1
        video_rec = self.hercules.generar_video_vertical_profesional(num_cap, texto_cap, nuevo_vid_id)
        self.videos_tiktok.append(video_rec)

        self.banco_contenido.append({
            "id": len(self.banco_contenido) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "cap_asociado": num_cap,
            "copys": copys,
            "estado": "Pendiente de Aprobación"
        })
        self.sincronizar()

    def publicar_o_descartar_contenido(self, item_id, accion):
        if accion == "eliminar":
            self.banco_contenido = [i for i in self.banco_contenido if i["id"] != item_id]
        elif accion == "publicar":
            for i in self.banco_contenido:
                if i["id"] == item_id:
                    i["estado"] = "🚀 Publicado con Éxito"
        self.sincronizar()

    def responder_duda(self, duda_id, respuesta):
        for d in self.dudas_agentes:
            if d["id"] == duda_id:
                d["respuesta"] = respuesta
                d["respondida"] = True
                self.sincronizar()
                break

    def eliminar_elemento_lore(self, elem_id):
        self.lore_universo = [e for e in self.lore_universo if e["id"] != elem_id]
        self.sincronizar()

    def eliminar_pagina_manga(self, pag_id):
        self.paginas_manga = [p for p in self.paginas_manga if p["pag_id"] != pag_id]
        self.sincronizar()

    def eliminar_video_tiktok(self, vid_id):
        self.videos_tiktok = [v for v in self.videos_tiktok if v.get("id") != vid_id]
        self.sincronizar()

    def guardar_credencial_especifica(self, servicio, datos):
        self.credenciales[servicio] = datos
        self.sincronizar()

    def actualizar_metricas_red(self, plat, seg, rend, inter):
        self.metricas_redes[plat] = {
            "seguidores": seg,
            "rendimiento_principal": rend,
            "interacciones": inter,
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.sincronizar()