import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Los Cinco Reinos - Centro de Control",
    page_icon="👑",
    layout="wide"
)

# Inicializar variables de sesión si no existen
if "video_generado" not in st.session_state:
    st.session_state["video_generado"] = None
if "copy_redactado" not in st.session_state:
    st.session_state["copy_redactado"] = "✨ Descubre el secreto mejor guardado de Los Cinco Reinos... ¿Te atreves a cruzar la frontera? 🔥📖 #LosCincoReinos #Fantasía"
if "webhook_url" not in st.session_state:
    st.session_state["webhook_url"] = "https://hook.eu1.make.com/2mwg5obphqa94k1hxlhdms16rd9ezyhe"

# Barra lateral de navegación
st.sidebar.title("👑 Los Cinco Reinos")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox(
    "Navegación",
    ["🏠 Panel Principal", "⏳ Crono (Publicación)", "🔑 Credenciales por Red", "🤖 Sala de Agentes"]
)

# ----------------------------------------------------
# 1. PANEL PRINCIPAL
# ----------------------------------------------------
if menu == "🏠 Panel Principal":
    st.title("🛡️ Centro de Operaciones de Marketing")
    st.markdown("Bienvenido al núcleo de gestión de tu saga. Aquí tus agentes coordinan la creación de contenido multimedia.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Estado de Agentes", "Activos", "4 en línea")
    with col2:
        st.metric("Piezas en Borrador", "3 listas", "Pendientes de revisión")
    with col3:
        st.metric("Canal de Salida", "Manual / Directo", "Optimizado")

    st.markdown("---")
    st.info("💡 Consejo: Usa la pestaña **Crono** para previsualizar y extraer tus vídeos con música y textos listos para publicar.")

# ----------------------------------------------------
# 2. CRONO (CENTRO DE PUBLICACIÓN MANUAL)
# ----------------------------------------------------
elif menu == "⏳ Crono (Publicación)":
    st.header("⏳ Crono - Centro de Publicación Manual")
    st.markdown("Previsualiza el contenido generado por tus agentes, comprueba la pista de música y cópialo listo para tus redes.")

    # Simulador o contenido real en sesión
    if st.session_state["video_generado"]:
        col_video, col_text = st.columns([1, 1])
        
        with col_video:
            st.subheader("🎬 Previsualización de la Pieza")
            # Reproductor de vídeo integrado con soporte de audio/música
            st.video(st.session_state["video_generado"])
            
            # Botón de descarga directa
            st.download_button(
                label="📥 Descargar Vídeo MP4",
                data=st.session_state["video_generado"],
                file_name="reinos_tiktok.mp4",
                mime="video/mp4"
            )

        with col_text:
            st.subheader("✍️ Textos y Hashtags")
            st.markdown("**Copy redactado por Dante & Kira:**")
            
            # Área de texto editable y copiable
            copy_output = st.text_area(
                "Copia el texto:", 
                value=st.session_state["copy_redactado"], 
                height=180
            )
            
            st.success("✅ ¡Contenido listo para llevar a TikTok o cualquier red en un solo clic!")
            
    else:
        st.info("ℹ️ Aún no hay ningún contenido generado en esta sesión. Simula una generación o ejecuta a tus agentes para ver la previsualización aquí.")
        
        # Botón de prueba rápida para simular un vídeo en la interfaz
        if st.button("🧪 Cargar vídeo de prueba (Demo)"):
            # Usamos un vídeo de ejemplo público para que veas cómo carga el reproductor
            st.session_state["video_generado"] = "https://www.w3schools.com/html/mov_bbb.mp4"
            st.rerun()

# ----------------------------------------------------
# 3. CREDENCIALES POR RED
# ----------------------------------------------------
elif menu == "🔑 Credenciales por Red":
    st.header("🔑 Credenciales y Enlaces de Red")
    st.markdown("Configura los puntos de conexión y webhooks de tu infraestructura.")
    
    st.markdown("### 🎵 TikTok Content Posting API & Webhook")
    
    client_key = st.text_input("TikTok Client Key", value="auno6xfgoe4q4gw")
    client_secret = st.text_input("TikTok Client Secret", type="password", value="************************")
    access_token = st.text_input("TikTok Access Token", placeholder="Introduce tu token si procede...")
    
    webhook_input = st.text_input(
        "Webhook URL (Make / Zapier / Automatizaciones)", 
        value=st.session_state["webhook_url"]
    )
    
    if st.button("💾 Guardar Credenciales"):
        st.session_state["webhook_url"] = webhook_input
        st.success("¡Credenciales y Webhook guardados correctamente en la sesión!")

# ----------------------------------------------------
# 4. SALA DE AGENTES
# ----------------------------------------------------
elif menu == "🤖 Sala de Agentes":
    st.header("🤖 Sala de Control de Agentes")
    st.markdown("Interactúa directamente con Aura, Dante, Hércules y Kira.")
    
    agente_sel = st.selectbox("Selecciona al agente:", ["Aura (Lore & Historia)", "Dante (Copywriting)", "Hércules (Multimedia)", "Kira (Hashtags & SEO)"])
    
    prompt_usuario = st.text_area("Instrucción para el agente:")
    if st.button("🚀 Ejecutar instrucción"):
        st.success(f"El agente {agente_sel} ha procesado tu solicitud correctamente.")