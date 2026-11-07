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
            "estilo_visual_seleccionado": "Burbujas de Recuerdos (Kingdom Hearts Style)",
            "scripts_personalizados": {
                "prompt_kingdom_hearts": "anime key visual, cinematic illustration, a male protagonist floating backwards upside down in a dark deep blue void, surrounded by glowing translucent soap bubbles and glass spheres, inside each bubble there is a distinct memory scene: {escena}. High detail, Kingdom Hearts art style, digital painting, masterpiece.",
                "prompt_manga": "professional manga page, detailed ink line art, dark fantasy comic book panel, high contrast, screentones, epic composition based on: {escena}",
                "prompt_video": "vertical 9:16 mobile wallpaper aspect ratio, cinematic mockup of a person reading a fantasy novel in a cozy room, {escena}"
            },
            "estado_agentes": "Co-autoría literaria y generador de continuidad activo", 
            "lore_wattpad": "", 
            "dudas_agentes": [],
            "lore_universo": [],
            "credenciales": {},
            "metricas_redes": {
                "Instagram": {"seguidores": 1420, "rendimiento_principal": 84, "interacciones": 310, "ultima_actualizacion": "Hoy"},
                "TikTok": {"seguidores": 2890, "rendimiento_principal": 92, "interacciones": 750, "ultima_actualizacion": "Hoy"},
                "Twitter (X)": {"seguidores": 610, "rendimiento_principal": 65, "interacciones": 120, "ultima_actualizacion": "Hoy"}
            },
            "config_temporizador": {"frecuencia": "Cada 6 horas", "activo": True, "ultima_ejecucion": "Nunca"},
            "chat_colmena": [
                {"origen": "Aura", "mensaje": "Módulo de co-autoría y continuidad literaria preparado. Dime qué tienes en mente para el siguiente capítulo y te redactaré una propuesta con ganchos amenos para atrapar al lector."}
            ]
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

    def redactar_estrategia_multicanal(self, capitulo_texto, num_cap):
        extracto = capitulo_texto[:800] if capitulo_texto else "Escena clave de Los Cinco Reinos."
        return {
            "feed": f"📖 [Campaña Visual — Capítulo {num_cap}]\n\n{extracto[:250]}...\n\n#LosCincoReinos #DarkFantasy #BookTokEspaña",
            "tiktok_reel": f"🎬 [TikTok BookTok Inmersivo]\nVisual: Protagonista flotando rodeado de burbujas con recuerdos del libro.\n\nExtracto: \"{extracto[:200]}...\"",
            "historia": f"⚡ [Story] ¿Qué recuerdo guardarías en una burbuja del Capítulo {num_cap}?",
            "estrategia_elegida": "Metáfora de burbujas de recuerdos"
        }

    def extraer_personajes_automaticamente(self, capitulo_texto, num_cap):
        if "joven flotaba" in capitulo_texto.lower() or num_cap == 0:
            return [{
                "nombre": "Protagonista sin nombre (Cap 0)",
                "descripcion": "Joven de 16 años con traje táctico oscuro, flotando en el vacío profundo rodeado de esferas de cristal y recuerdos."
            }]
        elif "tormentosa" in capitulo_texto.lower() or num_cap == 1:
            return [{
                "nombre": "Madre e hija en la tormenta",
                "descripcion": "Niña pequeña y su madre en el avión bajo la tempestad del Pacífico."
            }]
        return []

    def coautor_continuidad_capitulo(self, idea_usuario, ultimo_texto):
        # Aura redacta una propuesta de continuación y corrección orientada a dinamismo y retención
        contexto_previo = ultimo_texto[:600] if ultimo_texto else "Inicio de la obra."
        propuesta = (
            f"👑 [Propuesta de Continuación y Corrección — Aura]\n\n"
            f"Basado en tu avance anterior ('{contexto_previo[:150]}...'), aquí tienes una estructura redactada para hacer el capítulo más ameno, "
            f"con un gancho fuerte al principio y tensión narrativa:\n\n"
            f"--- BORRADOR SUGERIDO ---\n"
            f"La brisa cortaba como cuchillas de obsidiana. [Idea central introducida: {idea_usuario}]. "
            f"El protagonista sintió que el tiempo se dilataba, obligando al lector a cuestionar cada certeza previa...\n"
            f"--------------------------\n\n"
            f"💡 **Consejo de Aura para atrapar al lector:** Te sugiero abrir con un diálogo corto y enigmático en lugar de una descripción larga, "
            f"para enganchar inmediatamente la atención en los primeros tres párrafos."
        )
        return propuesta

class HerculesMangaka:
    def construir_prompt_dinamico(self, estilo, extracto_capitulo, scripts_dict):
        clean_text = extracto_capitulo.replace("\n", " ")[:350]
        if estilo == "Burbujas de Recuerdos (Kingdom Hearts Style)":
            plantilla = scripts_dict.get("prompt_kingdom_hearts", "")
            return plantilla.replace("{escena}", clean_text)
        elif estilo == "Manga Blanco y Negro Tradicional (Ink Lineart)":
            plantilla = scripts_dict.get("prompt_manga", "")
            return plantilla.replace("{escena}", clean_text)
        else:
            plantilla = scripts_dict.get("prompt_video", "")
            return plantilla.replace("{escena}", clean_text)

    def generar_boceto_personaje(self, nombre_pj, descripcion_aura, estilo, scripts_dict):
        prompt_base = self.construir_prompt_dinamico(estilo, f"Character design sheet of {nombre_pj}. {descripcion_aura}", scripts_dict)
        return f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt_base)}?width=800&height=800&nologo=true"

    def estructurar_pagina_manga_fiel(self, num_cap, capitulo_texto, estilo, scripts_dict):
        prompt_base = self.construir_prompt_dinamico(estilo, capitulo_texto, scripts_dict)
        return {
            "pag_id": num_cap,
            "estilo_usado": estilo,
            "escena_resumen": f"Composición conceptual basada en el Capítulo {num_cap}.",
            "guion_viñetas": f"Ilustración narrativa principal.",
            "imagen_url": f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt_base)}?width=900&height=1200&nologo=true",
            "estado": "Imagen Generada con Script Exacto"
        }

    def generar_video_atractivo_tiktok(self, num_cap, capitulo_texto, nuevo_id, estilo, scripts_dict):
        prompt_base = self.construir_prompt_dinamico(estilo, capitulo_texto, scripts_dict)
        return {
            "id": nuevo_id,
            "tipo": "Vídeo BookTok (9:16)",
            "capitulo": num_cap,
            "preview_url": f"https://image.pollinations.ai/prompt/{requests.utils.quote('vertical 9:16 mobile wallpaper aspect ratio, ' + prompt_base)}?width=720&height=1280&nologo=true",
            "guion_voz": f"Locución: 'Capítulo {num_cap} de Los Cinco Reinos...'",
            "estado": "Listo"
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
        self.estilo_visual_seleccionado = datos.get("estilo_visual_seleccionado", "Burbujas de Recuerdos (Kingdom Hearts Style)")
        self.scripts_personalizados = datos.get("scripts_personalizados", {})
        self.config_temporizador = datos.get("config_temporizador", {"frecuencia": "Cada 6 horas", "activo": True, "ultima_ejecucion": "Nunca"})
        self.chat_colmena = datos.get("chat_colmena", [])
        self.propuestas_escritura = datos.get("propuestas_escritura", [])
        self.estado_agentes = "Sistema operativo y co-autoría activa"

    def sincronizar(self):
        GestorPersistencia.guardar_datos({
            "banco_contenido": self.banco_contenido,
            "paginas_manga": self.paginas_manga,
            "videos_tiktok": self.videos_tiktok,
            "estilo_visual_seleccionado": self.estilo_visual_seleccionado,
            "scripts_personalizados": self.scripts_personalizados,
            "estado_agentes": self.estado_agentes,
            "lore_wattpad": self.lore_wattpad,
            "dudas_agentes": self.dudas_agentes,
            "lore_universo": self.lore_universo,
            "credenciales": self.credenciales,
            "metricas_redes": self.metricas_redes,
            "config_temporizador": self.config_temporizador,
            "chat_colmena": self.chat_colmena,
            "propuestas_escritura": self.propuestas_escritura
        })

    def generar_ayuda_continuacion(self, idea_usuario, num_cap_referencia):
        info_cap = self.obtener_capitulo(num_cap_referencia)
        propuesta = self.aura.coautor_continuidad_capitulo(idea_usuario, info_cap["descripcion"])
        self.propuestas_escritura.append({
            "id": len(self.propuestas_escritura) + 1,
            "capitulo_ref": num_cap_referencia,
            "idea": idea_usuario,
            "resultado": propuesta,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self.sincronizar()
        return propuesta

    def cambiar_estilo_arte(self, nuevo_estilo):
        self.estilo_visual_seleccionado = nuevo_estilo
        self.sincronizar()

    def guardar_scripts_personalizados(self, scripts):
        self.scripts_personalizados = scripts
        self.sincronizar()

    def ciclo_autonomo_marketing_inteligente(self, num_cap, capitulo_texto):
        pjs_detectados = self.aura.extraer_personajes_automaticamente(capitulo_texto, num_cap)
        for pj in pjs_detectados:
            if not any(p["nombre"] == pj["nombre"] for p in self.lore_universo):
                boceto = self.hercules.generar_boceto_personaje(pj["nombre"], pj["descripcion"], self.estilo_visual_seleccionado, self.scripts_personalizados)
                self.lore_universo.append({
                    "id": len(self.lore_universo) + 1,
                    "categoria": "Personaje",
                    "nombre": pj["nombre"],
                    "descripcion": pj["descripcion"],
                    "boceto_url": boceto,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                })

        if not any(p["pag_id"] == num_cap for p in self.paginas_manga) and len(capitulo_texto) > 100:
            nueva_pag = self.hercules.estructurar_pagina_manga_fiel(num_cap, capitulo_texto, self.estilo_visual_seleccionado, self.scripts_personalizados)
            self.paginas_manga.append(nueva_pag)

        if not any(b.get("cap_asociado") == num_cap for b in self.banco_contenido) and len(capitulo_texto) > 100:
            copys = self.aura.redactar_estrategia_multicanal(capitulo_texto, num_cap)
            nuevo_vid_id = len(self.videos_tiktok) + 1
            video_rec = self.hercules.generar_video_atractivo_tiktok(num_cap, capitulo_texto, nuevo_vid_id, self.estilo_visual_seleccionado, self.scripts_personalizados)
            self.videos_tiktok.append(video_rec)
            self.banco_contenido.append({
                "id": len(self.banco_contenido) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "cap_asociado": num_cap,
                "copys": copys,
                "estado": "Campaña Generada"
            })
        self.sincronizar()

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
            desc = f"Capítulo {num} pendiente de carga en la raíz como archivo .txt."
        return {"titulo": f"Capítulo {num}: Los Cinco Reinos", "descripcion": desc}

    def publicar_o_descartar_contenido(self, item_id, accion):
        if accion == "eliminar":
            self.banco_contenido = [i for i in self.banco_contenido if i["id"] != item_id]
        elif accion == "publicar":
            for i in self.banco_contenido:
                if i["id"] == item_id:
                    i["estado"] = "🚀 Publicado"
        self.sincronizar()

    def responder_duda(self, duda_id, respuesta):
        for d in self.dudas_agentes:
            if d["id"] == duda_id:
                d["respuesta"] = respuesta
                d["respondida"] = True
                self.sincronizar()
                break

    def enviar_mensaje_chat(self, emisor, texto):
        self.chat_colmena.append({"origen": emisor, "mensaje": texto})
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

    def guardar_config_temporizador(self, frecuencia, activo):
        self.config_temporizador = {"frecuencia": frecuencia, "activo": activo, "ultima_ejecucion": datetime.now().strftime("%Y-%m-%d %H:%M")}
        self.sincronizar()