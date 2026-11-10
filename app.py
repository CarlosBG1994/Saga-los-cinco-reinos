import streamlit as st
import os
import threading
from motor_diario import motor

# Configuración de la página
st.set_page_config(
    page_title="Los Cinco Reinos - Oficina de Agentes",
    page_icon="👑",
    layout="wide"
)

# Inicializar variables de sesión
if "copy_redactado" not in st.session_state:
    st.session_state["copy_redactado"] = "✨ Descubre el secreto mejor guardado de Los Cinco Reinos... ¿Te atreves a cruzar la frontera? 🔥📖 #LosCincoReinos #Fantasía"
if "personaje_activo" not in st.session_state:
    st.session_state["personaje_activo"] = "Hugo"
if "ultimo_analisis_aura" not in st.session_state:
    st.session_state["ultimo_analisis_aura"] = "Aura está lista para escanear los capítulos con IA."
if "ultima_directriz_hercules" not in st.session_state:
    st.session_state["ultima_directriz_hercules"] = "Hércules está preparado para renderizar al personaje activo."
if "api_key_gemini" not in st.session_state:
    st.session_state["api_key_gemini"] = os.environ.get("GEMINI_API_KEY", "")
if "aura_estado_proceso" not in st.session_state:
    st.session_state["aura_estado_proceso"] = "Inactivo"
if "imagen_hercules_bytes" not in st.session_state:
    st.session_state["imagen_hercules_bytes"] = None

# Barra lateral de navegación
st.sidebar.title("👑 Los Cinco Reinos")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox(
    "Navegación",
    [
        "🏢 Oficina de la Agencia", 
        "🤖 Sala de Máquinas (Estado)", 
        "⏳ Crono (Validación y Publicación)", 
        "📚 Base de Lore", 
        "⚙️ Ajustes y API"
    ]
)

# ----------------------------------------------------
# 1. OFICINA DE LA AGENCIA
# ----------------------------------------------------
if menu == "🏢 Oficina de la Agencia":
    st.title("🏢 Oficina Central - Los Cinco Reinos")
    st.markdown("Tu equipo trabaja codo a codo. Aquí supervisas a Aura, Hércules, Dante, Kira, Hermes y Vulcano.")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📖 Aura")
        st.caption("Analista Textual (Lore con IA)")
        st.info("Lee los capítulos en segundo plano y extrae personajes.")
        
        if st.session_state["aura_estado_proceso"] == "Procesando":
            st.warning("🔄 Aura está trabajando en segundo plano...")
        elif st.session_state["aura_estado_proceso"] == "Completado":
            st.success("✅ ¡Análisis completado!")
        
        if st.button("🔍 Ordenar a Aura escanear en 2º plano", type="primary"):
            if not st.session_state["api_key_gemini"]:
                st.error("⚠️ Introduce tu Google AI Studio API Key en la pestaña '⚙️ Ajustes y API'.")
            else:
                st.session_state["aura_estado_proceso"] = "Procesando"
                def tarea_bg(api_key):
                    res = motor.aura_escanear_capitulos_automatico_ia(api_key)
                    if "error" in res:
                        st.session_state["ultimo_analisis_aura"] = f"Error: {res['error']}"
                    else:
                        st.session_state["ultimo_analisis_aura"] = f"¡Escaneo completado! Capítulos leídos: {res['archivos_leidos']}. Personajes totales: {len(res['personajes_totales'])}"
                    st.session_state["aura_estado_proceso"] = "Completado"
                
                hilo = threading.Thread(target=tarea_bg, args=(st.session_state["api_key_gemini"],))
                hilo.daemon = True
                hilo.start()
                st.success("🚀 ¡Proceso lanzado en segundo plano!")

    with col2:
        st.markdown("### 🎨 Hércules")
        st.caption("Director Gráfico y Vídeo")
        st.success(f"Personaje en escena:\n**{st.session_state['personaje_activo']}**")
        
        if st.button("🖼️ Ordenar a Hércules Renderizar Imagen"):
            if not st.session_state["api_key_gemini"]:
                st.error("⚠️ Introduce tu API Key en Ajustes.")
            else:
                with st.spinner("Hércules está generando el arte visual 9:16..."):
                    img_bytes, err = motor.hercules_generar_imagen_personaje(st.session_state["personaje_activo"], st.session_state["api_key_gemini"])
                    if err:
                        st.warning(err)
                    else:
                        st.session_state["imagen_hercules_bytes"] = img_bytes
                        st.success("✨ ¡Imagen generada con éxito por Hércules!")

        if st.session_state["imagen_hercules_bytes"]:
            st.image(st.session_state["imagen_hercules_bytes"], caption=f"Render de {st.session_state['personaje_activo']}", use_column_width=True)
        else:
            st.info("🖼️ Pulsa el botón superior para que Hércules genere el arte gráfico del personaje.")

    with col3:
        st.markdown("### ✍️ Dante & Kira")
        st.caption("Copywriting & SEO")
        st.warning("Redactando ganchos y optimizando hashtags.")
        if st.button("💬 Consultar a Dante"):
            st.toast("Dante: 'Los copys están listos para TikTok.'")

    st.markdown("---")
    st.subheader("👥 Selector de Personaje Activo para Hércules")
    
    if motor.lore_personajes:
        lista_personajes = list(motor.lore_personajes.keys())
        personaje_elegido = st.selectbox("Personaje protagonista en escena:", lista_personajes)
        st.session_state["personaje_activo"] = personaje_elegido
        st.session_state["ultima_directriz_hercules"] = motor.sincronizar_hercules_lore(personaje_elegido)
        
        info_p = motor.lore_personajes[personaje_elegido]
        st.info(f"📌 **Ficha activa:** {personaje_elegido} ({info_p['rol']}) — *{info_p['descripcion']}*")
    else:
        st.warning("⚠️ No hay personajes en la base de Lore.")

# ----------------------------------------------------
# 2. SALA DE MÁQUINAS
# ----------------------------------------------------
elif menu == "🤖 Sala de Máquinas (Estado)":
    st.title("🕹️ Estado del Equipo en Directo (Sala de Máquinas)")
    cols = st.columns(6)
    agentes_info = [
        ("Aura", "Analista", st.session_state["aura_estado_proceso"]),
        ("Hércules", "Director Gráfico", "Listo para render"),
        ("Dante", "Copywriter", "Activo"),
        ("Kira", "SEO", "Activa"),
        ("Hermes", "Soporte", "OK"),
        ("Crono", "Orquestador", "OK")
    ]
    for i, (nombre, rol, estado) in enumerate(agentes_info):
        with cols[i]:
            st.markdown(f"**{nombre}**")
            st.caption(rol)
            st.info(estado)

    st.markdown("---")
    archivos_disponibles = motor.listar_capitulos()
    capitulo_sel = st.selectbox("Elegir Archivo de Capítulo", archivos_disponibles)
    formato_sel = st.selectbox("Formato de contenido:", ["Publicación / Post Estático", "Vídeo Corto (Reel/TikTok)", "Carrusel de Lore"])
    
    if st.button("🚀 Ordenar al equipo procesar y generar propuesta"):
        res = motor.procesar_agentes_autonomos(capitulo_sel, st.session_state["personaje_activo"], formato_sel)
        st.session_state["ultimo_analisis_aura"] = res['aura_analisis']
        st.session_state["ultima_directriz_hercules"] = res['hercules_render']
        st.session_state["copy_redactado"] = res["dante_copy"] + "\n\n" + res["kira_tags"]
        st.success("¡Propuesta generada! Dirígete a **⏳ Crono**.")

# ----------------------------------------------------
# 3. CRONO (Validación y Publicación)
# ----------------------------------------------------
elif menu == "⏳ Crono (Validación y Publicación)":
    st.header("⏳ Crono - Centro de Validación y Publicación")
    
    with st.expander("🔍 Auditoría Gráfica y Textual de los Agentes", expanded=True):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("### 📖 Análisis de Aura")
            st.write(st.session_state["ultimo_analisis_aura"])
        with col_v2:
            st.markdown("### 🎨 Render de Hércules")
            if st.session_state["imagen_hercules_bytes"]:
                st.image(st.session_state["imagen_hercules_bytes"], width=200, caption="Arte activo")
            st.code(st.session_state["ultima_directriz_hercules"], language="markdown")

    st.markdown("---")
    col_video, col_text = st.columns([1, 1])
    
    with col_video:
        st.subheader("🎬 Previsualización de la Pieza Real")
        video_subido = st.file_uploader("Sube el archivo de vídeo definitivo (.mp4):", type=["mp4", "mov", "avi"])
        if video_subido is not None:
            st.video(video_subido)
            st.success("✅ ¡Vídeo validado!")
        else:
            st.info("📂 Sube aquí tu archivo MP4 para previsualizarlo.")

    with col_text:
        st.subheader("✍️ Textos validados")
        st.markdown(f"**Personaje activo:** `{st.session_state['personaje_activo']}`")
        copy_output = st.text_area("Copia el copy preparado:", value=st.session_state["copy_redactado"], height=180)
        if st.button("✅ Validar y Aprobar Contenido"):
            st.success("🎉 ¡Contenido aprobado oficialmente para TikTok!")

# ----------------------------------------------------
# 4. BASE DE LORE
# ----------------------------------------------------
elif menu == "📚 Base de Lore":
    st.header("📚 Base de Datos de Lore")
    if st.button("🔍 Hacer que Aura escanee con IA en 2º plano", type="primary"):
        if not st.session_state["api_key_gemini"]:
            st.error("⚠️ Introduce tu API Key en Ajustes.")
        else:
            st.session_state["aura_estado_proceso"] = "Procesando"
            def tarea_lore(api_key):
                motor.aura_escanear_capitulos_automatico_ia(api_key)
                st.session_state["aura_estado_proceso"] = "Completado"
            hilo = threading.Thread(target=tarea_lore, args=(st.session_state["api_key_gemini"],))
            hilo.daemon = True
            hilo.start()
            st.success("🚀 Escaneo lanzado en segundo plano.")

    st.markdown("---")
    with st.expander("➕ Añadir Nuevo Personaje Manualmente"):
        nombre_in = st.text_input("Nombre")
        rol_in = st.selectbox("Rol", ["Protagonista", "Secundario", "Antagonista", "Secuaz"])
        desc_in = st.text_area("Descripción")
        if st.button("💾 Guardar Personaje"):
            if nombre_in and motor.agregar_personaje(nombre_in, rol_in, desc_in):
                st.success(f"¡{nombre_in} guardado!")
                st.rerun()

    st.markdown("---")
    st.subheader("📋 Personajes Registrados")
    for pers, datos in list(motor.lore_personajes.items()):
        with st.expander(f"👤 {pers} — [{datos['rol']}]"):
            st.write(f"**Descripción:** {datos['descripcion']}")
            if st.button(f"🗑️ Eliminar {pers}", key=f"del_{pers}"):
                motor.eliminar_personaje(pers)
                st.rerun()

# ----------------------------------------------------
# 5. AJUSTES Y API
# ----------------------------------------------------
elif menu == "⚙️ Ajustes y API":
    st.header("⚙️ Configuración del Sistema y Modelos")
    api_key_input = st.text_input("Google AI Studio API Key", type="password", value=st.session_state["api_key_gemini"])
    if st.button("💾 Guardar Configuración"):
        st.session_state["api_key_gemini"] = api_key_input
        st.success("¡Configuración guardada correctamente!")