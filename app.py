import streamlit as st
from motor_diario import ColmenaBufferInfinito, HermesVulcanoPostPublicacion

# Configuración de la página
st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Centro de Mando 24/7",
    page_icon="👑",
    layout="wide"
)

# Inicializar el estado de la sesión conectado al motor diario y persistencia
if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

if "hermes_vulcano" not in st.session_state:
    st.session_state.hermes_vulcano = HermesVulcanoPostPublicacion()

colmena = st.session_state.colmena_buffer
hermes = st.session_state.hermes_vulcano

# Título Principal
st.title("👑 Centro de Mando 24/7 - Saga: Los Cinco Reinos")

# Pestañas de navegación de la aplicación
tab_redes, tab_manga, tab_produccion, tab_agentes, tab_config = st.tabs([
    "📢 Redes Sociales", 
    "🎨 Visor y Mangaka (Hércules)", 
    "⚡ Motor de Producción (Aura)", 
    "🐝 Colmena y Métricas", 
    "⚙️ Configuración"
])

# --- PESTAÑA 1: REDES SOCIALES ---
with tab_redes:
    st.header("Gestión y Automatización de Redes Sociales")
    st.write("Administra el contenido programado generado por la colmena para difundir la saga.")
    
    banco = getattr(colmena, "banco_contenido_semanal", [])
    
    if banco:
        for idx, item in enumerate(banco):
            st.markdown(f"**Item #{item.get('id', idx+1)}** — *{item.get('timestamp', '')}*")
            st.write(f"**Texto:** {item.get('texto', '')}")
            st.write(f"**Copy Comercial:** {item.get('copy_comercial', '')}")
            st.write(f"**Hashtags:** {item.get('hashtags', '')}")
            
            estado = item.get('estado', 'Pendiente')
            st.write(f"Estado actual: `{estado}`")
            
            if "Pendiente" in estado:
                if st.button(f"🚀 Aprobar y Enviar a Redes #{item.get('id', idx+1)}", key=f"btn_redes_{idx}"):
                    item['estado'] = "Aprobado y Publicado"
                    colmena.sincronizar()
                    st.success(f"¡Item #{item.get('id', idx+1)} aprobado y difundido con éxito!")
                    st.rerun()
            st.divider()
    else:
        st.info("No hay elementos pendientes en el banco de contenido. Usa la pestaña 'Motor de Producción' para ordenar a Aura crear nuevos fragmentos.")

# --- PESTAÑA 2: VISOR Y MANGAKA (HÉRCULES) ---
with tab_manga:
    st.header("🎨 Visor y Estudiador de Planchas de Manga")
    st.write("Ordena a Hércules generar nuevas planchas visuales y revisa las páginas con sus respectivas correcciones.")
    
    # Formulario para ordenar una nueva plancha a Hércules
    with st.form("form_hercules"):
        st.subheader("✏️ Ordenar nueva plancha a Hércules")
        escena_input = st.text_input("Describe la escena para convertirla en plancha de manga:", "Hugo cayendo en sueño hacia las ruinas ancestrales...")
        btn_dibujar = st.form_submit_button("🎨 Ordenar a Hércules Dibujar Plancha")
        
        if btn_dibujar and escena_input:
            with st.spinner("Hércules está procesando los trazos y generando el arte..."):
                nueva_pag = colmena.hercules_modo_mangaka(escena_input)
                st.success(f"¡Plancha #{nueva_pag['pag_id']} generada y guardada con éxito!")
                st.rerun()

    st.markdown("---")
    st.subheader("📖 Planchas Registradas en el Sistema")
    
    paginas = getattr(colmena, "paginas_manga", [])
    if paginas:
        for pag in reversed(paginas):
            pag_id = pag["pag_id"]
            st.markdown(f"### Página #{pag_id} — Escena: *{pag['escena']}*")
            
            col_img, col_det = st.columns([1, 1])
            with col_img:
                # Muestra la imagen dinámica única correspondiente a esta página
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
                nota_texto = st.text_input(f"Añadir corrección para la Página #{pag_id}:", key=nota_key)
                if st.button(f"💾 Guardar Nota en Página #{pag_id}", key=f"btn_nota_{pag_id}"):
                    if nota_texto:
                        colmena.guardar_correccion_manga(pag_id, nota_texto)
                        st.success("¡Nota de corrección guardada para siempre!")
                        st.rerun()
            st.divider()
    else:
        st.info("Todavía no hay planchas de manga creadas. Usa el formulario superior para que Hércules empiece a dibujar.")

# --- PESTAÑA 3: MOTOR DE PRODUCCIÓN (AURA) ---
with tab_produccion:
    st.header("⚡ Motor de Producción Continua (Aura)")
    st.write("Indica instrucciones a Aura para que redacte contenido, analice lore y alimente el banco automáticamente.")
    
    with st.form("form_aura"):
        instruccion = st.text_area("Instrucción o directriz para Aura:", "Redacta el extracto inicial del encuentro en el reino prohibido...")
        btn_aura = st.form_submit_button("🧠 Ordenar a Aura Redactar y Enviar al Banco")
        
        if btn_aura and instruccion:
            with st.spinner("Aura está redactando y procesando el contenido..."):
                colmena.ciclo_produccion_continua(instruccion)
                st.success("¡Contenido redactado por Aura y añadido al banco con éxito!")
                st.rerun()

# --- PESTAÑA 4: COLMENA Y MÉTRICAS ---
with tab_agentes:
    st.header("🐝 Estado en Vivo de la Colmena y Métricas Post-Publicación")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("### 🧠 Aura")
        st.markdown("**Rol:** Co-autora / Redacción")
        st.info("Estado: **Activa**\n\nAnalizando capítulos y redactando fragmentos narrativos.")
        
    with col_b:
        st.markdown("### 🎨 Hércules")
        st.markdown("**Rol:** Mangaka / Ilustrador")
        st.success(f"Estado: **Operativo**\n\nPlanchas activas en sistema: `{len(colmena.paginas_manga)}`")
        
    with col_c:
        st.markdown("### 📊 Hermes & Vulcano")
        st.markdown("**Rol:** Métricas y Comunidad")
        st.warning("Estado: **Monitoreando**\n\nControlando flujos de datos y respuestas.")

    st.markdown("---")
    st.subheader("📈 Panel de Métricas Actuales")
    metricas = hermes.actualizar_metricas()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Vistas Totales Estimadas", f"{metricas['vistas']:,}")
    m2.metric("Clicks hacia Amazon / Letrame", f"{metricas['clicks_amazon']}")
    m3.metric("Nivel de Engagement", metricas['engagement'])

# --- PESTAÑA 5: CONFIGURACIÓN ---
with tab_config:
    st.header("⚙️ Configuración del Sistema 24/7")
    st.json({
        "Estado del Motor": "Activo con Persistencia JSON",
        "Modo de Operación": "Cloud 24/7",
        "Archivo de Datos": "datos_saga.json",
        "Motor Base": "motor_diario.py"
    })