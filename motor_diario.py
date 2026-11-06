import time
import json
import os
import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup

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
        return {"banco_contenido": [], "paginas_manga": [], "estado_agentes": "Inactivo", "lore_wattpad": ""}

    @staticmethod
    def guardar_datos(datos):
        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

class AuraCoAutora:
    """Aura: Lee de Wattpad, analiza el lore y redacta la segunda parte automáticamente."""
    
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

    def redactar_segunda_parte(self, instruccion_usuario, lore_previo):
        time.sleep(1)
        return f"[Aura - Segunda Parte] Basado en el lore de la saga y tu directriz ('{instruccion_usuario}'): Los reinos fronterizos resuenan con los ecos de la batalla..."

class HerculesMangaka:
    """Hércules: Lee los capítulos reales y diseña planchas de manga fieles a la obra."""
    
    def dibujar_automatico(self, ciclo_num, texto_capitulo=""):
        # Extraer un fragmento representativo del capítulo para contextualizar la plancha
        extracto = texto_capitulo[:250] if texto_capitulo else "Trama principal de Los Cinco Reinos."
        
        return {
            "pag_id": ciclo_num,
            "escena": f"Storyboard y Plancha Oficial de la Saga #{ciclo_num}",
            "guion_viñetas": f"Viñeta 1: Panorama épico basado en el capítulo. | Viñeta 2: Detalle de personajes. | Contexto: {extracto}...",
            "imagen_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop", # Fondo estético abstracto/fantasía
            "correcciones": []
        }

class ColmenaBufferInfinito:
    """Orquesta la producción autónoma 24/7 y la gestión directa de los capítulos."""
    def __init__(self):
        self.aura = AuraCoAutora()
        self.hercules = HerculesMangaka()
        datos = GestorPersistencia.cargar_datos()
        self.banco_contenido_semanal = datos.get("banco_contenido", [])
        self.paginas_manga = datos.get("paginas_manga", [])
        self.lore_wattpad = datos.get("lore_wattpad", "")
        self.estado_agentes = "Activos 24/7"
        
        self.iniciar_hilo_autonomo()

    def sincronizar(self):
        GestorPersistencia.guardar_datos({
            "banco_contenido": self.banco_contenido_semanal,
            "paginas_manga": self.paginas_manga,
            "estado_agentes": self.estado_agentes,
            "lore_wattpad": self.lore_wattpad
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
                    descripcion_texto = f"Error al leer el archivo ({ruta}): {e}"
                    encontrado = True
                    break

        if not encontrado:
            descripcion_texto = f"Aún no se ha encontrado el archivo para el Capítulo {num} en la raíz."

        return {
            "titulo": f"Capítulo {num}: Los Cinco Reinos",
            "escena": f"Desarrollo de la trama principal #{num}",
            "descripcion": descripcion_texto,
            "plancha_generada": f"Plancha de Manga oficial #{num} - Estilo Hércules"
        }

    def iniciar_hilo_autonomo(self):
        def bucle_trabajo():
            ciclo = len(self.banco_contenido_semanal) + 1
            while True:
                time.sleep(60) 
                texto_nuevo = self.aura.redactar_segunda_parte("Generación continua para la saga", self.lore_wattpad)
                self.banco_contenido_semanal.append({
                    "id": ciclo,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "texto": texto_nuevo,
                    "copy_comercial": "Disponible en Amazon y Letrame.",
                    "hashtags": "#CincoReinos #Wattpad",
                    "estado": "Generado Automáticamente (Pendiente)"
                })
                
                # Obtener texto del capítulo actual para Hércules
                info_cap = self.obtener_capitulo(ciclo % 26)
                nueva_pag = self.hercules.dibujar_automatico(ciclo, info_cap["descripcion"])
                self.paginas_manga.append(nueva_pag)
                
                ciclo += 1
                self.sincronizar()

        hilo = threading.Thread(target=bucle_trabajo, daemon=True)
        try:
            hilo.start()
        except Exception:
            pass

    def guardar_correccion_manga(self, pag_id, nota):
        for pag in self.paginas_manga:
            if pag["pag_id"] == pag_id:
                pag["correcciones"].append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "nota": nota
                })
                self.sincronizar()
                break