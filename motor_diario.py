import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

ARCHIVO_DATOS = "datos_saga.json"

class GestorPersistencia:
    @staticmethod
    def cargar_datos():
        datos_por_defecto = {
            "banco_contenido": [], 
            "paginas_manga": [], 
            "videos_tiktok": [],
            "estilo_visual_seleccionado": "Burbujas de Recuerdos (Kingdom Hearts Style)",
            "scripts_personalizados": {
                "prompt_kingdom_hearts": "anime key visual, cinematic illustration, a male protagonist floating backwards upside down in a dark deep blue void, surrounded by glowing translucent soap bubbles and glass spheres, inside each bubble there is a distinct memory scene: {escena}. High detail, Kingdom Hearts art style, digital painting, masterpiece.",
                "prompt_manga": "professional manga page, detailed ink line art, dark fantasy comic book panel, high contrast, screentones, epic composition based on: {escena}",
                "prompt_video": "vertical 9:16 mobile wallpaper aspect ratio, cinematic mockup of a person reading a fantasy novel in a cozy room, {escena}"
            },
            "estado_agentes": "Agencia de Marketing y Co-autoría Activa", 
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
                {"origen": "Cronos (Director)", "mensaje": "Agencia de marketing en marcha. Todos los sistemas operativos listos para impulsar las ventas de la novela."}
            ],
            "propuestas_escritura": []
        }

        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                    datos_cargados = json.load(f)
                    for k, v in datos_por_defecto.items():
                        if k not in datos_cargados or not datos_cargados[k]:
                            datos_cargados[k] = v
                    return datos_cargados
            except Exception:
                pass
        return datos_por_defecto

    @staticmethod
    def guardar_datos(datos):
        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

class AuraCoAutora:
    def redactar_estrategia_multicanal(self, capitulo_texto, num_cap):
        extracto = capitulo_texto[:800] if capitulo_texto else "Escena clave de Los Cinco Reinos."
        return {
            "feed": f"📖 [Campaña de Ventas — Capítulo {num_cap}]\n\n{extracto[:250]}...\n\n💡 Estrategia de conversión: Gancho emocional para captar lectores inmersivos.\n\n#LosCincoReinos #BookTokEspaña #FantasíaOscura #NovelaFantástica",
            "tiktok_reel": f"🎬 [TikTok BookTok Comercial]\nVisual: El protagonista flotando en el abismo rodeado de burbujas con recuerdos del libro.\n\nTexto: '¿Y si el libro que tienes en las manos cobra vida?'\n\n\"{extracto[:200]}...\"",
            "historia": f"⚡ [Story Interactiva] ¿Qué harías si despertaras en el Capítulo {num_cap}? Vota ahora.",
            "estrategia_elegida": "Conversión y retención de lectores"
        }

    def extraer_personajes_automaticamente(self, capitulo_texto, num_cap):
        personajes = []
        texto_lower = capitulo_texto.lower()
        if "joven" in texto_lower or num_cap == 0:
            personajes.append({
                "nombre": "Protagonista (Cap 0)",
                "descripcion": "Joven de dieciséis años, cabello oscuro, ojos azul celeste, flotando en un estado de ingravidez y ensoñación."
            })
        if "madre" in texto_lower or "niña" in texto_lower or num_cap == 1:
            personajes.append({
                "nombre": "Madre e Hija (Cap 1)",
                "descripcion": "Personajes clave atrapados en la tormenta nocturna sobre el océano Pacífico."
            })
        if not personajes:
            personajes.append({
                "nombre": f"Personaje Principal (Cap {num_cap})",
                "descripcion": "Entidad o figura destacada detectada en el capítulo."
            })
        return personajes

    def coautor_continuidad_capitulo(self, idea_usuario, ultimo_texto):
        contexto_previo = ultimo_texto[:600] if ultimo_texto else "Inicio de la obra."
        return (
            f"👑 [Propuesta de Continuación y Corrección — Aura]\n\n"
            f"Basado en tu avance ('{contexto_previo[:150]}...'), aquí tienes una estructura orientada a ventas y retención:\n\n"
            f"--- BORRADOR SUGERIDO ---\n"
            f"La tensión en el ambiente era palpable. [Idea central: {idea_usuario}]. "
            f"El lector necesita sentir el pulso de la escena desde la primera frase...\n"
            f"--------------------------\n\n"
            f"💡 **Consejo de Marketing:** Abre con un conflicto directo o una pregunta sin respuesta para enganchar en los primeros dos párrafos."
        )

class HerculesMangaka:
    def construir_prompt_dinamico(self, estilo, extracto_capitulo, scripts_dict):
        clean_text = extracto_capitulo.replace("\n", " ")[:350]
        if estilo == "Burbujas de Recuerdos (Kingdom Hearts Style)":
            plantilla = scripts_dict.get("prompt_kingdom_hearts", "anime key visual, cinematic illustration, a male protagonist floating backwards upside down in a dark deep blue void, surrounded by glowing translucent soap bubbles and glass spheres, inside each bubble there is a distinct memory scene: {escena}. High detail, Kingdom Hearts art style, digital painting, masterpiece.")
            return plantilla.replace("{escena}", clean_text)
        elif estilo == "Manga Blanco y Negro Tradicional (Ink Lineart)":
            plantilla = scripts_dict.get("prompt_manga", "professional manga page, detailed ink line art, dark fantasy comic book panel, high contrast, screentones, epic composition based on: {escena}")
            return plantilla.replace("{escena}", clean_text)
        else:
            plantilla = scripts_dict.get("prompt_video", "vertical 9:16 mobile wallpaper aspect ratio, cinematic mockup of a person reading a fantasy novel in a cozy room, {escena}")
            return plantilla.replace("{escena}", clean_text)

    def generar_boceto_personaje(self, nombre_pj, descripcion_aura, estilo, scripts_dict):
        prompt_base = self.construir_prompt_dinamico(estilo, f"Character design sheet of {nombre_pj}. {descripcion_aura}", scripts_dict)
        return f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt_base)}?width=800&height=800&nologo=true"

    def estructurar_pagina_manga_fiel(self, num_cap, capitulo_texto, estilo, scripts_dict):
        prompt_base = self.construir_prompt_dinamico(estilo, capitulo_texto, scripts_dict)
        return {
            "pag_id": num_cap,
            "estilo_usado": estilo,
            "escena_resumen": f"Composición visual de marketing para el Capítulo {num_cap}.",
            "guion_viñetas": f"Ilustración comercial de alto impacto.",
            "imagen_url": f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt_base)}?width=900&height=1200&nologo=true",
            "estado": "Imagen Comercial Generada"
        }

    def generar_video_atractivo_tiktok(self, num_cap, capitulo_texto, nuevo_id, estilo, scripts_dict):
        prompt_base = self.construir_prompt_dinamico(estilo, capitulo_texto, scripts_dict)
        return {
            "id": nuevo_id,
            "tipo": "Vídeo BookTok (9:16)",
            "capitulo": num_cap,
            "preview_url": f"https://image.pollinations.ai/prompt/{requests.utils.quote('vertical 9:16 mobile wallpaper aspect ratio, ' + prompt_base)}?width=720&height=1280&nologo=true",
            "guion_voz": f"Locución magnética para TikTok: 'Descubre los secretos del Capítulo {num_cap} de Los Cinco Reinos...'",
            "estado": "Listo para campaña"
        }

class ColmenaBufferInfinito:
    def __init__(self):
        self.aura = AuraCoAutora()
        self.hercules = HerculesMangaka()
        datos = GestorPersistencia.cargar_datos()
        self.banco_contenido = datos.get("banco_contenido", [])
        self.paginas_manga = datos.get("paginas_manga", [])
        self.videos_tiktok = datos.get("videos_tiktok", [])
        self.estilo_visual_seleccionado = datos.get("estilo_visual_seleccionado", "Burbujas de Recuerdos (Kingdom Hearts Style)")
        self.scripts_personalizados = datos.get("scripts_personalizados", {
            "prompt_kingdom_hearts": "anime key visual, cinematic illustration, a male protagonist floating backwards upside down in a dark deep blue void, surrounded by glowing translucent soap bubbles and glass spheres, inside each bubble there is a distinct memory scene: {escena}. High detail, Kingdom Hearts art style, digital painting, masterpiece.",
            "prompt_manga": "professional manga page, detailed ink line art, dark fantasy comic book panel, high contrast, screentones, epic composition based on: {escena}",
            "prompt_video": "vertical 9:16 mobile wallpaper aspect ratio, cinematic mockup of a person reading a fantasy novel in a cozy room, {escena}"
        })
        self.dudas_agentes = datos.get("dudas_agentes", [])
        self.lore_universo = datos.get("lore_universo", [])
        self.credenciales = datos.get("credenciales", {})
        self.metricas_redes = datos.get("metricas_redes", {})
        self.config_temporizador = datos.get("config_temporizador", {"frecuencia": "Cada 6 horas", "activo": True})
        self.chat_colmena = datos.get("chat_colmena", [])
        self.propuestas_escritura = datos.get("propuestas_escritura", [])
        self.estado_agentes = "Agencia de Marketing Operativa"

    def sincronizar(self):
        GestorPersistencia.guardar_datos({
            "banco_contenido": self.banco_contenido,
            "paginas_manga": self.paginas_manga,
            "videos_tiktok": self.videos_tiktok,
            "estilo_visual_seleccionado": self.estilo_visual_seleccionado,
            "scripts_personalizados": self.scripts_personalizados,
            "estado_agentes": self.estado_agentes,
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

        if not any(p["pag_id"] == num_cap for p in self.paginas_manga) and len(capitulo_texto) > 50:
            nueva_pag = self.hercules.estructurar_pagina_manga_fiel(num_cap, capitulo_texto, self.estilo_visual_seleccionado, self.scripts_personalizados)
            self.paginas_manga.append(nueva_pag)

        if not any(b.get("cap_asociado") == num_cap for b in self.banco_contenido) and len(capitulo_texto) > 50:
            copys = self.aura.redactar_estrategia_multicanal(capitulo_texto, num_cap)
            nuevo_vid_id = len(self.videos_tiktok) + 1
            video_rec = self.hercules.generar_video_atractivo_tiktok(num_cap, capitulo_texto, nuevo_vid_id, self.estilo_visual_seleccionado, self.scripts_personalizados)
            self.videos_tiktok.append(video_rec)
            self.banco_contenido.append({
                "id": len(self.banco_contenido) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "cap_asociado": num_cap,
                "copys": copys,
                "estado": "Campaña de Ventas Lista"
            })
        self.sincronizar()

    def obtener_capitulo(self, num):
        rutas = [f"capitulo {num}.txt", f"capitulo_{num}.txt", os.path.join("capitulos", f"capitulo {num}.txt")]
        for r in rutas:
            if os.path.exists(r):
                try:
                    with open(r, "r", encoding="utf-8") as f:
                        return {"titulo": f"Capítulo {num}: Los Cinco Reinos", "descripcion": f.read()}
                except Exception as e:
                    return {"titulo": f"Capítulo {num}", "descripcion": f"Error al leer archivo: {e}"}
        return {"titulo": f"Capítulo {num}", "descripcion": f"⚠️ Sube el archivo 'capitulo {num}.txt' en la carpeta raíz de tu repositorio para que la agencia lo procese."}

    def publicar_o_descartar_contenido(self, item_id, accion):
        if accion == "eliminar":
            self.banco_contenido = [i for i in self.banco_contenido if i["id"] != item_id]
        elif accion == "publicar":
            for i in self.banco_contenido:
                if i["id"] == item_id:
                    i["estado"] = "🚀 Publicado en Redes con Éxito"
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