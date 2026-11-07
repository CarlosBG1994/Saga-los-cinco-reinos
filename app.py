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
st.info("💡 *Tus agentes operan como una agencia de ventas profesional: analizan tus capítulos .txt, extraen todos los personajes importantes, generan publicaciones optimizadas y crean ilustraciones de alta precisión (Kingdom Hearts style).*")

estilo_actual = getattr(colmena, "estilo_visual_seleccionado", "Burbujas de Recuerdos (Kingdom Hearts Style)")
nuevo_estilo = st.selectbox(
    "🎨 Estilo Visual Activo para Hércules:",
    [
        "Burbujas de Recuerdos (Kingdom Hearts Style)",
        "Manga Blanco y Negro Tradicional (Ink Lineart)",
        "Ilustración Color Fantasy Conceptual"
    ],
    index=["Burbujas de Recuerdos (Kingdom Hearts Style)", "Manga Blanco y Negro Tradicional (Ink Lineart)", "Ilustración Color Fantasy Conceptual"].index(estilo_actual) if estilo_actual in ["Burbujas de Recuerdos (Kingdom Hearts Style)", "Manga Blanco y Negro Tradicional (Ink Lineart)", "Ilustración Color Fantasy Conceptual"] else 0
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
        dudas = [d for d in colmena.dudas_agentes if not d.get("respondida", False)]
        if dudas:
            st.error("❓ **Duda pendiente**")
            for d in dudas:
                st.warning(f"\"{d['pregunta']}\"")
                resp = st.text_input("Responder directriz:", key=f"d_{d['id']}")
                if st.button("Enviar", key=f"btn_{d['id']}"):
                    colmena.responder_duda(d['id'], resp)
                    st.rerun()
        else:
            st.success("🟢 Optimizando copys de venta")
    with col_s3:
        st.markdown("### 🎨 Hércules")
        st.success(f"🟢 Estilo: **{nuevo_estilo}**")

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
    st.write("Escribe tu idea para el siguiente fragmento. Aura te redactará una propuesta orientada a enganchar al lector desde el primer segundo.")
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
        st.success("¡La agencia ha analizado el capítulo, extraído personajes y generado material de marketing con éxito!")

# --- PESTAÑA 5: PERSONAJES ---
with tab_bocetos:
    st.header("👥 Biblioteca de Personajes Importantes")
    st.write("Aura extrae automáticamente a todos los personajes con nombre e importancia detectados en los capítulos.")
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
        st.info("Sube tus capítulos .txt y selecciona uno en la pestaña anterior para que Aura extraiga los personajes.")

# --- PESTAÑA 6: ESTUDIO GRÁFICO ---
with tab_manga:
    st.header("🎨 Estudio Gráfico de Hércules (Ilustraciones Fieles)")
    paginas = getattr(colmena, "paginas_manga", [])
    if paginas:
        for pag in reversed(paginas):
            st.markdown(f"### 📖 Ilustración Comercial — Cap {pag.get('pag_id')}")
            c1, c2 = st.columns([1, 1])
            with c1:
                st.image(pag.get("imagen_url"), use_container_width=True)
            with c2:
                st.info(pag.get('escena_resumen'))
            st.divider()
    else:
        st.info("No hay ilustraciones generadas aún.")

# --- PESTAÑA 7: BANCO MULTICANAL ---
with tab_redes:
    st.header("📢 Banco Multicanal (Campañas de Ventas)")
    banco = getattr(colmena, "banco_contenido", [])
    if banco:
        for item in reversed(banco):
            st.markdown(f"### 📦 Campaña #{item.get('id')} (Cap {item.get('cap_asociado')})")
            copys = item.get('copys', {})
            st.text_area("Feed / Post:", copys.get('feed', ''), key=f"f_{item.get('id')}", height=120)
            if st.button(f"🚀 Aprobar y Publicar Campaña #{item.get('id')}", key=f"pub_{item.get('id')}"):
                colmena.publicar_o_descartar_contenido(item.get('id'), "publicar")
                st.success("¡Publicado!")
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
            st.markdown(f"### Vídeo — Cap {vid.get('capitulo')}")
            c1, c2 = st.columns([1, 1])
            with c1:
                st.image(vid.get("preview_url"), use_container_width=True)
            with c2:
                st.info(vid.get('guion_voz'))
            st.divider()
    else:
        st.info("No hay vídeos generados.")

# --- PESTAÑA 9: EDITOR DE SCRIPTS ---
with tab_scripts:
    st.header("🛠️ Panel de Edición de Scripts de Hércules")
    scripts_actuales = getattr(colmena, "scripts_personalizados", {})
    with st.form("form_editar_scripts"):
        s_kh = st.text_area("Script para Burbujas de Recuerdos (Kingdom Hearts):", value=scripts_actuales.get("prompt_kingdom_hearts", ""), height=120)
        s_manga = st.text_area("Script para Manga:", value=scripts_actuales.get("prompt_manga", ""), height=100)
        s_video = st.text_area("Script para Vídeo:", value=scripts_actuales.get("prompt_video", ""), height=100)
        if st.form_submit_button("💾 Guardar Scripts"):
            colmena.guardar_scripts_personalizados({"prompt_kingdom_hearts": s_kh, "prompt_manga": s_manga, "prompt_video": s_video})
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
    st.header("⚙️ Configuración y Credenciales de Redes")
    st.write("Introduce y guarda de forma persistente tus claves de acceso para las integraciones oficiales.")
    
    plataforma = st.selectbox("Selecciona la plataforma a configurar:", ["TikTok API", "Instagram / Meta Graph API", "Twitter (X) API", "Google AI Studio", "Wattpad"])
    creds_actuales = colmena.credenciales.get(plataforma, {})
    
    with st.form(f"form_creds_{plataforma}"):
        c1 = st.text_input("Client Key / App ID / API Key / Usuario:", value=creds_actuales.get("campo1", ""))
        c2 = st.text_input("Client Secret / Token / Password:", value=creds_actuales.get("campo2", ""), type="password")
        
        if st.form_submit_button("💾 Guardar y Persistir Credenciales"):
            colmena.guardar_credencial_especifica(plataforma, {"campo1": c1, "campo2": c2})
            st.success(f"¡Credenciales de {plataforma} guardadas correctamente en disco!")
            st.rerun()