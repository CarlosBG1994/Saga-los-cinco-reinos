import streamlit as st
from motor_diario import ColmenaBufferInfinito

st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Co-autoría y Control",
    page_icon="👑",
    layout="wide"
)

if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

colmena = st.session_state.colmena_buffer

st.title("👑 Centro de Co-autoría, Arte & Marketing — Los Cinco Reinos")
st.info("💡 *Sube tus capítulos como archivos .txt en la raíz. Utiliza el nuevo apartado de Co-autoría para que Aura te redacte la continuación, corrija tu ritmo y haga la lectura más amena.*")

estilo_actual = getattr(colmena, "estilo_visual_seleccionado", "Burbujas de Recuerdos (Kingdom Hearts Style)")
nuevo_estilo = st.selectbox(
    "🎨 Estilo de Arte Activo para Hércules:",
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
    "💬 Chat",
    "✍️ Co-autoría y Continuidad",
    "📖 Capítulos",
    "👥 Personajes",
    "🎨 Estudio de Manga",
    "📢 Banco Multicanal",
    "🎬 Vídeos BookTok",
    "🛠️ Editor de Scripts",
    "📊 Métricas",
    "⚙️ Configuración"
])

# --- PESTAÑA 1: OFICINA SIMS ---
with tab_oficina:
    st.header("🖥️ Sala de Trabajo de los Agentes")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("### 👔 Cronos")
        st.info("💻 Coordinación activa.")
    with col_s2:
        st.markdown("### 👩‍💻 Aura")
        dudas = [d for d in colmena.dudas_agentes if not d.get("respondida", False)]
        if dudas:
            st.error("❓ **Duda pendiente**")
            for d in dudas:
                st.warning(f"\"{d['pregunta']}\"")
                resp = st.text_input("Responder:", key=f"d_{d['id']}")
                if st.button("Enviar directriz", key=f"btn_{d['id']}"):
                    colmena.responder_duda(d['id'], resp)
                    st.rerun()
        else:
            st.success("🟢 Lista para co-escribir")
    with col_s3:
        st.markdown("### 🎨 Hércules")
        st.success(f"🟢 Estilo: **{nuevo_estilo}**")

# --- PESTAÑA 2: CHAT ---
with tab_chat:
    st.header("💬 Comunicación Interna")
    for msg in colmena.chat_colmena:
        st.markdown(f"**[{msg['origen']}]:** {msg['mensaje']}")
    with st.form("form_chat"):
        m = st.text_input("Mensaje:")
        if st.form_submit_button("Enviar"):
            colmena.enviar_mensaje_chat("Usuario", m)
            st.rerun()

# --- NUEVA PESTAÑA 3: CO-AUTORÍA Y CONTINUIDAD ---
with tab_coautor:
    st.header("✍️ Taller de Co-autoría, Corrección y Continuidad Literaria")
    st.write("Escribe tu idea para el siguiente paso de la novela o el capítulo que quieres continuar. Aura analizará tu estilo, te corregirá para hacerlo más ameno y diseñará los ganchos de retención para captar al lector.")
    
    with st.form("form_coautor"):
        cap_ref = st.selectbox("Tomar como referencia el Capítulo:", options=list(range(0, 26)), format_func=lambda x: f"Capítulo {x}")
        idea_trama = st.text_area("¿Qué quieres que ocurra en este nuevo fragmento o capítulo?:", placeholder="Ej: El protagonista descubre una pista oculta en una de las burbujas y se cruza con un personaje misterioso...")
        
        if st.form_submit_button("✨ Ordenar a Aura Redactar y Corregir Continuación"):
            if idea_trama:
                colmena.generar_ayuda_continuacion(idea_trama, cap_ref)
                st.success("¡Aura ha procesado la propuesta literaria!")
                st.rerun()
            else:
                st.warning("Introduce una idea para la trama.")
                
    st.markdown("---")
    st.subheader("📜 Propuestas y Correcciones Generadas por Aura:")
    propuestas = getattr(colmena, "propuestas_escritura", [])
    if propuestas:
        for prop in reversed(propuestas):
            st.info(f"**Referencia: Capítulo {prop['capitulo_ref']}** (Idea: *{prop['idea']}*)")
            st.markdown(prop['resultado'])
            st.divider()
    else:
        st.info("No hay propuestas de co-autoría generadas todavía. Introduce una idea arriba para empezar.")

# --- PESTAÑA 4: CAPÍTULOS ---
with tab_capitulos:
    st.header("📖 Capítulos (Leyendo archivos .txt en la raíz)")
    num_cap = st.selectbox("Selecciona Capítulo:", options=list(range(0, 26)), format_func=lambda x: f"Capítulo {x}")
    info = colmena.obtener_capitulo(num_cap)
    st.markdown(f"### 👑 {info['titulo']}")
    st.text_area("Contenido limpio detectado:", info["descripcion"], height=180)
    if info["descripcion"] and "pendiente" not in info["descripcion"].lower():
        colmena.ciclo_autonomo_marketing_inteligente(num_cap, info["descripcion"])
        st.success("¡Capítulo analizado con éxito por la colmena!")

# --- PESTAÑA 5: PERSONAJES ---
with tab_bocetos:
    st.header("👥 Biblioteca de Personajes")
    for p in reversed(colmena.lore_universo):
        st.markdown(f"### 👤 {p['nombre']}")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.image(p.get("boceto_url"), use_container_width=True)
        with c2:
            st.write(p['descripcion'])
        st.divider()

# --- PESTAÑA 6: ESTUDIO DE MANGA ---
with tab_manga:
    st.header("🎨 Estudio de Manga e Ilustraciones Fieles")
    for pag in reversed(colmena.paginas_manga):
        st.markdown(f"### 📖 Ilustración — Cap {pag.get('pag_id')}")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.image(pag.get("imagen_url"), use_container_width=True)
        with c2:
            st.info(pag.get('escena_resumen'))
        st.divider()

# --- PESTAÑA 7: BANCO MULTICANAL ---
with tab_redes:
    st.header("📢 Banco Multicanal")
    for item in reversed(colmena.banco_contenido):
        st.markdown(f"### 📦 Campaña #{item.get('id')} (Cap {item.get('cap_asociado')})")
        copys = item.get('copys', {})
        st.text_area("Feed:", copys.get('feed', ''), key=f"f_{item.get('id')}")
        if st.button(f"🚀 Publicar #{item.get('id')}", key=f"pub_{item.get('id')}"):
            colmena.publicar_o_descartar_contenido(item.get('id'), "publicar")
            st.rerun()
        st.divider()

# --- PESTAÑA 8: VÍDEOS ---
with tab_videos:
    st.header("🎬 Vídeos BookTok")
    for vid in reversed(colmena.videos_tiktok):
        st.markdown(f"### Vídeo — Cap {vid.get('capitulo')}")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.image(vid.get("preview_url"), use_container_width=True)
        with c2:
            st.info(vid.get('guion_voz'))
        st.divider()

# --- PESTAÑA 9: EDITOR DE SCRIPTS ---
with tab_scripts:
    st.header("🛠️ Panel de Edición de Scripts de Hércules")
    scripts_actuales = getattr(colmena, "scripts_personalizados", {})
    with st.form("form_editar_scripts"):
        s_kh = st.text_area("Script para Burbujas de Recuerdos:", value=scripts_actuales.get("prompt_kingdom_hearts", ""), height=120)
        s_manga = st.text_area("Script para Manga:", value=scripts_actuales.get("prompt_manga", ""), height=100)
        s_video = st.text_area("Script para Vídeo:", value=scripts_actuales.get("prompt_video", ""), height=100)
        if st.form_submit_button("💾 Guardar Scripts"):
            colmena.guardar_scripts_personalizados({"prompt_kingdom_hearts": s_kh, "prompt_manga": s_manga, "prompt_video": s_video})
            st.success("¡Scripts guardados!")
            st.rerun()

# --- PESTAÑA 10: MÉTRICAS ---
with tab_metricas:
    st.header("📊 Métricas de Redes")
    for plat, datos in colmena.metricas_redes.items():
        st.metric(plat, f"{datos.get('seguidores')} seguidores")

# --- PESTAÑA 11: CONFIGURACIÓN ---
with tab_config:
    st.header("⚙️ Configuración Segura")
    st.write("Credenciales persistidas.")