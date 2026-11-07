import streamlit as st
from motor_diario import ColmenaBufferInfinito

st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Centro Autodidacta",
    page_icon="👑",
    layout="wide"
)

if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

colmena = st.session_state.colmena_buffer

st.title("👑 Centro Autodidacta de Mando & Mangaka — Los Cinco Reinos")
st.info("💡 *Modo Autodidacta Activo: Los agentes analizan los capítulos por su cuenta, proponen páginas de manga y copys avanzados, y solo te consultan si tienen dudas.*")

tab_capitulos, tab_bocetos, tab_manga, tab_asistencia, tab_redes, tab_videos, tab_wattpad, tab_config = st.tabs([
    "📖 Capítulos y Análisis Autónomo",
    "👥 Biblioteca de Personajes (Bocetos)",
    "🎨 Estudio de Manga",
    "❓ Buzón de Dudas (Agentes)",
    "📢 Banco Multicanal (Aprobar / Borrar)",
    "🎬 Vídeos (Reels / TikTok)",
    "🔗 Conexión Wattpad",
    "⚙️ Configuración"
])

# --- PESTAÑA 1: CAPÍTULOS Y ANÁLISIS AUTÓNOMO ---
with tab_capitulos:
    st.header("📖 Explorador de Capítulos y Acciones Proactivas")
    num_cap = st.selectbox("Selecciona el Capítulo:", options=list(range(0, 26)), format_func=lambda x: f"Capítulo {x}")
    
    info_cap = colmena.obtener_capitulo(num_cap)
    st.markdown(f"### 👑 {info_cap['titulo']}")
    st.text_area("Contenido real detectado:", info_cap["descripcion"], height=200)
    
    if info_cap["descripcion"] and "pendiente" not in info_cap["descripcion"].lower():
        colmena.procesar_autonomia_capitulo(num_cap, info_cap["descripcion"])
        st.success("🤖 *Aura y Hércules han analizado el capítulo de forma autónoma. Revisa el Estudio de Manga y el Banco Multicanal para ver sus propuestas.*")
    
    st.markdown("---")
    st.subheader("🚀 Forzar Paquete Creativo Adicional:")
    instruccion_user = st.text_area("Directrices adicionales (opcional, si quieres guiarles en algo específico):")
    if st.button("✨ Forzar Generación Extra"):
        colmena.generar_paquete_creativo_completo(instruccion_user, num_cap)
        st.success("¡Nuevo contenido generado!")
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
        for idx, p in enumerate(reversed(personajes)):
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
                
                nueva_desc = st.text_area(f"Modificar rasgos de {p['nombre']}:", value=p['descripcion'], key=f"desc_pj_{p_id}_{idx}")
                if st.button(f"🔄 Actualizar y Redibujar Boceto de {p['nombre']}", key=f"btn_upd_{p_id}_{idx}"):
                    colmena.actualizar_boceto_personaje(p_id, nueva_desc)
                    st.success("¡Boceto actualizado con éxito por Hércules!")
                    st.rerun()
                    
                if st.button(f"🗑️ Eliminar Personaje '{p['nombre']}'", key=f"del_pj_{p_id}_{idx}"):
                    colmena.eliminar_elemento_lore(p_id)
                    st.rerun()
            st.divider()
    else:
        st.info("No hay personajes registrados en la biblioteca.")

# --- PESTAÑA 3: ESTUDIO DE MANGA ---
with tab_manga:
    st.header("🎨 Estudio de Manga (Adaptación Autónoma)")
    st.write("Hércules diseña las páginas de manga aplicando criterios avanzados (como la metáfora del lector en la biblioteca).")
    
    with st.form("form_crear_manga"):
        cap_manga_sel = st.selectbox("Seleccionar Capítulo:", options=list(range(0, 26)), format_func=lambda x: f"Capítulo {x}")
        estilo_opcion = st.selectbox(
            "Enfoque Narrativo:",
            [
                "Especial: Lector en Biblioteca + Pensamiento con Escena del Libro",
                "Estándar (Acción y Diálogo Fiel)",
                "Clímax Dramático (Viñetas cinemáticas)"
            ]
        )
        if st.form_submit_button("🖌️ Ordenar a Hércules Dibujar Nueva Página"):
            colmena.generar_pagina_manga_capitulo(cap_manga_sel, estilo_opcion)
            st.success("¡Página generada!")
            st.rerun()

    st.markdown("---")
    st.subheader("📚 Páginas de Manga (Propuestas Autónomas y Manuales)")
    paginas = getattr(colmena, "paginas_manga", [])
    if paginas:
        for idx, pag in enumerate(reversed(paginas)):
            pag_id = pag.get('pag_id', idx)
            st.markdown(f"### 📖 Página de Manga — Capítulo {pag_id}")
            col_m1, col_m2 = st.columns([1, 1])
            with col_m1:
                st.image(pag.get("imagen_url"), use_container_width=True)
            with col_m2:
                st.info(f"**Escena / Composición:**\n{pag.get('escena_resumen', '')}")
                st.write(f"**Guion de Viñetas:**\n{pag.get('guion_viñetas', '')}")
                if st.button(f"🗑️ Eliminar Página #{pag_id}", key=f"del_m_{pag_id}_{idx}"):
                    colmena.eliminar_pagina_manga(pag_id)
                    st.rerun()
            st.divider()
    else:
        st.info("No hay páginas en el estudio todavía.")

# --- PESTAÑA 4: BUZÓN DE DUDAS ---
with tab_asistencia:
    st.header("❓ Buzón de Dudas (Consultas de los Agentes)")
    st.write("Aquí te preguntarán si tienen ambigüedades al analizar tus capítulos de forma autodidacta.")
    dudas = getattr(colmena, "dudas_agentes", [])
    if dudas:
        for idx, d in enumerate(reversed(dudas)):
            estado_txt = "✅ **Respondida**" if d["respondida"] else "⚠️ **Requiere tu respuesta**"
            st.markdown(f"**[{d['timestamp']}] {d['agente']}** — {estado_txt}")
            st.info(f"💬 \"{d['pregunta']}\"")
            if d["respondida"]:
                st.success(f"**Tu directriz:** {d['respuesta']}")
            else:
                resp_txt = st.text_input("Responder:", key=f"resp_d_{d['id']}_{idx}")
                if st.button(f"Guardar respuesta #{d['id']}", key=f"btn_d_{d['id']}_{idx}"):
                    if resp_txt:
                        colmena.responder_duda(d['id'], resp_txt)
                        st.success("¡Directriz aplicada!")
                        st.rerun()
            st.divider()
    else:
        st.info("No hay dudas pendientes. Los agentes están trabajando con criterio propio.")

# --- PESTAÑA 5: BANCO MULTICANAL ---
with tab_redes:
    st.header("📢 Banco Multicanal (Aprobar o Publicar)")
    banco = getattr(colmena, "banco_contenido", [])
    if banco:
        for idx, item in enumerate(reversed(banco)):
            item_id = item.get('id', idx)
            copys = item.get('copys', {})
            st.markdown(f"### 📦 Propuesta #{item_id} (Capítulo {item.get('cap_asociado', 'N/A')})")
            st.caption(f"Estado: **{item.get('estado', 'Pendiente')}**")
            
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                st.text_area("Feed:", copys.get('feed', ''), height=110, key=f"f_{item_id}_{idx}")
            with col_c2:
                st.text_area("TikTok / Reel:", copys.get('tiktok_reel', ''), height=110, key=f"t_{item_id}_{idx}")
            with col_c3:
                st.text_area("Historias:", copys.get('historia', ''), height=110, key=f"h_{item_id}_{idx}")
            
            c_a1, c_a2 = st.columns(2)
            with c_a1:
                if st.button(f"🚀 Aprobar y Publicar #{item_id}", key=f"pub_{item_id}_{idx}"):
                    colmena.publicar_o_descartar_contenido(item_id, "publicar")
                    st.success("¡Aprobado para redes!")
                    st.rerun()
            with c_a2:
                if st.button(f"🗑️ Descartar #{item_id}", key=f"del_b_{item_id}_{idx}"):
                    colmena.publicar_o_descartar_contenido(item_id, "eliminar")
                    st.warning("Descartado.")
                    st.rerun()
            st.divider()
    else:
        st.info("Banco vacío. Selecciona un capítulo en la primera pestaña para que los agentes comiencen su análisis autónomo.")

# --- PESTAÑA 6: VÍDEOS ---
with tab_videos:
    st.header("🎬 Vídeos Conceptuales Verticales")
    videos = getattr(colmena, "videos_tiktok", [])
    if videos:
        for idx, vid in enumerate(reversed(videos)):
            vid_id = vid.get('id', idx)
            st.markdown(f"### Vídeo Proactivo — Capítulo {vid.get('capitulo', 'N/A')}")
            c_v1, c_v2 = st.columns([1, 1])
            with c_v1:
                st.image(vid.get("preview_url"), use_container_width=True)
            with c_v2:
                st.info(f"**Guion de voz:**\n{vid.get('guion_voz', '')}")
                if st.button(f"🗑️ Eliminar Vídeo #{vid_id}", key=f"del_v_{vid_id}_{idx}"):
                    colmena.eliminar_video_tiktok(vid_id)
                    st.rerun()
            st.divider()
    else:
        st.info("No hay vídeos generados.")

# --- PESTAÑA 7: WATTPAD ---
with tab_wattpad:
    st.header("🔗 Conexión con Wattpad")
    url_wattpad = st.text_input("Enlace público:")
    if st.button("Asimilar Lore"):
        if url_wattpad:
            res = colmena.asimilar_historia_wattpad(url_wattpad)
            st.success("¡Asimilado!")
            st.text_area("Resultado:", res, height=150)

# --- PESTAÑA 8: CONFIGURACIÓN DINÁMICA DE REDES Y PLATAFORMAS ---
with tab_config:
    st.header("⚙️ Configuración y Credenciales de Redes")
    st.write("Selecciona una plataforma para configurar sus parámetros específicos de acceso e integración.")
    
    plataforma_elegida = st.selectbox(
        "Selecciona la plataforma a configurar:",
        [
            "TikTok API", 
            "Instagram / Meta Graph API", 
            "Twitter (X) API", 
            "Google AI Studio", 
            "Wattpad"
        ]
    )
    
    with st.form(f"form_conf_{plataforma_elegida}"):
        credenciales_actuales = colmena.credenciales.get(plataforma_elegida, {})
        
        if plataforma_elegida == "TikTok API":
            st.subheader("Configuración para TikTok")
            client_key = st.text_input("Client Key / App ID:", value=credenciales_actuales.get("client_key", ""), type="default")
            client_secret = st.text_input("Client Secret:", value=credenciales_actuales.get("client_secret", ""), type="password")
            access_token = st.text_input("Access Token / Creator Token:", value=credenciales_actuales.get("access_token", ""), type="password")
            
        elif plataforma_elegida == "Instagram / Meta Graph API":
            st.subheader("Configuración para Instagram y Facebook (Meta)")
            app_id = st.text_input("Meta App ID:", value=credenciales_actuales.get("app_id", ""))
            app_secret = st.text_input("Meta App Secret:", value=credenciales_actuales.get("app_secret", ""), type="password")
            page_token = st.text_input("Page / User Access Token:", value=credenciales_actuales.get("page_token", ""), type="password")
            instagram_account_id = st.text_input("Instagram Business Account ID:", value=credenciales_actuales.get("instagram_account_id", ""))
            
        elif plataforma_elegida == "Twitter (X) API":
            st.subheader("Configuración para Twitter / X")
            api_key = st.text_input("API Key (Consumer Key):", value=credenciales_actuales.get("api_key", ""))
            api_secret = st.text_input("API Secret (Consumer Secret):", value=credenciales_actuales.get("api_secret", ""), type="password")
            bearer_token = st.text_input("Bearer Token:", value=credenciales_actuales.get("bearer_token", ""), type="password")
            access_token_x = st.text_input("Access Token:", value=credenciales_actuales.get("access_token_x", ""), type="password")
            
        elif plataforma_elegida == "Google AI Studio":
            st.subheader("Configuración para Google AI Studio")
            api_key_google = st.text_input("Google Gemini API Key:", value=credenciales_actuales.get("api_key_google", ""), type="password")
            
        elif plataforma_elegida == "Wattpad":
            st.subheader("Configuración para Wattpad")
            wattpad_user = st.text_input("Usuario o Correo de Wattpad:", value=credenciales_actuales.get("wattpad_user", ""))
            wattpad_token = st.text_input("Token de Autorización / API Key:", value=credenciales_actuales.get("wattpad_token", ""), type="password")
        
        if st.form_submit_button(f"💾 Guardar Credenciales de {plataforma_elegida}"):
            # Recopilamos todos los datos del formulario actual
            datos_a_guardar = {}
            if plataforma_elegida == "TikTok API":
                datos_a_guardar = {"client_key": client_key, "client_secret": client_secret, "access_token": access_token}
            elif plataforma_elegida == "Instagram / Meta Graph API":
                datos_a_guardar = {"app_id": app_id, "app_secret": app_secret, "page_token": page_token, "instagram_account_id": instagram_account_id}
            elif plataforma_elegida == "Twitter (X) API":
                datos_a_guardar = {"api_key": api_key, "api_secret": api_secret, "bearer_token": bearer_token, "access_token_x": access_token_x}
            elif plataforma_elegida == "Google AI Studio":
                datos_a_guardar = {"api_key_google": api_key_google}
            elif plataforma_elegida == "Wattpad":
                datos_a_guardar = {"wattpad_user": wattpad_user, "wattpad_token": wattpad_token}
                
            colmena.guardar_credencial_especifica(plataforma_elegida, datos_a_guardar)
            st.success(f"¡Credenciales para {plataforma_elegida} guardadas correctamente con todos sus campos!")
            st.rerun()