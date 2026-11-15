import streamlit as st
import time

st.set_page_config(
    page_title="Oficina Central - Los Cinco Reinos",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Oficina Central - Los Cinco Reinos")
st.markdown("Tu equipo trabaja codo a codo. Aura analiza el lore y Hércules genera el arte visual y las escenas de tus personajes.")

# Layout en 3 columnas para los agentes
col1, col2, col3 = st.columns(3)

# --- COLUMNA 1: AURA (Analista Textual) ---
with col1:
    st.markdown("### 📖 Aura")
    st.caption("Analista Textual (Lore con IA)")
    
    st.info("Lee los capítulos en segundo plano y extrae personajes.")
    
    if "aura_status" not in st.session_state:
        st.session_state.aura_status = "Inactivo"

    if st.session_state.aura_status == "Trabajando":
        st.warning("🔄 Aura está trabajando en segundo plano...")
    else:
        st.success("✅ Aura en línea.")

    if st.button("🔍 Ordenar a Aura escanear en 2º plano"):
        st.session_state.aura_status = "Trabajando"
        with st.spinner("Aura analizando capítulos y extrayendo entidades..."):
            time.sleep(2)
        st.session_state.aura_status = "Completado"
        st.rerun()

# --- COLUMNA 2: HÉRCULES (Director Gráfico y Visual) ---
with col2:
    st.markdown("### 🎨 Hércules")
    st.caption("Director Gráfico y Visual")
    
    personaje = st.selectbox("Personaje en escena:", ["Hugo", "A'ial", "Sky Slimboard", "Fengro", "Oxtor"])
    
    st.markdown("✍️ **Indícale cambios de apariencia a Hércules:**")
    prompt_apariencia = st.text_area(
        "Prompt de modificación",
        value="pelo corto con aspecto más europeo y que vista moderno",
        height=100
    )
    
    if st.button("🖼️ Ordenar a Hércules Renderizar Imagen Real"):
        with st.spinner(f"Hércules generando arte cinematográfico para {personaje}..."):
            time.sleep(3)
        st.success("✨ ¡Imagen cinematográfica generada con éxito!")
        # Aquí puedes integrar la llamada a generación de imágenes si usas alguna API (como DALL-E / Stable Diffusion)

# --- COLUMNA 3: DANTE & KIRA (Copywriting & SEO) ---
with col3:
    st.markdown("### ✍️ Dante & Kira")
    st.caption("Copywriting & SEO")
    
    st.markdown(
        """<div style='background-color: #fdf8e2; padding: 10px; border-radius: 5px; border: 1px solid #e6dbb9;'>
        Redactando ganchos y optimizando hashtags para Instagram y TikTok.
        </div>""", 
        unsafe_allow_html=True
    )
    
    if st.button("💬 Consultar a Dante"):
        st.info("Dante: *'Recuerda enfatizar la tensión y el misterio en el próximo post para enganchar a los lectores en TikTok.'*")