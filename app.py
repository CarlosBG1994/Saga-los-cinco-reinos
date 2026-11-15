import streamlit as st
import os
import threading
import streamlit.components.v1 as components
from motor_diario import motor

st.set_page_config(page_title="Los Cinco Reinos - Oficina de Agentes", page_icon="👑", layout="wide")

API_DEFAULT = "AQ.Ab8RN6IYksoP9PÚ3mgI8Py0nXmvFawOefvaOGXYcCCLbv2sTAg"

if "copy_redactado" not in st.session_state:
    st.session_state["copy_redactado"] = "✨ Descubre el secreto mejor guardado de Los Cinco Reinos... 🔥📖 #LosCincoReinos #Fantasía"
if "personaje_activo" not in st.session_state:
    st.session_state["personaje_activo"] = "Hugo"
if "ultimo_analisis_aura" not in st.session_state:
    st.session_state["ultimo_analisis_aura"] = "Aura lista para escanear."
if "api_key_gemini" not in st.session_state:
    st.session_state["api_key_gemini"] = os.environ.get("GEMINI_API_KEY", API_DEFAULT)
if "aura_estado_proceso" not in st.session_state:
    st.session_state["aura_estado_proceso"] = "Inactivo"
if "cambios_hercules" not in st.session_state:
    st.session_state["cambios_hercules"] = ""

st.sidebar.title("👑 Los Cinco Reinos")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("Navegación", ["🏢 Oficina de la Agencia", "🤖 Sala de Máquinas (Estado)", "⏳ Crono (Validación y Publicación)", "📚 Base de Lore", "⚙️ Ajustes y API"])

# ----------------------------------------------------
# 1. OFICINA DE LA AGENCIA
# ----------------------------------------------------
if menu == "🏢 Oficina de la Agencia":
    st.title("🏢 Oficina Central - Los Cinco Reinos")
    st.markdown("Gestión local y autónoma de tus agentes.")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📖 Aura")
        st.caption("Analista Textual")
        if st.session_state["aura_estado_proceso"] == "Procesando":
            st.warning("🔄 Analizando en 2º plano...")
        elif st.session_state["aura_estado_proceso"] == "Completado":
            st.success("✅ ¡Completado!")
        
        if st.button("🔍 Ordenar a Aura escanear en 2º plano", type="primary"):
            st.session_state["aura_estado_proceso"] = "Procesando"
            def tarea_bg(key):
                motor.aura_escanear_capitulos_automatico_ia(key)
                st.session_state["aura_estado_proceso"] = "Completado"
            hilo = threading.Thread(target=tarea_bg, args=(st.session_state["api_key_gemini"],))
            hilo.daemon = True
            hilo.start()
            st.success("🚀 Lanzado en segundo plano.")

    with col2:
        st.markdown("### 🎨 Hércules")
        st.caption("Director Gráfico (Estética Dorada)")
        st.success(f"Personaje: **{st.session_state['personaje_activo']}**")
        
        cambios = st.text_area("✍️ Indícale cambios a Hércules:", value=st.session_state["cambios_hercules"], key="input_cambios")
        if st.button("🔄 Aplicar Cambios"):
            st.session_state["cambios_hercules"] = cambios
            st.success("✨ ¡Cambios aplicados al diseño!")

        # Renderizamos el SVG local en tonos amarillos/dorados al instante y sin errores de red
        svg_data = motor.hercules_generar_avatar_svg(st.session_state["personaje_activo"], st.session_state["cambios_hercules"])
        components.html(svg_data, height=350)

    with col3:
        st.markdown("### ✍️ Dante & Kira")
        st.caption("Copywriting & SEO")
        if st.button("💬 Consultar a Dante"):
            st.toast("Dante: 'Copys listos para redes.'")

    st.markdown("---")
    st.subheader("👥 Selector de Personaje Activo")
    if motor.lore_personajes:
        lista = list(motor.lore_personajes.keys())
        st.session_state["personaje_activo"] = st.selectbox("Elegir protagonista:", lista)
        info = motor.lore_personajes[st.session_state["personaje_activo"]]
        st.info(f"📌 **{st.session_state['personaje_activo']}** ({info['rol']}) — *{info['descripcion']}*")

# ----------------------------------------------------
# 2. SALA DE MÁQUINAS
# ----------------------------------------------------
elif menu == "🤖 Sala de Máquinas (Estado)":
    st.title("🕹️ Sala de Máquinas")
    cols = st.columns(6)
    for i, nombre in enumerate(["Aura", "Hércules", "Dante", "Kira", "Hermes", "Crono"]):
        with cols[i]:
            st.markdown(f"**{nombre}**")
            st.info("Activo")

    st.markdown("---")
    cap = st.selectbox("Elegir Capítulo", motor.listar_capitulos())
    formato = st.selectbox("Formato", ["Vídeo Corto (Reel/TikTok)", "Post Estático"])
    if st.button("🚀 Procesar propuesta"):
        res = motor.procesar_agentes_autonomos(cap, st.session_state["personaje_activo"], formato)
        st.session_state["ultimo_analisis_aura"] = res["aura_analisis"]
        st.session_state["copy_redactado"] = res["dante_copy"] + "\n\n" + res["kira_tags"]
        st.success("¡Propuesta generada con éxito en Crono!")

# ----------------------------------------------------
# 3. CRONO
# ----------------------------------------------------
elif menu == "⏳ Crono (Validación y Publicación)":
    st.header("⏳ Crono - Validación")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Análisis y Textos")
        st.write(st.session_state["ultimo_analisis_aura"])
        st.text_area("Copy:", value=st.session_state["copy_redactado"], height=150)
    with c2:
        st.markdown("### Previsualización Gráfica")
        svg_crono = motor.hercules_generar_avatar_svg(st.session_state["personaje_activo"], st.session_state["cambios_hercules"])
        components.html(svg_crono, height=350)

# ----------------------------------------------------
# 4. BASE DE LORE
# ----------------------------------------------------
elif menu == "📚 Base de Lore":
    st.header("📚 Base de Datos de Lore")
    with st.expander("➕ Añadir Personaje"):
        n = st.text_input("Nombre")
        r = st.selectbox("Rol", ["Protagonista", "Secundario", "Antagonista"])
        d = st.text_area("Descripción")
        if st.button("Guardar") and n:
            motor.agregar_personaje(n, r, d)
            st.success(f"¡{n} guardado!")
            st.rerun()

    for p, dat in list(motor.lore_personajes.items()):
        with st.expander(f"👤 {p}"):
            st.write(dat["descripcion"])
            if st.button(f"Eliminar {p}", key=f"del_{p}"):
                motor.eliminar_personaje(p)
                st.rerun()

# ----------------------------------------------------
# 5. AJUSTES Y API
# ----------------------------------------------------
elif menu == "⚙️ Ajustes y API":
    st.header("⚙️ Configuración")
    st.session_state["api_key_gemini"] = st.text_input("API Key", type="password", value=st.session_state["api_key_gemini"])
    if st.button("Guardar"):
        st.success("Configuración guardada.")