import streamlit as st
import os
import time

st.set_page_config(
    page_title="Oficina Central - Los Cinco Reinos",
    page_icon="🏢",
    layout="wide"
)

st.markdown("Tu equipo trabaja codo a codo. Aura analiza el lore y Hércules genera el arte visual y las escenas de tus personajes.")
st.title("🏢 Oficina Central - Los Cinco Reinos")

# Directorio donde guardas tus capítulos (puedes adaptarlo o dejarlo en la carpeta actual)
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
            
            # Lógica simple de lectura para extraer menciones clave del lore
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
            
            st.session_state.entidades_encontradas = list(personajes_detectados)
        
        st.session_state.aura_status = "Completado"
        st.rerun()

    # Mostrar resultados del análisis de Aura si ya ha escaneado
    if st.session_state.entidades_encontradas:
        st.markdown(f"**Personajes activos en el Lore detectados ({len(st.session_state.entidades_encontradas)}):**")
        st.write(", ".join(st.session_state.entidades_encontradas))

# --- COLUMNA 2: HÉRCULES (Director Gráfico y Visual) ---
with col2:
    st.markdown("### 🎨 Hércules")
    st.caption("Director Gráfico y Visual")
    
    # Permitir elegir personaje basándonos también en lo que Aura detectó si existe
    lista_personajes = st.session_state.entidades_encontradas if st.session_state.entidades_encontradas else ["Hugo", "A'ial", "Sky Slimboard", "Fengro", "Oxtor"]
    personaje = st.selectbox("Personaje en escena:", lista_personajes)
    
    st.markdown("✍️ **Indícale cambios de apariencia a Hércules:**")
    prompt_apariencia = st.text_area(
        "Prompt de modificación",
        value="pelo corto con aspecto más europeo y que vista moderno",
        height=100
    )
    
    if st.button("🖼️ Ordenar a Hércules Renderizar Imagen Real"):
        with st.spinner(f"Hércules aplicando cambios '{prompt_apariencia}' a {personaje}..."):
            time.sleep(2)  # Simulación de procesamiento de renderizado local
        st.success("✨ ¡Imagen cinematográfica generada con éxito!")
        st.markdown(f"*(Renderizado activo para **{personaje}** con directriz: {prompt_apariencia})*")

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
        st.info("Dante: *'Para el próximo post en TikTok, enfócate en la tensión de los entrenamientos de Hugo y el misterio del monte Olyphso. ¡Eso engancha seguro!'*")