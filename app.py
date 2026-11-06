import streamlit as st
from motor_diario import ColmenaBufferInfinito

st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Centro de Mando 24/7",
    page_icon="👑",
    layout="wide"
)

st.markdown(
    """
    <meta http-equiv="refresh" content="15">
    """,
    unsafe_allow_html=True
)

if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

colmena = st.session_state.colmena_buffer

st.title("👑 Centro de Mando 24/7 - Saga: Los Cinco Reinos")
st.info("🔄 *El sistema se actualiza automáticamente cada 15 segundos para mostrar el trabajo en segundo plano de los agentes.*")

# Pestañas principales (6 secciones completas)
tab_redes, tab_manga, tab_capitulos, tab_wattpad, tab_agentes, tab_config = st.tabs([
    "📢 Redes Sociales", 
    "🎨 Visor de Manga (Hércules)", 
    "📖 Los 25 Capítulos", 
    "🔗 Conexión Wattpad (Aura)",
    "🐝 Colmena y Estado en Vivo", 
    "⚙️ Configuración"
])

# --- PESTAÑA 1: REDES SOCIALES ---
with tab_redes:
    st.header("Gestión y Automatización de Redes Sociales (Aura & Cronos)")
    st.write("Administra el contenido programado de forma autónoma por la colmena para difundir la saga.")
    
    banco = getattr(colmena, "banco_contenido_semanal", [])
    
    if banco:
        for item in reversed(banco):
            item_id = item.get('id', 1)
            st.markdown(f"**Item #{item_id}** — *{item.get('timestamp', '')}*")
            st.write(f"**Texto:** {item.get('texto', '')}")
            st.write(f"**Copy Comercial:** {item.get('copy_comercial', '')}")
            st.write(f"**Hashtags:** {item.get('hashtags', '')}")
            
            estado = item.get('estado', 'Pendiente')
            st.write(f"Estado actual: `{estado}`")
            
            if "Pendiente" in estado:
                if st.button(f"🚀 Aprobar y Enviar a Redes #{item_id}", key=f"btn_redes_{item_id}"):
                    item['estado'] = "Aprobado y Publicado"
                    colmena.sincronizar()
                    st.success(f"¡Item #{item_id} aprobado y difundido con éxito!")
                    st.rerun()
            st.divider()
    else:
        st.warning("Esperando a que Aura genere contenido automáticamente en el buffer...")

# --- PESTAÑA 2: VISOR DE MANGA (HÉRCULES) ---
with tab_manga:
    st.header("🎨 Visor y Estudiador de Planchas de Manga (Hércules)")
    st.write("Revisa las planchas e ilustraciones generadas automáticamente por Hércules y déjale notas de corrección.")
    
    paginas = getattr(colmena, "paginas_manga", [])
    
    if paginas:
        for pag in reversed(paginas):
            pag_id = pag["pag_id"]
            st.markdown(f"### Plancha #{pag_id} — Escena: *{pag.get('escena', '')}*")
            
            col_img, col_det = st.columns([1, 1])
            with col_img:
                st.image(
                    pag.get("imagen_url", "https://picsum.photos/600/400"), 
                    caption=f"Plancha Oficial - Página #{pag_id}",
                    use_container_width=True
                )
            
            with col_det:
                st.write("**Notas y Correcciones Guardadas:**")
                correcciones = pag.get("correcciones", [])
                if correcciones:
                    for corr in correcciones:
                        st.info(f"[{corr['fecha']}] {corr['nota']}")
                else:
                    st.write("_Sin correcciones registradas todavía._")
                
                nota_key = f"nota_input_{pag_id}"
                nota_texto = st.text_input(f"Añadir corrección para la Plancha #{pag_id}:", key=nota_key)
                if st.button(f"💾 Guardar Nota en Plancha #{pag_id}", key=f"btn_nota_{pag_id}"):
                    if nota_texto:
                        colmena.guardar_correccion_manga(pag_id, nota_texto)
                        st.success("¡Nota de corrección guardada para siempre!")
                        st.rerun()
            st.divider()
    else:
        st.warning("Hércules está preparando las planchas visuales en segundo plano...")

# --- PESTAÑA 3: LOS CAPÍTULOS ---
with tab_capitulos:
    st.header("📖 Explorador de Capítulos de la Saga")
    st.write("Consulta el contenido de los capítulos subidos directamente en la raíz de tu repositorio (del 0 al 25).")
    
    num_cap = st.selectbox(
        "Selecciona el Capítulo a consultar:",
        options=list(range(0, 26)),
        format_func=lambda x: f"Capítulo {x}"
    )
    
    info_cap = colmena.obtener_capitulo(num_cap)
    
    st.markdown(f"### 👑 {info_cap['titulo']}")
    st.markdown(f"**Escena Principal:** *{info_cap['escena']}*")
    st.text_area("Contenido del Capítulo:", info_cap["descripcion"], height=300)
    st.markdown(f"**Estado del Arte:** `{info_cap['plancha_generada']}`")

# --- PESTAÑA 4: CONEXIÓN WATTPAD (AURA) ---
with tab_wattpad:
    st.header("🔗 Conexión con Wattpad y Segunda Parte (Aura)")
    st.write("Permite a Aura leer tus novelas desde Wattpad para asimilar el universo y ayudarte a escribir la segunda parte.")
    
    url_wattpad = st.text_input("Pega el enlace público de tu historia o capítulo en Wattpad:")
    if st.button("🔗 Ordenar a Aura leer Wattpad y estructurar la 2ª Parte"):
        if url_wattpad:
            with st.spinner("Aura está accediendo a Wattpad y asimilando el universo de tu obra..."):
                resultado = colmena.asimilar_historia_wattpad(url_wattpad)
                st.success("¡Lore asimilado con éxito por Aura!")
                st.text_area("Fragmento asimilado:", resultado, height=200)
        else:
            st.warning("Por favor, introduce una URL válida.")
            
    if getattr(colmena, "lore_wattpad", ""):
        st.markdown("---")
        st.subheader("📚 Lore Actual Asimilado de Wattpad")
        st.text_area("Base de conocimiento activa:", colmena.lore_wattpad, height=150, disabled=True)

# --- PESTAÑA 5: COLMENA Y ESTADO EN VIVO ---
with tab_agentes:
    st.header("🐝 Estado en Vivo de la Colmena Autónoma")
    st.write("Supervisa el rendimiento y las tareas ejecutadas en segundo plano por los agentes.")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("### 🧠 Aura")
        st.markdown("**Rol:** Co-autora / Redacción")
        st.info("Estado: **Activa 24/7**\n\nGenerando fragmentos narrativos y procesando Wattpad.")
        
    with col_b:
        st.markdown("### 🎨 Hércules")
        st.markdown("**Rol:** Mangaka / Ilustrador")
        st.success(f"Estado: **Operativo 24/7**\n\nPlanchas activas en sistema: `{len(colmena.paginas_manga)}`")
        
    with col_c:
        st.markdown("### ⏳ Cronos")
        st.markdown("**Rol:** Automatización / Redes")
        st.warning("Estado: **Monitoreando**\n\nControlando colas de publicaciones y persistencia.")

    st.markdown("---")
    st.subheader("📊 Métricas Generales del Sistema")
    m1, m2, m3 = st.columns(3)
    m1.metric("Ítems de Contenido en Banco", len(colmena.banco_contenido_semanal))
    m2.metric("Planchas de Manga Creadas", len(colmena.paginas_manga))
    m3.metric("Capítulos Totales Indexados", "Del 0 al 25")

# --- PESTAÑA 6: CONFIGURACIÓN ---
with tab_config:
    st.header("⚙️ Configuración del Sistema 24/7")
    st.json({
        "Estado del Motor": "Activo con Persistencia en JSON",
        "Modo de Operación": "Autónomo 24/7 (Hilos en Segundo Plano)",
        "Archivo de Datos": "datos_saga.json",
        "Capítulos Soportados": "Del 0 al 25 en la raíz",
        "Motor Base": "motor_diario.py"
    })