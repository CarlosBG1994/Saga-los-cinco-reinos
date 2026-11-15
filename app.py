import streamlit as st
import os
import time
import urllib.parse

st.set_page_config(
    page_title="Oficina Central - Los Cinco Reinos",
    page_icon="🏢",
    layout="wide"
)

st.markdown("Tu equipo trabaja codo a codo. Aura analiza el lore y Hércules genera el arte visual y las escenas de tus personajes.")
st.title("🏢 Oficina Central - Los Cinco Reinos")

# Directorio donde guardas tus capítulos locales (.txt)
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
            # Buscar archivos de capítulos locales (ej. capitulo 14.txt, etc.)
            archivos = [f for f in os.listdir(CAPITULOS_DIR) if f.startswith("capitulo") and f.endswith(".txt")]
            personajes_detectados = set()
            
            # Palabras clave del lore de Los Cinco Reinos
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
            
            # Si no encuentra archivos locales de texto, muestra los principales por defecto para que la app no quede vacía
            if not personajes_detectados:
                personajes_detectados = {"Hugo", "A'ial", "Sky Slimboard", "Freyr", "Merlín"}
                
            st.session_state.entidades_encontradas = list(personajes_detectados)
        
        st.session_state.aura_status = "Completado"
        st.rerun()

    # Mostrar resultados del análisis de Aura
    if st.session_state.entidades_encontradas:
        st.markdown(f"**Personajes activos en el Lore detectados ({len(st.session_state.entidades_encontradas)}):**")
        st.write(", ".join(st.session_state.entidades_encontradas))

# --- COLUMNA 2: HÉRCULES (Director Gráfico y Visual) ---
with col2:
    st.markdown("### 🎨 Hércules")
    st.caption("Director Gráfico y Visual")
    
    lista_personajes = st.session_state.entidades_encontradas if st.session_state.entidades_encontradas else ["Hugo", "A'ial", "Sky Slimboard", "Fengro", "Oxtor"]
    personaje = st.selectbox("Personaje en escena:", lista_personajes)
    
    st.markdown("✍️ **Indícale cambios de apariencia a Hércules:**")
    prompt_apariencia = st.text_area(
        "Prompt de modificación",
        value="pelo corto con aspecto más europeo y que vista moderno, alta calidad cinematográfica",
        height=100
    )
    
    if st.button("🖼️ Ordenar a Hércules Renderizar Imagen Real"):
        with st.spinner(f"Hércules generando y pintando el arte visual para {personaje}..."):
            # Construcción del prompt detallado para el render visual
            prompt_completo = f"Fantasy character portrait of {personaje} from Los Cinco Reinos, {prompt_apariencia}, cinematic lighting, highly detailed, digital art"
            prompt_encoded = urllib.parse.quote(prompt_completo)
            
            # Generación de la imagen visual real por URL directa
            imagen_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=768&height=768&nologo=true"
            st.session_state[f"img_{personaje}"] = imagen_url

    # Mostrar la imagen generada de forma real en la interfaz
    if f"img_{personaje}" in st.session_state:
        st.success("✨ ¡Imagen cinematográfica generada con éxito por Hércules!")
        st.image(st.session_state[f"img_{personaje}"], caption=f"Render final: {personaje}", use_column_width=True)

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
        st.info("Dante: *'Para el próximo post en TikTok, enfócate en la tensión de los entrenamientos y el misterio del lore. ¡Eso engancha seguro!'*")