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
            "estado_agentes": "Control Manual y Coherente", 
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
                texto_extraido = " ".join([p.get_text() for p in parrafos])
                if len(texto_extraido) > 200:
                    return texto_extraido[:3000]
            return "No se pudo extraer texto estructurado de la URL proporcionada."
        except Exception as e:
            return f"Error de conexión con Wattpad: {e}"

    def redactar_con_coherencia(self, instruccion_usuario, lore_previo, capitulo_texto):
        contexto_base = capitulo_texto[:500] if capitulo_texto else "Sin capítulo seleccionado."
        return f"[Aura - Borrador Coherente] Basado estrictamente en tu obra y directriz ('{instruccion_usuario}'). Contexto analizado: {contexto_base}..."

class HerculesMangaka:
    def estructurar_plancha_real(self, num_cap, capitulo_texto):
        extracto = capitulo_texto[:300] if capitulo_texto else "Trama oficial de la saga."
        return {
            "pag_id": num_cap,
            "escena": f"Adaptación fiel del Capítulo {num_cap}",
            "guion_viñetas": f"Viñeta 1 (Inicio): Presentación de la escena basada en el texto real. | Viñeta 2 (Nudo): Desarrollo fiel. | Extracto de referencia: {extracto}",
            "imagen_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop",
            "correcciones": []
        }

class ColmenaBufferInfinito:
    def __init__(self):
        self.aura = AuraCoAutora()
        self.hercules = HerculesMangaka()
        datos = GestorPersistencia.cargar_datos()
        self.banco_contenido_semanal = datos.get("banco_contenido", [])
        self.paginas_manga = datos.get("paginas_manga", [])
        self.lore_wattpad = datos.get("lore_wattpad", "")
        self.dudas_agentes = datos.get("dudas_agentes", [])
        self.lore_universo = datos.get("lore_universo", [])
        self.credenciales = datos.get("credenciales", {})
        self.metricas_redes = datos.get("metricas_redes", {})
        self.estado_agentes = "Modo Asistido y Coherente"

    def sincronizar(self):
        GestorPersistencia.guardar_datos({
            "banco_contenido": self.banco_contenido_semanal,
            "paginas_manga": self.paginas_manga,
            "estado_agentes": self.estado_agentes,
            "lore_wattpad": self.lore_wattpad,
            "dudas_agentes": self.dudas_agentes,
            "lore_universo": self.lore_universo,
            "credenciales": self.credenciales,
            "metricas_redes": self.metricas_redes
        })

    def asimilar_historia_wattpad(self, url):
        texto_leido = self.aura.leer_wattpad(url)
        self.lore_wattpad = texto_leido
        self.sincronizar()
        return texto_leido

    def obtener_capitulo(self, num):
        posibles_rutas = [
            f"capitulo {num}.txt",
            f"capitulo_{num}.txt",
            os.path.join("capitulos", f"capitulo {num}.txt"),
            os.path.join("capitulos", f"capitulo_{num}.txt")
        ]
        descripcion_texto = ""
        encontrado = False
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                try:
                    with open(ruta, "r", encoding="utf-8") as f:
                        descripcion_texto = f.read()
                        encontrado = True
                        break
                except Exception as e:
                    descripcion_texto = f"Error al leer el archivo: {e}"
                    encontrado = True
                    break
        if not encontrado:
            descripcion_texto = f"Aún no se ha encontrado el archivo para el Capítulo {num} en la raíz del repositorio."
        return {
            "titulo": f"Capítulo {num}: Los Cinco Reinos",
            "descripcion": descripcion_texto
        }

    def generar_dudas_automaticas_capitulo(self, num_cap, capitulo_texto):
        existentes = [d for d in self.dudas_agentes if f"Capítulo {num_cap}" in d.get("pregunta", "")]
        if existentes:
            return

        duda_aura = {
            "id": len(self.dudas_agentes) + 1,
            "agente": "Aura (Co-autora)",
            "pregunta": f"[Capítulo {num_cap}] ¿Cuál debe ser el enfoque emocional principal de los personajes en esta escena y qué tono de tensión buscas?",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "respondida": False,
            "respuesta": ""
        }
        self.dudas_agentes.append(duda_aura)

        duda_hercules = {
            "id": len(self.dudas_agentes) + 2,
            "agente": "Hércules (Mangaka)",
            "pregunta": f"[Capítulo {num_cap}] ¿Qué elemento visual clave o escenario principal quieres que destaque obligatoriamente en la plancha de este capítulo?",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "respondida": False,
            "respuesta": ""
        }
        self.dudas_agentes.append(duda_hercules)
        self.sincronizar()

    def generar_contenido_manual(self, instruccion, num_cap):
        info_cap = self.obtener_capitulo(num_cap)
        texto_generado = self.aura.redactar_con_coherencia(instruccion, self.lore_wattpad, info_cap["descripcion"])
        
        nuevo_item = {
            "id": len(self.banco_contenido_semanal) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "texto": texto_generado,
            "cap_asociado": num_cap,
            "estado": "Revisión Requerida"
        }
        self.banco_contenido_semanal.append(nuevo_item)
        self.sincronizar()
        return nuevo_item

    def generar_manga_manual(self, num_cap):
        info_cap = self.obtener_capitulo(num_cap)
        nueva_pag = self.hercules.estructurar_plancha_real(num_cap, info_cap["descripcion"])
        self.paginas_manga.append(nueva_pag)
        self.sincronizar()

    def registrar_duda(self, pregunta, agente):
        self.dudas_agentes.append({
            "id": len(self.dudas_agentes) + 1,
            "agente": agente,
            "pregunta": pregunta,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "respondida": False,
            "respuesta": ""
        })
        self.sincronizar()

    def responder_duda(self, duda_id, respuesta):
        for d in self.dudas_agentes:
            if d["id"] == duda_id:
                d["respuesta"] = respuesta
                d["respondida"] = True
                self.sincronizar()
                break

    def guardar_elemento_lore(self, categoria, nombre, descripcion):
        nuevo_elemento = {
            "id": len(self.lore_universo) + 1,
            "categoria": categoria,
            "nombre": nombre,
            "descripcion": descripcion,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.lore_universo.append(nuevo_elemento)
        self.sincronizar()

    def eliminar_elemento_lore(self, elemento_id):
        self.lore_universo = [e for e in self.lore_universo if e["id"] != elemento_id]
        self.sincronizar()

    def eliminar_item_banco(self, item_id):
        self.banco_contenido_semanal = [i for i in self.banco_contenido_semanal if i["id"] != item_id]
        self.sincronizar()

    def eliminar_plancha_manga(self, pag_id):
        self.paginas_manga = [p for p in self.paginas_manga if p["pag_id"] != pag_id]
        self.sincronizar()

    def guardar_correccion_manga(self, pag_id, nota):
        for pag in self.paginas_manga:
            if pag["pag_id"] == pag_id:
                pag["correcciones"].append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "nota": nota
                })
                self.sincronizar()
                break

    def guardar_credencial(self, servicio, token):
        self.credenciales[servicio] = token
        self.sincronizar()

    def actualizar_metricas_red(self, plataforma, seguidores, rendimiento_principal, interacciones):
        self.metricas_redes[plataforma] = {
            "seguidores": seguidores,
            "rendimiento_principal": rendimiento_principal,
            "interacciones": interacciones,
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.sincronizar()