import streamlit as st
from motor_diario import ColmenaBufferInfinito

st.set_page_config(
    page_title="Agencia de Marketing & Ventas — Los Cinco Reinos",
    page_icon="👑",
    layout="wide"
)

if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

colmena = st.session_state.colmena_buffer

st.title("👑 Agencia de Marketing Literario — Los Cinco Reinos")
st.info("💡 *Tus agentes operan como una agencia de ventas profesional: analizan tus archivos .txt, extraen los personajes importantes, generan contenido comercial y crean arte visual con tu estilo propio.*")

estilo_actual = getattr(colmena, "estilo_visual_seleccionado", "Estilo Propio: Fantasía Oscura y Narrativa Original")
nuevo_estilo = st.selectbox(
    "🎨 Estilo Visual Activo para Hércules:",
    [
        "Estilo Propio: Fantasía Oscura y Narrativa Original",
        "Manga Blanco y Negro Tradicional (Ink Lineart)",
        "Ilustración Conceptual de Alta Resolución"
    ],
    index=0
)

if nuevo_estilo != estilo_actual:
    colmena.cambiar_estilo_arte(nuevo_estilo)
    st.success(f"¡Estilo cambiado a '{nuevo_estilo}'!")
    st.rerun()

tab_oficina, tab_chat, tab_coautor, tab_capitulos, tab_bocetos, tab_manga, tab_redes, tab_videos, tab_scripts, tab_metricas, tab_config = st.tabs([
    "🖥️ Oficina Sims",
    "💬 Chat Agencia",
    "✍️ Co-autoría & Ventas",
    "📖 Capítulos (.txt)",
    "👥 Biblioteca de Personajes",
    "🎨 Estudio Gráfico",
    "📢 Banco Multicanal",
    "🎬 Vídeos BookTok",
    "🛠️ Editor de Scripts",
    "📊 Métricas de Ventas",
    "⚙️ Credenciales API"
])

# --- PESTAÑA 1: OFICINA SIMS ---
with tab_oficina:
    st.header("🖥️ Sala de Operaciones de los Agentes")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("### 👔 Cronos")
        st.info("💻 Dirigiendo campañas de conversión.")
    with col_s2:
        st.markdown("### 👩‍💻 Aura")
        st.success("🟢 Optimizando copys de venta y personajes.")
    with col_s3:
        st.markdown("### 🎨 Hércules")
        st.success(f"🟢 Estilo Propietario Activo")

# --- PESTAÑA 2: CHAT ---
with tab_chat:
    st.header("💬 Canal de Comunicación con la Agencia")
    for msg in colmena.chat_colmena:
        st.markdown(f"**[{msg['origen']}]:** {msg['mensaje']}")
    with st.form("form_chat"):
        m = st.text_input("Instrucción para el equipo:")
        if st.form_submit_button("Enviar Orden"):
            if m:
                colmena.enviar_mensaje_chat("Usuario (Director)", m)
                st.rerun()

# --- PESTAÑA 3: CO-AUTORÍA ---
with tab_coautor:
    st.header("✍️ Co-autoría, Corrección y Ganchos de Ventas")
    with st.form("form_coautor"):
        cap_ref = st.selectbox("Tomar como base el Capítulo:", options=list(range(0, 26)), format_func=lambda x: f"Capítulo {x}")
        idea_trama = st.text_area("¿Qué quieres que ocurra en el siguiente segmento para atrapar al lector?:")
        if st.form_submit_button("✨ Generar Continuación Optimizada"):
            if idea_trama:
                colmena.generar_ayuda_continuacion(idea_trama, cap_ref)
                st.success("¡Propuesta generada!")
                st.rerun()
    st.markdown("---")
    for prop in reversed(getattr(colmena, "propuestas_escritura", [])):
        st.info(f"**Referencia: Capítulo {prop['capitulo_ref']}** | Idea: *{prop['idea']}*")
        st.markdown(prop['resultado'])
        st.divider()

# --- PESTAÑA 4: CAPÍTULOS ---
with tab_capitulos:
    st.header("📖 Capítulos de la Novela")
    num_cap = st.selectbox("Seleccionar Capítulo:", options=list(range(0, 26)), format_func=lambda x: f"Capítulo {x}")
    info = colmena.obtener_capitulo(num_cap)
    st.markdown(f"### 👑 {info['titulo']}")
    st.text_area("Texto del capítulo:", info["descripcion"], height=200)
    if info["descripcion"] and "⚠️" not in info["descripcion"] and "Error" not in info["descripcion"]:
        colmena.ciclo_autonomo_marketing_inteligente(num_cap, info["descripcion"])
        st.success("¡La agencia ha analizado el capítulo, extraído personajes y generado material con éxito!")

# --- PESTAÑA 5: PERSONAJES ---
with tab_bocetos:
    st.header("👥 Biblioteca de Personajes Importantes")
    personajes = getattr(colmena, "lore_universo", [])
    if personajes:
        for p in reversed(personajes):
            st.markdown(f"### 👤 {p['nombre']}")
            c1, c2 = st.columns([1, 1])
            with c1:
                if p.get("boceto_url"):
                    st.image(p["boceto_url"], use_container_width=True)
            with c2:
                st.write(f"**Descripción:** {p.get('descripcion')}")
            st.divider()
    else:
        st.info("Sube tus capítulos .txt para que Aura extraiga los personajes.")

# --- PESTAÑA 6: ESTUDIO GRÁFICO ---
with tab_manga:
    st.header("🎨 Estudio Gráfico de Hércules")
    paginas = getattr(colmena, "paginas_manga", [])
    if paginas:
        for pag in reversed(paginas):
            pag_id = pag.get('pag_id')
            st.markdown(f"### 📖 Ilustración Comercial — Cap {pag_id}")
            c1, c2 = st.columns([1, 1])
            with c1:
                st.image(pag.get("imagen_url"), use_container_width=True)
            with c2:
                st.info(pag.get('escena_resumen'))
                if st.button(f"🗑️ Eliminar Ilustración #{pag_id}", key=f"del_manga_{pag_id}"):
                    colmena.eliminar_pagina_manga(pag_id)
                    st.success("Eliminado.")
                    st.rerun()
            st.divider()
    else:
        st.info("No hay ilustraciones generadas aún.")

# --- PESTAÑA 7: BANCO MULTICANAL ---
with tab_redes:
    st.header("📢 Banco Multicanal (Campañas de Ventas)")
    banco = getattr(colmena, "banco_contenido", [])
    if banco:
        for item in reversed(banco):
            item_id = item.get('id')
            st.markdown(f"### 📦 Campaña #{item_id} (Cap {item.get('cap_asociado')})")
            copys = item.get('copys', {})
            st.text_area("Feed / Post:", copys.get('feed', ''), key=f"f_{item_id}", height=120)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button(f"🚀 Publicar Campaña #{item_id}", key=f"pub_{item_id}"):
                    colmena.publicar_o_descartar_contenido(item_id, "publicar")
                    st.success("¡Publicado!")
                    st.rerun()
            with col_b2:
                if st.button(f"🗑️ Descartar Campaña #{item_id}", key=f"del_banco_{item_id}"):
                    colmena.publicar_o_descartar_contenido(item_id, "eliminar")
                    st.warning("Descartado.")
                    st.rerun()
            st.divider()
    else:
        st.info("Banco multicanal vacío.")

# --- PESTAÑA 8: VÍDEOS ---
with tab_videos:
    st.header("🎬 Vídeos BookTok para TikTok / Reels")
    videos = getattr(colmena, "videos_tiktok", [])
    if videos:
        for vid in reversed(videos):
            vid_id = vid.get('id')
            st.markdown(f"### Vídeo — Cap {vid.get('capitulo')}")
            c1, c2 = st.columns([1, 1])
            with c1:
                st.image(vid.get("preview_url"), use_container_width=True)
            with c2:
                st.info(vid.get('guion_voz'))
                if st.button(f"🗑️ Eliminar Vídeo #{vid_id}", key=f"del_vid_{vid_id}"):
                    colmena.eliminar_video_tiktok(vid_id)
                    st.success("Eliminado.")
                    st.rerun()
            st.divider()
    else:
        st.info("No hay vídeos generados.")

# --- PESTAÑA 9: EDITOR DE SCRIPTS ---
with tab_scripts:
    st.header("🛠️ Panel de Edición de Scripts y Estilo Propietario")
    scripts_actuales = getattr(colmena, "scripts_personalizados", {})
    with st.form("form_editar_scripts"):
        s_arte = st.text_area("Script para Estilo Propietario de Arte:", value=scripts_actuales.get("prompt_arte", ""), height=120)
        s_manga = st.text_area("Script para Manga:", value=scripts_actuales.get("prompt_manga", ""), height=100)
        s_video = st.text_area("Script para Vídeo:", value=scripts_actuales.get("prompt_video", ""), height=100)
        if st.form_submit_button("💾 Guardar Scripts Propios"):
            colmena.guardar_scripts_personalizados({"prompt_arte": s_arte, "prompt_manga": s_manga, "prompt_video": s_video})
            st.success("¡Scripts guardados con éxito!")
            st.rerun()

# --- PESTAÑA 10: MÉTRICAS ---
with tab_metricas:
    st.header("📊 Métricas de Ventas y Rendimiento")
    metricas = getattr(colmena, "metricas_redes", {})
    cols = st.columns(len(metricas))
    for i, (plat, datos) in enumerate(metricas.items()):
        with cols[i]:
            st.subheader(f"📱 {plat}")
            st.metric("Lectores / Seguidores", datos.get("seguidores", 0))
            st.metric("Rendimiento", f"{datos.get('rendimiento_principal', 0)}%")

# --- PESTAÑA 11: CREDENCIALES API ---
with tab_config:
    st.header("⚙️ Configuración y Credenciales de Redes & IA")
    st.write("Introduce y guarda de forma persistente tus claves de acceso de forma independiente para cada plataforma.")
    
    plataforma = st.selectbox("Selecciona la plataforma a configurar:", ["Google AI Studio", "TikTok API", "Instagram / Meta Graph API", "Twitter (X) API", "Wattpad"])
    creds_actuales = colmena.credenciales.get(plataforma, {})
    
    with st.form(f"form_creds_{plataforma}"):
        if plataforma == "Google AI Studio":
            val_key = creds_actuales.get("api_key_google", "AQ.Ab8RN6IYksoP9pU3mgI8Py0nXmvFawOefvAoGXYcCCLbv2sTAg")
            c1 = st.text_input("Google Gemini API Key:", value=val_key, type="password")
            c2 = ""
        else:
            c1 = st.text_input("Client Key / App ID / API Key / Usuario:", value=creds_actuales.get("c1", ""))
            c2 = st.text_input("Client Secret / Token / Password:", value=creds_actuales.get("c2", ""), type="password")
        
        if st.form_submit_button("💾 Guardar Credenciales de esta Plataforma"):
            if plataforma == "Google AI Studio":
                datos_guardar = {"api_key_google": c1}
            else:
                datos_guardar = {"c1": c1, "c2": c2}
            colmena.guardar_credencial_especifica(plataforma, datos_guardar)
            st.success(f"¡Credenciales de {plataforma} guardadas correctamente en disco de forma independiente!")
            st.rerun()