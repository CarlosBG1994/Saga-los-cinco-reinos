import streamlit as st
from motor_diario import ColmenaBufferInfinito

st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Centro de Mando",
    page_icon="👑",
    layout="wide"
)

if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

colmena = st.session_state.colmena_buffer

st.title("👑 Centro de Mando - Saga: Los Cinco Reinos")
st.info("💡 *Modo Coherente Interactivo: Análisis de capítulos, buzón de dudas, atlas de lore y credenciales estructuradas.*")

# Las 7 pestañas principales del Centro de Mando
tab_capitulos, tab_lore, tab_asistencia, tab_redes, tab_manga, tab_wattpad, tab_config = st.tabs([
    "📖 Capítulos y Órdenes",
    "🗺️ Personajes, Mapas y Bestiario",
    "❓ Buzón de Dudas (Agentes Activos)",
    "📢 Contenido y Redes",
    "🎨 Visor de Manga",
    "🔗 Conexión Wattpad",
    "⚙️ Configuración y Credenciales"
])

# --- PESTAÑA 1: CAPÍTULOS Y ÓRDENES ---
with tab_capitulos:
    st.header("📖 Explorador de Capítulos y Activación de Agentes")
    st.write("Selecciona un capítulo real de tu repositorio. Al seleccionarlo, Aura y Hércules lo leerán y te plantearán sus dudas en el buzón.")
    
    num_cap = st.selectbox(
        "Selecciona el Capítulo:",
        options=list(range(0, 26)),
        format_func=lambda x: f"Capítulo {x}"
    )
    
    info_cap = colmena.obtener_capitulo(num_cap)
    st.markdown(f"### 👑 {info_cap['titulo']}")
    st.text_area("Contenido real detectado en la raíz:", info_cap["descripcion"], height=250)
    
    if info_cap["descripcion"] and "Aún no se ha encontrado" not in info_cap["descripcion"]:
        colmena.generar_dudas_automaticas_capitulo(num_cap, info_cap["descripcion"])
    
    st.markdown("---")
    st.subheader("🛠️ Dar orden directa a los agentes sobre este capítulo:")
    instruccion_user = st.text_input("¿Qué quieres que Aura redacte o continúe basándose en este capítulo?")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✍️ Ordenar a Aura redactar texto coherente"):
            if instruccion_user:
                colmena.generar_contenido_manual(instruccion_user, num_cap)
                st.success("¡Borrador generado y añadido a la pestaña de Contenido!")
                st.rerun()
            else:
                st.warning("Escribe una directriz clara para Aura.")
                
    with col_btn2:
        if st.button("🎨 Ordenar a Hércules crear plancha de este capítulo"):
            colmena.generar_manga_manual(num_cap)
            st.success("¡Plancha de manga estructurada y añadida al Visor!")
            st.rerun()

# --- PESTAÑA 2: PERSONAJES, MAPAS Y BESTIARIO ---
with tab_lore:
    st.header("🗺️ Atlas de la Saga: Personajes, Mapas y Bestiario")
    st.write("Gestiona la base de datos oficial del universo de Los Cinco Reinos.")
    
    with st.form("form_nuevo_lore"):
        st.subheader("➕ Añadir nuevo elemento al Lore")
        cat_lore = st.selectbox("Categoría:", ["Personaje", "Mapa / Lugar", "Bestiario"])
        nombre_lore = st.text_input("Nombre:")
        desc_lore = st.text_area("Descripción y trasfondo:")
        
        if st.form_submit_button("💾 Guardar en la Base de Datos"):
            if nombre_lore and desc_lore:
                colmena.guardar_elemento_lore(cat_lore, nombre_lore, desc_lore)
                st.success(f"¡'{nombre_lore}' guardado con éxito!")
                st.rerun()
            else:
                st.warning("Rellena el nombre y la descripción.")

    st.markdown("---")
    st.subheader("📚 Elementos Registrados")
    lista_lore = getattr(colmena, "lore_universo", [])
    if lista_lore:
        filtro_cat = st.radio("Filtrar por categoría:", ["Todos", "Personaje", "Mapa / Lugar", "Bestiario"], horizontal=True)
        for elem in reversed(lista_lore):
            if filtro_cat == "Todos" or elem["categoria"] == filtro_cat:
                elem_id = elem["id"]
                st.markdown(f"### [{elem['categoria']}] {elem['nombre']}")
                st.write(elem['descripcion'])
                if st.button(f"🗑️ Eliminar '{elem['nombre']}'", key=f"del_lore_{elem_id}"):
                    colmena.eliminar_elemento_lore(elem_id)
                    st.rerun()
                st.divider()
    else:
        st.info("Aún no hay elementos registrados.")

# --- PESTAÑA 3: BUZÓN DE DUDAS (AGENTES ACTIVOS) ---
with tab_asistencia:
    st.header("❓ Buzón de Dudas (Consultas Activas de los Agentes)")
    st.write("Aquí verás las preguntas que Aura y Hércules te hacen al analizar tus capítulos para asegurarte de que trabajan exactamente como deseas.")
    
    nueva_duda = st.text_input("Plantear una duda o regla adicional a los agentes:")
    agente_destino = st.selectbox("¿A qué agente va dirigida?", ["Aura (Co-autora)", "Hércules (Mangaka)"])
    if st.button("Enviar consulta personalizada"):
        if nueva_duda:
            colmena.registrar_duda(nueva_duda, agente_destino)
            st.success("¡Consulta registrada!")
            st.rerun()
            
    st.markdown("---")
    st.subheader("📋 Preguntas pendientes de los Agentes")
    dudas = getattr(colmena, "dudas_agentes", [])
    if dudas:
        for d in reversed(dudas):
            estado_txt = "✅ **Respondida**" if d["respondida"] else "⚠️ **Requiere tu respuesta**"
            st.markdown(f"**[{d['timestamp']}] {d['agente']}** — {estado_txt}")
            st.info(f"💬 \"{d['pregunta']}\"")
            
            if d["respondida"]:
                st.success(f"**Tu directriz activa:** {d['respuesta']}")
            else:
                resp_key = f"resp_{d['id']}"
                resp_txt = st.text_input(f"Responder a {d['agente']}:", key=resp_key)
                if st.button(f"Guardar respuesta #{d['id']}", key=f"btn_duda_{d['id']}"):
                    if resp_txt:
                        colmena.responder_duda(d['id'], resp_txt)
                        st.success("¡Respuesta guardada! Los agentes aplicarán esta directriz.")
                        st.rerun()
            st.divider()
    else:
        st.info("No hay dudas pendientes. Explora los capítulos en la primera pestaña para que los agentes comiencen a analizar.")

# --- PESTAÑA 4: CONTENIDO Y MÉTRICAS DE REDES ---
with tab_redes:
    st.header("📢 Contenido y Métricas de Redes Sociales")
    st.write("Supervisa el contenido generado, aprueba publicaciones y registra las métricas de rendimiento de cada plataforma.")
    
    st.subheader("📊 Panel de Métricas por Red Social")
    metricas_guardadas = getattr(colmena, "metricas_redes", {})
    cols_met = st.columns(len(metricas_guardadas) if metricas_guardadas else 1)
    
    for idx, (plat, datos) in enumerate(metricas_guardadas.items()):
        with cols_met[idx]:
            st.markdown(f"### 📱 {plat}")
            st.metric("Seguidores", datos.get("seguidores", 0))
            st.metric("Rendimiento / Alcance", datos.get("rendimiento_principal", 0))
            st.metric("Interacciones", datos.get("interacciones", 0))
            st.caption(f"Actualizado: {datos.get('ultima_actualizacion', 'N/A')}")

    st.markdown("---")
    with st.expander("🔄 Actualizar Métricas Manualmente (o vía Token de API)"):
        with st.form("form_act_metricas"):
            plat_sel = st.selectbox("Plataforma a actualizar:", ["Instagram", "TikTok", "Twitter (X)"])
            seg_input = st.number_input("Número de seguidores:", min_value=0, value=0)
            rend_input = st.number_input("Alcance / Visualizaciones recientes:", min_value=0, value=0)
            inter_input = st.number_input("Interacciones totales:", min_value=0, value=0)
            
            if st.form_submit_button("💾 Guardar y Sincronizar Métricas"):
                colmena.actualizar_metricas_red(plat_sel, seg_input, rend_input, inter_input)
                st.success(f"¡Métricas de {plat_sel} actualizadas con éxito!")
                st.rerun()

    st.markdown("---")
    st.subheader("📝 Banco de Contenido Programado")
    banco = getattr(colmena, "banco_contenido_semanal", [])
    if banco:
        for item in reversed(banco):
            item_id = item.get('id', 1)
            st.markdown(f"**Item #{item_id}** (Capítulo asociado: {item.get('cap_asociado', 'N/A')})")
            st.text_area(f"Texto #{item_id}", item.get('texto', ''), height=100, key=f"txt_{item_id}")
            if st.button(f"🗑️ Eliminar Item #{item_id}", key=f"del_item_{item_id}"):
                colmena.eliminar_item_banco(item_id)
                st.rerun()
            st.divider()
    else:
        st.info("No hay contenido generado en este momento.")

# --- PESTAÑA 5: VISOR DE MANGA ---
with tab_manga:
    st.header("🎨 Visor de Planchas de Manga")
    paginas = getattr(colmena, "paginas_manga", [])
    if paginas:
        for pag in reversed(paginas):
            pag_id = pag["pag_id"]
            st.markdown(f"### Plancha #{pag_id} — *{pag.get('escena', '')}*")
            st.info(pag.get("guion_viñetas", ""))
            
            col_img, col_det = st.columns([1, 1])
            with col_img:
                st.image(pag.get("imagen_url"), use_container_width=True)
            with col_det:
                st.write("**Notas y Correcciones:**")
                for corr in pag.get("correcciones", []):
                    st.write(f"- {corr['nota']}")
                nota_txt = st.text_input(f"Añadir nota a plancha #{pag_id}:", key=f"nota_m_{pag_id}")
                if st.button(f"Guardar nota #{pag_id}", key=f"btn_m_{pag_id}"):
                    if nota_txt:
                        colmena.guardar_correccion_manga(pag_id, nota_txt)
                        st.rerun()
                if st.button(f"🗑️ Eliminar Plancha #{pag_id}", key=f"del_manga_{pag_id}"):
                    colmena.eliminar_plancha_manga(pag_id)
                    st.rerun()
            st.divider()
    else:
        st.info("No hay planchas de manga generadas todavía.")

# --- PESTAÑA 6: CONEXIÓN WATTPAD ---
with tab_wattpad:
    st.header("🔗 Conexión con Wattpad")
    url_wattpad = st.text_input("Pega el enlace público de Wattpad para extraer el lore:")
    if st.button("Asimilar Lore"):
        if url_wattpad:
            res = colmena.asimilar_historia_wattpad(url_wattpad)
            st.success("¡Lore asimilado con éxito!")
            st.text_area("Resultado:", res, height=150)

# --- PESTAÑA 7: CONFIGURACIÓN Y CREDENCIALES ESPECÍFICAS ---
with tab_config:
    st.header("⚙️ Configuración y Credenciales por Plataforma")
    st.write("Introduce los campos específicos que te solicita cada plataforma para dejar configurada la automatización.")
    
    servicio_elegido = st.selectbox(
        "Selecciona la plataforma a configurar:",
        ["TikTok API", "Instagram / Meta Graph API", "Twitter (X) API", "Google AI Studio (Gemini API)", "Wattpad API / Token"]
    )
    
    st.markdown("---")
    
    # Formulario dinámico según la plataforma seleccionada
    if servicio_elegido == "TikTok API":
        with st.form("form_cred_tiktok"):
            st.subheader("🔑 Credenciales de TikTok for Developers")
            c_key = st.text_input("Client Key:", value="awno6fxfgoe4q4gw")
            c_secret = st.text_input("Client Secret:", type="password")
            
            if st.form_submit_button("💾 Guardar Credenciales de TikTok"):
                if c_key and c_secret:
                    colmena.guardar_credencial_especifica("TikTok API", {"client_key": c_key, "client_secret": c_secret})
                    st.success("¡Credenciales de TikTok guardadas correctamente!")
                    st.rerun()
                else:
                    st.warning("Rellena ambos campos.")
                    
    elif servicio_elegido == "Instagram / Meta Graph API":
        with st.form("form_cred_meta"):
            st.subheader("🔑 Credenciales de Meta (Instagram Graph)")
            app_id = st.text_input("Meta App ID:")
            app_secret = st.text_input("Meta App Secret:", type="password")
            access_token = st.text_input("Long-Lived Access Token:", type="password")
            
            if st.form_submit_button("💾 Guardar Credenciales de Meta"):
                if app_id and access_token:
                    colmena.guardar_credencial_especifica("Instagram / Meta Graph API", {"app_id": app_id, "app_secret": app_secret, "access_token": access_token})
                    st.success("¡Credenciales de Meta/Instagram guardadas correctamente!")
                    st.rerun()
                else:
                    st.warning("Rellena al menos el App ID y el Access Token.")
                    
    elif servicio_elegido == "Twitter (X) API":
        with st.form("form_cred_twitter"):
            st.subheader("🔑 Credenciales de Twitter / X Developer")
            api_key = st.text_input("API Key (Consumer Key):")
            api_secret = st.text_input("API Secret (Consumer Secret):", type="password")
            bearer_token = st.text_input("Bearer Token:", type="password")
            
            if st.form_submit_button("💾 Guardar Credenciales de Twitter"):
                if api_key and bearer_token:
                    colmena.guardar_credencial_especifica("Twitter (X) API", {"api_key": api_key, "api_secret": api_secret, "bearer_token": bearer_token})
                    st.success("¡Credenciales de Twitter guardadas correctamente!")
                    st.rerun()
                else:
                    st.warning("Rellena los campos obligatorios.")
                    
    else:
        with st.form("form_cred_general"):
            st.subheader(f"🔑 Credencial para {servicio_elegido}")
            token_unico = st.text_input("Introduce el Token o Clave API:", type="password")
            
            if st.form_submit_button(f"💾 Guardar Credencial de {servicio_elegido}"):
                if token_unico:
                    colmena.guardar_credencial_especifica(servicio_elegido, {"token": token_unico})
                    st.success(f"¡Credencial para '{servicio_elegido}' guardada correctamente!")
                    st.rerun()
                else:
                    st.warning("Introduce un valor válido.")

    st.markdown("---")
    st.subheader("🛡️ Estado Actual de las Credenciales Registradas")
    credenciales_guardadas = getattr(colmena, "credenciales", {})
    if credenciales_guardadas:
        for serv, info in credenciales_guardadas.items():
            st.markdown(f"* **{serv}**: `Configurado y Guardado`")
    else:
        st.info("No hay credenciales configuradas todavía.")