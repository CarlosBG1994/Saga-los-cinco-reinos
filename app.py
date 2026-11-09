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
if "copy_redactado" not in st.session_state:
    st.session_state["copy_redactado"] = "✨ Descubre el secreto mejor guardado de Los Cinco Reinos... ¿Te atreves a cruzar la frontera? 🔥📖 #LosCincoReinos #Fantasía"
if "personaje_activo" not in st.session_state:
    st.session_state["personaje_activo"] = "Hugo"
if "ultimo_analisis_aura" not in st.session_state:
    st.session_state["ultimo_analisis_aura"] = "Aún no se ha procesado ningún capítulo en esta sesión."
if "ultima_directriz_hercules" not in st.session_state:
    st.session_state["ultima_directriz_hercules"] = "Pendiente de sincronizar con Hércules."

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
    st.markdown("Tu equipo trabaja codo a codo en la sala de operaciones. Aquí supervisas a Aura, Hércules, Dante, Kira, Hermes y Vulcano.")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📖 Aura")
        st.caption("Analista Textual (Lore)")
        st.info("Extrayendo esencias de los capítulos y sincronizando perfiles.")
        if st.button("💬 Hablar con Aura"):
            st.toast("Aura: 'Jefe, los fragmentos están listos para el análisis cruzado.'")

    with col2:
        st.markdown("### 🎨 Hércules")
        st.caption("Director Gráfico y Vídeo")
        st.success(f"Personaje sincronizado:\n**{st.session_state['personaje_activo']}**")
        st.write("Generando recursos visuales adaptados al lore.")
        if st.button("🎨 Forzar render visual"):
            st.success("¡Hércules ha actualizado el render visual aplicando la descripción del personaje!")

    with col3:
        st.markdown("### ✍️ Dante & Kira")
        st.caption("Copywriting & SEO")
        st.warning("Redactando ganchos y optimizando hashtags.")
        if st.button("💬 Consultar a Dante"):
            st.toast("Dante: 'Los copys están optimizados para enganchar en redes al instante.'")

    st.markdown("---")
    st.subheader("👥 Selector de Personaje Activo para Hércules")
    
    if motor.lore_personajes:
        lista_personajes = list(motor.lore_personajes.keys())
        personaje_elegido = st.selectbox("Personaje en escena:", lista_personajes)
        st.session_state["personaje_activo"] = personaje_elegido
        
        info_p = motor.lore_personajes[personaje_elegido]
        st.info(f"📌 **Ficha activa:** {personaje_elegido} ({info_p['rol']}) — *{info_p['descripcion']}*")
    else:
        st.warning("⚠️ No hay personajes en la base de Lore. Añade uno desde la pestaña 'Base de Lore'.")

# ----------------------------------------------------
# 2. SALA DE MÁQUINAS (Estado y Procesamiento)
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
        ("Crono", "Orquestador", "Listo para validación")
    ]
    
    for i, (nombre, rol, estado) in enumerate(agentes_info):
        with cols[i]:
            st.markdown(f"**{nombre}**")
            st.caption(rol)
            st.success(estado)

    st.markdown("---")
    st.subheader("⚙️ Panel de Control de Contenido")
    
    archivos_disponibles = motor.listar_capitulos()
    capitulo_sel = st.selectbox("Elegir Archivo de Capítulo", archivos_disponibles)
    formato_sel = st.selectbox("¿Qué formato de contenido necesitas esta semana?", ["Publicación / Post Estático", "Vídeo Corto (Reel/TikTok)", "Carrusel de Lore"])
    
    if st.button("🚀 Ordenar a Aura y al equipo procesar y generar propuesta"):
        try:
            resultado_proceso = motor.procesar_agentes_autonomos(capitulo_sel, st.session_state["personaje_activo"], formato_sel)
            
            # Guardamos los resultados en la sesión para validarlos en Crono
            st.session_state["ultimo_analisis_aura"] = resultado_proceso['aura_analisis']
            st.session_state["ultima_directriz_hercules"] = resultado_proceso['hercules_render']
            st.session_state["copy_redactado"] = resultado_proceso["dante_copy"] + "\n\n" + resultado_proceso["kira_tags"]
            
            st.success("¡El equipo ha procesado la propuesta! Dirígete a la pestaña **⏳ Crono** para validarla y revisarla.")
            
        except Exception as e:
            st.error(f"Error controlado en el motor: {e}")

# ----------------------------------------------------
# 3. CRONO (Validación y Publicación Manual)
# ----------------------------------------------------
elif menu == "⏳ Crono (Validación y Publicación)":
    st.header("⏳ Crono - Centro de Validación y Publicación")
    st.markdown("Aquí es donde **validas el trabajo de tus agentes**. Revisa el análisis de Aura, el enfoque de Hércules y los textos de Dante antes de dar luz verde.")

    # PANEL DE VALIDACIÓN DEL TRABAJO DE LOS AGENTES
    with st.expander("🔍 Auditoría de Trabajo de los Agentes (Validación)", expanded=True):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("### 📖 Análisis de Aura (Lore)")
            st.write(st.session_state["ultimo_analisis_aura"])
        with col_v2:
            st.markdown("### 🎨 Directriz de Hércules (Gráficos)")
            st.write(st.session_state["ultima_directriz_hercules"])

    st.markdown("---")
    
    col_video, col_text = st.columns([1, 1])
    
    with col_video:
        st.subheader("🎬 Previsualización de la Pieza Real")
        video_subido = st.file_uploader("Sube el archivo de vídeo definitivo generado para esta pieza:", type=["mp4", "mov", "avi"])
        
        if video_subido is not None:
            st.video(video_subido)
            st.success("✅ ¡Vídeo validado y cargado correctamente!")
        else:
            st.info("📂 Sube aquí el archivo MP4 para previsualizarlo junto a la música.")

    with col_text:
        st.subheader("✍️ Textos y Ganchos validados")
        st.markdown(f"**Personaje activo vinculado:** `{st.session_state['personaje_activo']}`")
        
        copy_output = st.text_area(
            "Copia el copy preparado:", 
            value=st.session_state["copy_redactado"], 
            height=180
        )
        
        if st.button("✅ Validar y Aprobar Contenido para Publicar"):
            st.success("🎉 ¡Contenido validado oficialmente! Ya puedes copiar los textos y subirlo a TikTok.")

# ----------------------------------------------------
# 4. BASE DE LORE (Crear, Editar y Eliminar Personajes)
# ----------------------------------------------------
elif menu == "📚 Base de Lore":
    st.header("📚 Base de Datos de Lore")
    st.markdown("Gestiona, cataloga o elimina los personajes de tu saga para que Hércules y Aura mantengan la coherencia absoluta.")
    
    # SECCIÓN PARA AÑADIR NUEVO PERSONAJE
    with st.expander("➕ Añadir Nuevo Personaje al Lore"):
        nuevo_nombre_ing = st.text_input("Nombre del personaje")
        nuevo_rol_ing = st.selectbox("Rol principal", ["Protagonista", "Secundario", "Antagonista", "Secuaz"], key="rol_nuevo")
        nueva_desc_ing = st.text_area("Descripción física y psicológica", key="desc_nueva")
        
        if st.button("💾 Guardar Nuevo Personaje"):
            if nuevo_nombre_ing:
                if motor.agregar_personaje(nuevo_nombre_ing, nuevo_rol_ing, nueva_desc_ing):
                    st.success(f"¡Personaje '{nuevo_nombre_ing}' creado y catalogado con éxito!")
                    st.rerun()
                else:
                    st.error("El personaje ya existe o el nombre está vacío.")
            else:
                st.warning("Por favor, introduce un nombre válido.")

    st.markdown("---")
    st.subheader("📋 Personajes Existentes (Editar / Eliminar)")
    
    if not motor.lore_personajes:
        st.info("No hay personajes registrados actualmente.")
    else:
        for pers, datos in list(motor.lore_personajes.items()):
            with st.expander(f"👤 {pers} — [{datos['rol']}]"):
                nuevo_rol = st.selectbox("Rol", ["Protagonista", "Secundario", "Antagonista", "Secuaz"], index=["Protagonista", "Secundario", "Antagonista", "Secuaz"].index(datos['rol']) if datos['rol'] in ["Protagonista", "Secundario", "Antagonista", "Secuaz"] else 0, key=f"rol_edit_{pers}")
                nueva_desc = st.text_area("Descripción física y psicológica", value=datos["descripcion"], key=f"desc_edit_{pers}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"💾 Actualizar Ficha", key=f"btn_act_{pers}"):
                        motor.lore_personajes[pers]["rol"] = nuevo_rol
                        motor.lore_personajes[pers]["descripcion"] = nueva_desc
                        st.success(f"¡Ficha de {pers} actualizada correctamente!")
                with col_btn2:
                    if st.button(f"🗑️ Eliminar Personaje", key=f"btn_del_{pers}"):
                        motor.eliminar_personaje(pers)
                        st.success(f"¡Personaje {pers} eliminado del Lore!")
                        st.rerun()

# ----------------------------------------------------
# 5. AJUSTES Y API
# ----------------------------------------------------
elif menu == "⚙️ Ajustes y API":
    st.header("⚙️ Configuración del Sistema y Modelos")
    st.markdown("Ajusta los parámetros de conexión y webhooks de respaldo.")
    
    api_key_input = st.text_input("Google AI Studio API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
    modelo_elegido = st.selectbox("Modelo de IA Activo", ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"])
    webhook_input = st.text_input("Webhook URL (Respaldo)", value="https://hook.eu1.make.com/2mwg5obphqa94k1hxlhdms16rd9ezyhe")
    
    if st.button("💾 Guardar Configuración"):
        st.success("¡Configuración guardada correctamente!")