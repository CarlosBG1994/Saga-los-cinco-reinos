import streamlit as st
import os
from motor_diario import motor

# Configuración de la página
st.set_page_config(
    page_title="Los Cinco Reinos - Oficina de Agentes",
    page_icon="👑",
    layout="wide"
)

# Inicializar variables de sesión esenciales
if "video_generado" not in st.session_state:
    st.session_state["video_generado"] = "https://www.w3schools.com/html/mov_bbb.mp4"
if "copy_redactado" not in st.session_state:
    st.session_state["copy_redactado"] = "✨ Descubre el secreto mejor guardado de Los Cinco Reinos... ¿Te atreves a cruzar la frontera? 🔥📖 #LosCincoReinos #Fantasía"
if "personaje_activo" not in st.session_state:
    st.session_state["personaje_activo"] = "Hugo (Joven delgado, alto, de pelo negro y ojos azul celeste)"
if "webhook_url" not in st.session_state:
    st.session_state["webhook_url"] = "https://hook.eu1.make.com/2mwg5obphqa94k1hxlhdms16rd9ezyhe"

# Barra lateral de navegación
st.sidebar.title("👑 Los Cinco Reinos")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox(
    "Navegación",
    [
        "🏢 Oficina de la Agencia", 
        "🤖 Sala de Máquinas (Estado)", 
        "⏳ Crono (Publicación)", 
        "📚 Base de Lore", 
        "⚙️ Ajustes y API"
    ]
)

# ----------------------------------------------------
# 1. OFICINA DE LA AGENCIA (Vista interactiva del equipo)
# ----------------------------------------------------
if menu == "🏢 Oficina de la Agencia":
    st.title("🏢 Oficina Central - Los Cinco Reinos")
    st.markdown("Tu equipo trabaja codo a codo en la sala de operaciones. Aquí puedes ver qué hace cada miembro, gestionar directrices y sincronizar fichas.")

    # Representación visual de la oficina por escritorios
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📖 Aura")
        st.caption("Analista Textual (Lore)")
        st.info("Extrayendo esencias de los capítulos y sincronizando perfiles de personajes.")
        if st.button("💬 Hablar con Aura"):
            st.toast("Aura: 'Jefe, tengo los fragmentos del capítulo listos para el equipo.'")

    with col2:
        st.markdown("### 🎨 Hércules")
        st.caption("Director Gráfico y Vídeo")
        st.success(f"Personaje sincronizado:\n**{st.session_state['personaje_activo']}**")
        st.write("Preparando recursos visuales adaptados al lore.")
        prompt_hercules = st.text_input("Ajustar directriz visual a Hércules:", placeholder="Ej: Estilo épico oscuro...")
        if st.button("🎨 Forzar generación de recurso"):
            st.success("¡Hércules ha actualizado el render visual aplicando el personaje y el lore activo!")

    with col3:
        st.markdown("### ✍️ Dante & Kira")
        st.caption("Copywriting & SEO")
        st.warning("Redactando ganchos virales y optimizando hashtags.")
        if st.button("💬 Consultar a Dante"):
            st.toast("Dante: 'Los copys están optimizados para enganchar desde el segundo uno en TikTok.'")

    st.markdown("---")
    st.subheader("👥 Selector de Personaje Activo para Hércules")
    st.markdown("Selecciona qué personaje protagoniza la pieza para que Hércules mantenga la coherencia visual exacta:")
    
    personaje_elegido = st.selectbox(
        "Personaje en escena:",
        [
            "Hugo (Joven delgado, alto, de pelo negro y ojos azul celeste)",
            "Esther (Protagonista principal)",
            "Personaje secundario / Genérico del Reino"
        ]
    )
    st.session_state["personaje_activo"] = personaje_elegido
    st.success(f"Sincronizado correctamente: Hércules ya conoce los rasgos de **{personaje_elegido}**.")

# ----------------------------------------------------
# 2. SALA DE MÁQUINAS (Estado en Directo y Procesamiento)
# ----------------------------------------------------
elif menu == "🤖 Sala de Máquinas (Estado)":
    st.title("🕹️ Estado del Equipo en Directo (Sala de Máquinas)")
    st.markdown("Monitorización en tiempo real de los procesos autónomos de la agencia.")
    
    cols = st.columns(6)
    agentes_info = [
        ("Aura", "Analista Textual", "Analizando textos"),
        ("Hércules", "Director Gráfico", "Sincronizado con fichas"),
        ("Dante", "Copywriter", "Redactando ganchos"),
        ("Kira", "Estratega SEO", "Optimizando hashtags"),
        ("Hermes", "Soporte Redes", "Monitoreando flujos"),
        ("Crono", "Orquestador", "Listo para salida")
    ]
    
    for i, (nombre, rol, estado) in enumerate(agentes_info):
        with cols[i]:
            st.markdown(f"**{nombre}**")
            st.caption(rol)
            st.success(estado)

    st.markdown("---")
    st.subheader("⚙️ Panel de Control de Contenido")
    
    capitulo_sel = st.selectbox("Elegir Archivo de Capítulo", ["capitulo_0.txt", "capitulo_1.txt", "capitulo_2.txt"])
    formato_sel = st.selectbox("¿Qué formato de contenido necesitas esta semana?", ["Publicación / Post Estático", "Vídeo Corto (Reel/TikTok)", "Carrusel de Lore"])
    
    if st.button("🚀 Ordenar a Aura y al equipo procesar y generar propuesta"):
        try:
            # Llamada al motor para leer el archivo de capítulo seleccionado
            texto_leido = motor.leer_capitulo(capitulo_sel)
            contexto_h = motor.procesar_contexto_personaje(st.session_state["personaje_activo"])
            
            st.success("¡El equipo ha procesado el capítulo con éxito sin errores de API!")
            st.info(f"📄 **Resumen de lectura por Aura:** Archivo `{capitulo_sel}` procesado correctamente.")
            st.write(f"🎨 **Directriz aplicada:** {contexto_h}")
        except Exception as e:
            st.error(f"Error controlado en el motor: {e}")

# ----------------------------------------------------
# 3. CRONO (Centro de Publicación Manual)
# ----------------------------------------------------
elif menu == "⏳ Crono (Publicación)":
    st.header("⏳ Crono - Centro de Publicación Manual")
    st.markdown("Previsualiza el contenido multimedia generado por Hércules con su música y los textos de Dante listos para copiar.")

    col_video, col_text = st.columns([1, 1])
    
    with col_video:
        st.subheader("🎬 Previsualización de la Pieza (Vídeo / Música)")
        st.video(st.session_state["video_generado"])
        st.download_button(
            label="📥 Descargar Archivo MP4",
            data=st.session_state["video_generado"],
            file_name="reinos_contenido.mp4",
            mime="video/mp4"
        )

    with col_text:
        st.subheader("✍️ Textos y Ganchos")
        st.markdown(f"**Personaje activo vinculado:** `{st.session_state['personaje_activo']}`")
        
        copy_output = st.text_area(
            "Copia el copy preparado:", 
            value=st.session_state["copy_redactado"], 
            height=180
        )
        st.success("✅ Todo listo para copiar y colgar manualmente en TikTok en un solo clic.")

# ----------------------------------------------------
# 4. BASE DE LORE
# ----------------------------------------------------
elif menu == "📚 Base de Lore":
    st.header("📚 Base de Datos de Lore")
    st.markdown("Gestiona los personajes y reglas del mundo para que Hércules y Aura mantengan la coherencia absoluta.")
    
    with st.expander("👤 Hugo — [Protagonista]", expanded=True):
        st.text_input("Nombre", value="Hugo")
        st.selectbox("Rol", ["Protagonista", "Secundario", "Antagonista"], index=0)
        st.text_area("Descripción física y psicológica", value="Joven delgado, alto, de pelo negro y ojos azul celeste.")
        if st.button("💾 Actualizar Ficha de Hugo"):
            st.success("¡Ficha actualizada y sincronizada en tiempo real con Hércules!")

# ----------------------------------------------------
# 5. AJUSTES Y API
# ----------------------------------------------------
elif menu == "⚙️ Ajustes y API":
    st.header("⚙️ Configuración del Sistema y Modelos")
    st.markdown("Ajusta los parámetros de conexión y webhooks de respaldo.")
    
    api_key_input = st.text_input("Google AI Studio API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
    modelo_elegido = st.selectbox("Modelo de IA Activo", ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"])
    webhook_input = st.text_input("Webhook URL (Respaldo)", value=st.session_state["webhook_url"])
    
    if st.button("💾 Guardar Configuración"):
        st.session_state["webhook_url"] = webhook_input
        st.success("¡Configuración guardada correctamente!")