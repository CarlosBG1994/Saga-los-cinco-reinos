import streamlit as st
from motor_diario import ColmenaBufferInfinito

st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Centro Mangaka",
    page_icon="👑",
    layout="wide"
)

# Inicialización segura que previene errores de atributos antiguos en caché
if "colmena_buffer" not in st.session_state or not hasattr(st.session_state.colmena_buffer, "procesar_autonomia_capitulo"):
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

colmena = st.session_state.colmena_buffer

st.title("👑 Centro de Mando & Mangaka - Los Cinco Reinos")
st.info("💡 *Gestión avanzada: Aura describe con precisión, Hércules diseña bocetos editables por personaje y estructura las páginas de manga.*")

tab_capitulos, tab_bocetos, tab_manga, tab_asistencia, tab_redes, tab_videos, tab_wattpad, tab_config = st.tabs([
    "📖 Capítulos y Órdenes",
    "👥 Biblioteca de Personajes (Bocetos)",
    "🎨 Estudio de Manga",
    "❓ Buzón Inteligente",
    "📢 Banco Multicanal (Aprobar / Borrar)",
    "🎬 Vídeos (Reels / TikTok)",
    "🔗 Conexión Wattpad",
    "⚙️ Configuración"
])

# --- PESTAÑA 1: CAPÍTULOS Y ÓRDENES ---
with tab_capitulos:
    st.header("📖 Explorador de Capítulos y Automatización")
    num_cap = st.selectbox("Selecciona el Capítulo:", options=list(range(0, 26)), format_func=lambda x: f"Capítulo {x}")
    
    info_cap = colmena.obtener_capitulo(num_cap)
    st.markdown(f"### 👑 {info_cap['titulo']}")
    st.text_area("Contenido real:", info_cap["descripcion"], height=200)
    
    if info_cap["descripcion"] and "pendiente" not in info_cap["descripcion"].lower():
        colmena.procesar_autonomia_capitulo(num_cap, info_cap["descripcion"])
    
    st.markdown("---")
    st.subheader("🚀 Generar Paquete Multicanal para Redes:")
    instruccion_user = st.text_area("Directrices adicionales para los copys y vídeos:")
    if st.button("✨ Generar Contenido para Redes"):
        colmena.generar_paquete_creativo_completo(instruccion_user, num_cap)
        st.success("¡Contenido generado y enviado al Banco Multicanal!")
        st.rerun()

# --- PESTAÑA 2: BIBLIOTECA DE PERSONAJES Y BOCETOS ---
with tab_bocetos:
    st.header("👥 Biblioteca de Personajes y Bocetos Editables")
    st.write("Aura define a los personajes con precisión milimétrica y Hércules genera un boceto visual inicial que puedes modificar las veces que quieras.")
    
    with st.expander("➕ Añadir nuevo Personaje a la Biblioteca"):
        with st.form("form_nuevo_pj"):
            nombre_pj = st.text_input("Nombre del Personaje:")
            desc_pj = st.text_area("Rasgos físicos, vestimenta, expresiones y trasfondo:")
            if st.form_submit_button("🎨 Generar Personaje y Boceto Inicial"):
                if nombre_pj and desc_pj:
                    colmena.guardar_personaje_con_boceto(nombre_pj, desc_pj)
                    st.success(f"¡Personaje '{nombre_pj}' creado con su boceto inicial!")
                    st.rerun()
                else:
                    st.warning("Rellena todos los campos.")

    st.markdown("---")
    lista_lore = getattr(colmena, "lore_universo", [])
    personajes = [p for p in lista_lore if p["categoria"] == "Personaje"]
    
    if personajes:
        for p in reversed(personajes):
            p_id = p["id"]
            st.markdown(f"### 👤 {p['nombre']}")
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                if p.get("boceto_url"):
                    st.image(p["boceto_url"], caption=f"Boceto actual de {p['nombre']}", use_container_width=True)
                else:
                    st.info("Sin boceto generado.")
            with col_b2:
                st.write(f"**Descripción actual (Aura):**\n{p['descripcion']}")
                
                nueva_desc = st.text_area(f"Modificar rasgos de {p['nombre']}:", value=p['descripcion'], key=f"desc_pj_{p_id}")
                if st.button(f"🔄 Actualizar y Redibujar Boceto de {p['nombre']}", key=f"btn_upd_{p_id}"):
                    colmena.actualizar_boceto_personaje(p_id, nueva_desc)
                    st.success("¡Boceto actualizado con éxito por Hércules!")
                    st.rerun()
                    
                if st.button(f"🗑️ Eliminar Personaje '{p['nombre']}'", key=f"del_pj_{p_id}"):
                    colmena.eliminar_elemento_lore(p_id)
                    st.rerun()
            st.divider()
    else:
        st.info("No hay personajes registrados en la biblioteca.")

# --- PESTAÑA 3: ESTUDIO DE MANGA ---
with tab_manga:
    st.header("🎨 Estudio de Manga (Adaptación de la Novela)")
    st.write("Hércules diseña las páginas de manga basándose en los capítulos. Puedes elegir si quieres aplicar la metáfora visual del lector en la biblioteca y un pensamiento con la escena del libro.")
    
    with st.form("form_crear_manga"):
        cap_manga_sel = st.selectbox("Seleccionar Capítulo para Adaptar:", options=list(range(0, 26)), format_func=lambda x: f"Capítulo {x}")
        estilo_opcion = st.selectbox(
            "Enfoque Narrativo y Visual de Hércules:",
            [
                "Estándar (Acción y Diálogo Fiel)",
                "Especial: Lector en Biblioteca + Pensamiento con Escena del Libro",
                "Clímax Dramático (Viñetas cinemáticas)"
            ]
        )
        if st.form_submit_button("🖌️ Ordenar a Hércules Dibujar Página de Manga"):
            colmena.generar_pagina_manga_capitulo(cap_manga_sel, estilo_opcion)
            st.success("¡Página de manga generada y añadida al estudio!")
            st.rerun()

    st.markdown("---")
    st.subheader("📚 Páginas de Manga Generadas")
    paginas = getattr(colmena, "paginas_manga", [])
    if paginas:
        for pag in reversed(paginas):
            pag_id = pag.get('pag_id')
            st.markdown(f"### 📖 Página de Manga — Capítulo {pag_id}")
            col_m1, col_m2 = st.columns([1, 1])
            with col_m1:
                st.image(pag.get("imagen_url"), use_container_width=True)
            with col_m2:
                st.info(f"**Escena / Composición:**\n{pag.get('escena_resumen', '')}")
                st.write(f"**Guion de Viñetas:**\n{pag.get('guion_viñetas', '')}")
                if st.button(f"🗑️ Eliminar Página #{pag_id}", key=f"del_m_{pag_id}"):
                    colmena.eliminar_pagina_manga(pag_id)
                    st.rerun()
            st.divider()
    else:
        st.info("No hay páginas de manga en el estudio todavía.")

# --- PESTAÑA 4: BUZÓN INTELIGENTE ---
with tab_asistencia:
    st.header("❓ Buzón de Dudas Inteligente")
    dudas = getattr(colmena, "dudas_agentes", [])
    if dudas:
        for d in reversed(dudas):
            estado_txt = "✅ **Respondida**" if d["respondida"] else "⚠️ **Requiere respuesta**"
            st.markdown(f"**[{d['timestamp']}] {d['agente']}** — {estado_txt}")
            st.info(f"💬 \"{d['pregunta']}\"")
            if d["respondida"]:
                st.success(f"**Tu directriz:** {d['respuesta']}")
            else:
                resp_txt = st.text_input("Responder:", key=f"resp_d_{d['id']}")
                if st.button(f"Guardar #{d['id']}", key=f"btn_d_{d['id']}"):
                    if resp_txt:
                        colmena.responder_duda(d['id'], resp_txt)
                        st.success("¡Directriz guardada!")
                        st.rerun()
            st.divider()
    else:
        st.info("No hay dudas pendientes.")

# --- PESTAÑA 5: BANCO MULTICANAL ---
with tab_redes:
    st.header("📢 Banco Multicanal (Aprobar o Eliminar)")
    banco = getattr(colmena, "banco_contenido", [])
    if banco:
        for item in reversed(banco):
            item_id = item.get('id')
            copys = item.get('copys', {})
            st.markdown(f"### 📦 Publicación #{item_id} (Capítulo {item.get('cap_asociado', 'N/A')})")
            st.caption(f"Estado: **{item.get('estado', 'Pendiente')}**")
            
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                st.text_area("Feed:", copys.get('feed', ''), height=110, key=f"f_{item_id}")
            with col_c2:
                st.text_area("TikTok / Reel:", copys.get('tiktok_reel', ''), height=110, key=f"t_{item_id}")
            with col_c3:
                st.text_area("Historias:", copys.get('historia', ''), height=110, key=f"h_{item_id}")
            
            c_a1, c_a2 = st.columns(2)
            with c_a1:
                if st.button(f"🚀 Aprobar y Publicar #{item_id}", key=f"pub_{item_id}"):
                    colmena.publicar_o_descartar_contenido(item_id, "publicar")
                    st.success("¡Aprobado!")
                    st.rerun()
            with c_a2:
                if st.button(f"🗑️ Eliminar #{item_id}", key=f"del_b_{item_id}"):
                    colmena.publicar_o_descartar_contenido(item_id, "eliminar")
                    st.warning("Eliminado.")
                    st.rerun()
            st.divider()
    else:
        st.info("Banco vacío.")

# --- PESTAÑA 6: VÍDEOS ---
with tab_videos:
    st.header("🎬 Vídeos Conceptuales Verticales")
    videos = getattr(colmena, "videos_tiktok", [])
    if videos:
        for vid in reversed(videos):
            vid_id = vid.get('id')
            st.markdown(f"### Vídeo — Capítulo {vid.get('capitulo', 'N/A')}")
            c_v1, c_v2 = st.columns([1, 1])
            with c_v1:
                st.image(vid.get("preview_url"), use_container_width=True)
            with c_v2:
                st.info(f"**Guion:**\n{vid.get('guion_voz', '')}")
                if st.button(f"🗑️ Eliminar Vídeo #{vid_id}", key=f"del_v_{vid_id}"):
                    colmena.eliminar_video_tiktok(vid_id)
                    st.rerun()
            st.divider()
    else:
        st.info("No hay vídeos.")

# --- PESTAÑA 7: WATTPAD ---
with tab_wattpad:
    st.header("🔗 Conexión con Wattpad")
    url_wattpad = st.text_input("Enlace público:")
    if st.button("Asimilar Lore"):
        if url_wattpad:
            res = colmena.asimilar_historia_wattpad(url_wattpad)
            st.success("¡Asimilado!")
            st.text_area("Resultado:", res, height=150)

# --- PESTAÑA 8: CONFIGURACIÓN ---
with tab_config:
    st.header("⚙️ Configuración")
    serv = st.selectbox("Plataforma:", ["TikTok API", "Instagram / Meta Graph API", "Twitter (X) API", "Google AI Studio", "Wattpad"])
    with st.form("form_conf"):
        val = st.text_input("Token o Credencial:", type="password")
        if st.form_submit_button("Guardar"):
            colmena.guardar_credencial_especifica(serv, {"token": val})
            st.success("¡Guardado!")
            st.rerun()