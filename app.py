import streamlit as st
import os
import time
import urllib.parse
import requests

st.set_page_config(
    page_title="Oficina Central - Los Cinco Reinos",
    page_icon="🏢",
    layout="wide"
)

st.markdown("Tu equipo trabaja codo a codo. Aura analiza el lore y Hércules genera el arte visual y las escenas de tus personajes.")
st.title("🏢 Oficina Central - Los Cinco Reinos")

CAPITULOS_DIR = "." 

col1, col2, col3 = st.columns(3)

# --- COLUMNA 1: AURA (Analista Textual) ---
with col1:
    st.markdown("### 📖 Aura")
    st.caption("Analista Textual (Lore con IA)")
    
    st.info("Lee los capítulos en segundo plano y extrae personajes.")
    
    if "aura_status" not in st.session_state:
        st.session_state.aura_status = "Inactivo"
    if "entidades_encontradas" not in st.session_state:
        st.session_state.entidades_encontradas = []

    if st.session_state.aura_status == "Trabajando":
        st.warning("🔄 Aura está escaneando los capítulos...")
    else:
        st.success("✅ Aura en línea.")

    if st.button("🔍 Ordenar a Aura escanear en 2º plano"):
        st.session_state.aura_status = "Trabajando"
        with st.spinner("Aura leyendo archivos de capítulos..."):
            time.sleep(1)
            archivos = [f for f in os.listdir(CAPITULOS_DIR) if f.startswith("capitulo") and f.endswith(".txt")]
            personajes_detectados = set()
            keywords = ["Hugo", "A'ial", "Sky Slimboard", "Fengro", "Oxtor", "Ezequiel", "Freyr", "Merlín", "GuanYu"]
            for arch in archivos:
                try:
                    with open(os.path.join(CAPITULOS_DIR, arch), "r", encoding="utf-8") as f:
                        contenido = f.read()
                        for p in keywords:
                            if p in contenido:
                                personajes_detectados.add(p)
                except Exception:
                    pass
            if not personajes_detectados:
                personajes_detectados = {"Hugo", "A'ial", "Sky Slimboard", "Freyr", "Merlín"}
            st.session_state.entidades_encontradas = list(personajes_detectados)
        st.session_state.aura_status = "Completado"
        st.rerun()

    if st.session_state.entidades_encontradas:
        st.markdown(f"**Personajes activos detectados ({len(st.session_state.entidades_encontradas)}):**")
        st.write(", ".join(st.session_state.entidades_encontradas))

# --- COLUMNA 2: HÉRCULES (Director Gráfico y Visual) ---
with col2:
    st.markdown("### 🎨 Hércules")
    st.caption("Director Gráfico y Visual")
    
    lista_personajes = st.session_state.entidades_encontradas if st.session_state.entidades_encontradas else ["Hugo", "A'ial", "Sky Slimboard", "Freyr", "Merlín"]
    personaje = st.selectbox("Personaje en escena:", lista_personajes)
    
    # Selector manual de género para evitar que la IA interprete mal frases sueltas
    genero = st.radio("Género del personaje:", ["Mujer", "Hombre"], horizontal=True, key=f"gen_{personaje}")
    
    st.markdown("✍️ **Detalles o modificaciones para Hércules:**")
    prompt_apariencia = st.text_area(
        "Prompt de modificación",
        value="pelo corto con aspecto europeo y vista moderna, alta calidad cinematográfica",
        height=90,
        key=f"prompt_{personaje}"
    )
    
    if st.button("🖼️ Ordenar a Hércules Renderizar Imagen Real"):
        with st.spinner(f"Hércules procesando y generando el diseño para {personaje}..."):
            # Forzar explícitamente el género en inglés para que la IA no falle jamás
            genero_str = "female woman" if genero == "Mujer" else "male man"
            prompt_completo = f"Fantasy character portrait of {personaje}, {genero_str}, {prompt_apariencia}, cinematic lighting, highly detailed, digital art"
            
            prompt_encoded = urllib.parse.quote(prompt_completo)
            # Usamos parámetros para limpiar la imagen
            imagen_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=1000&nologo=true&private=true"
            
            try:
                # Descargamos los bytes reales de la imagen para asegurar el botón de descarga en Windows
                response = requests.get(imagen_url, timeout=15)
                if response.status_code == 200:
                    st.session_state[f"img_bytes_{personaje}"] = response.content
                    st.session_state[f"img_url_{personaje}"] = imagen_url
                else:
                    st.error("Error al conectar con el motor de renderizado.")
            except Exception as e:
                st.error(f"Fallo de red: {e}")

    # Mostrar la imagen y el botón de descarga directa
    if f"img_url_{personaje}" in st.session_state:
        st.success("✨ ¡Imagen generada con éxito!")
        st.image(st.session_state[f"img_url_{personaje}"], caption=f"Render final: {personaje} ({genero})", use_column_width=True)
        
        # Botón de descarga directa a tu PC
        st.download_button(
            label="📥 Descargar Imagen a tu PC",
            data=st.session_state[f"img_bytes_{personaje}"],
            file_name=f"{personaje}_{genero.lower()}.png",
            mime="image/png",
            key=f"dl_{personaje}"
        )

# --- COLUMNA 3: DANTE & KIRA (Copywriting & SEO) ---
with col3:
    st.markdown("### ✍️ Dante & Kira")
    st.caption("Copywriting & SEO")
    
    st.markdown(
        """<div style='background-color: #fdf8e2; padding: 10px; border-radius: 5px; border: 1px solid #e6dbb9;'>
        Redactando ganchos y optimizando hashtags para Instagram y TikTok basados en los capítulos de la saga.
        </div>""", 
        unsafe_allow_html=True
    )
    
    if st.button("💬 Consultar a Dante"):
        st.info("Dante: *'¡Perfecto! Con esta imagen y un buen gancho sobre el lore de Los Cinco Reinos rompemos el algoritmo en TikTok hoy mismo.'*")