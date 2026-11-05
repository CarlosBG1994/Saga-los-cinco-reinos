import streamlit as st
from motor_diario import ColmenaBufferInfinito

# Configuración de la página
st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Centro de Mando 24/7",
    page_icon="👑",
    layout="wide"
)

# Recarga automática de la página cada 15 segundos para ver el trabajo en vivo de los agentes
st.markdown(
    """
    <meta http-equiv="refresh" content="15">
    """,
    unsafe_allow_html=True
)

# Inicializar la colmena en el estado de la sesión
if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

colmena = st.session_state.colmena_buffer

st.title("👑 Centro de Mando 24/7 - Saga: Los Cinco Reinos")
st.info("🔄 *El sistema se actualiza automáticamente cada 15 segundos para mostrar el trabajo en segundo plano de los agentes.*")

# Pestañas principales de navegación
tab_redes, tab_manga, tab_capitulos, tab_agentes, tab_config = st.tabs([
    "📢 Redes Sociales", 
    "🎨 Visor de Manga (Hércules)", 
    "📖 Los 25 Capítulos", 
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
                # Muestra la imagen generada automáticamente
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
                
                # Input para añadir nueva nota a esta página específica
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

# --- PESTAÑA 3: LOS 25 CAPÍTULOS DE LA SAGA ---
with tab_capitulos:
    st.header("📖 Explorador de los 25 Capítulos de la Saga")
    st.write("Consulta la estructura, lore y metadatos oficiales de los 25 capítulos que componen la obra.")
    
    # Selector de capítulos del 1 al 25
    num_cap = st.selectbox(
        "Selecciona el Capítulo a consultar:",
        options=list(range(1, 26)),
        format_func=lambda x: f"Capítulo {x} de 25"
    )
    
    info_cap = colmena.obtener_capitulo(num_cap)
    
    st.markdown(f"### 👑 {info_cap['titulo']}")
    st.markdown(f"**Escena Principal:** *{info_cap['escena']}*")
    st.info(info_cap["descripcion"])
    st.markdown(f"**Estado del Arte:** `{info_cap['plancha_generada']}`")

# --- PESTAÑA 4: COLMENA Y ESTADO EN VIVO ---
with tab_agentes:
    st.header("🐝 Estado en Vivo de la Colmena Autónoma")
    st.write("Supervisa el rendimiento y las tareas ejecutadas en segundo plano por los agentes.")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("### 🧠 Aura")
        st.markdown("**Rol:** Co-autora / Redacción")
        st.info("Estado: **Activa 24/7**\n\nGenerando fragmentos narrativos y textos comerciales automáticamente.")
        
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
    m3.metric("Capítulos Totales Indexados", "25 Capítulos")

# --- PESTAÑA 5: CONFIGURACIÓN ---
with tab_config:
    st.header("⚙️ Configuración del Sistema 24/7")
    st.json({
        "Estado del Motor": "Activo con Persistencia en JSON",
        "Modo de Operación": "Autónomo 24/7 (Hilos en Segundo Plano)",
        "Archivo de Datos": "datos_saga.json",
        "Capítulos Totales": "25 Capítulos",
        "Motor Base": "motor_diario.py"
    })