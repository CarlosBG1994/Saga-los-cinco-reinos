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
st.info("💡 *Modo Coherente Estricto: Los agentes operan exclusivamente bajo tus directrices directas analizando tus capítulos reales.*")

tab_capitulos, tab_asistencia, tab_redes, tab_manga, tab_wattpad, tab_config = st.tabs([
    "📖 Capítulos y Órdenes",
    "❓ Buzón de Dudas (Ayuda)",
    "📢 Contenido y Redes",
    "🎨 Visor de Manga",
    "🔗 Conexión Wattpad",
    "⚙️ Configuración"
])

# --- PESTAÑA 1: CAPÍTULOS Y ÓRDENES ---
with tab_capitulos:
    st.header("📖 Explorador de Capítulos y Creación Guiada")
    st.write("Selecciona un capítulo real de tu repositorio para que Aura o Hércules trabajen estrictamente sobre él.")
    
    num_cap = st.selectbox(
        "Selecciona el Capítulo:",
        options=list(range(0, 26)),
        format_func=lambda x: f"Capítulo {x}"
    )
    
    info_cap = colmena.obtener_capitulo(num_cap)
    st.markdown(f"### 👑 {info_cap['titulo']}")
    st.text_area("Contenido real detectado en la raíz:", info_cap["descripcion"], height=250)
    
    st.markdown("---")
    st.subheader("🛠️ Dar orden estricta a los agentes sobre este capítulo:")
    instruccion_user = st.text_input("¿Qué quieres que Aura redacte o continúe basándose en este capítulo?")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✍️ Ordenar a Aura redactar texto coherente"):
            if instruccion_user:
                colmena.generar_contenido_manual(instruccion_user, num_cap)
                st.success("¡Borrador coherente generado y añadido a la pestaña de Contenido!")
                st.rerun()
            else:
                st.warning("Escribe una directriz clara para Aura.")
                
    with col_btn2:
        if st.button("🎨 Ordenar a Hércules crear plancha de este capítulo"):
            colmena.generar_manga_manual(num_cap)
            st.success("¡Plancha de manga estructurada y añadida al Visor!")
            st.rerun()

# --- PESTAÑA 2: BUZÓN DE DUDAS ---
with tab_asistencia:
    st.header("❓ Buzón de Dudas y Asistencia de la Colmena")
    st.write("Si los agentes necesitan aclaraciones sobre la trama, te consultarán aquí para no inventar nada.")
    
    nueva_duda = st.text_input("Plantear una duda o regla de coherencia a los agentes:")
    agente_destino = st.selectbox("¿A qué agente va dirigida?", ["Aura (Co-autora)", "Hércules (Mangaka)"])
    if st.button("Enviar consulta a la colmena"):
        if nueva_duda:
            colmena.registrar_duda(nueva_duda, agente_destino)
            st.success("¡Consulta registrada!")
            st.rerun()
            
    st.markdown("---")
    st.subheader("📋 Historial de Dudas y Respuestas")
    dudas = getattr(colmena, "dudas_agentes", [])
    if dudas:
        for d in reversed(dudas):
            st.markdown(f"**[{d['timestamp']}] Para {d['agente']}**: {d['pregunta']}")
            if d["respondida"]:
                st.success(f"**Tu respuesta (Directriz activa):** {d['respuesta']}")
            else:
                resp_key = f"resp_{d['id']}"
                resp_txt = st.text_input(f"Aclarar duda #{d['id']}:", key=resp_key)
                if st.button(f"Guardar aclaración #{d['id']}", key=f"btn_duda_{d['id']}"):
                    if resp_txt:
                        colmena.responder_duda(d['id'], resp_txt)
                        st.success("¡Directriz guardada con éxito!")
                        st.rerun()
            st.divider()
    else:
        st.info("No hay dudas registradas. Todo marcha bajo tus órdenes directas.")

# --- PESTAÑA 3: CONTENIDO Y REDES (Con borrado) ---
with tab_redes:
    st.header("📢 Contenido Generado (Control de Borrado)")
    st.write("Revisa los textos generados. Puedes borrarlos si no te convencen.")
    
    banco = getattr(colmena, "banco_contenido_semanal", [])
    if banco:
        for item in reversed(banco):
            item_id = item.get('id', 1)
            st.markdown(f"**Item #{item_id}** (Capítulo asociado: {item.get('cap_asociado', 'N/A')}) — *{item.get('timestamp', '')}*")
            st.text_area(f"Texto #{item_id}", item.get('texto', ''), height=100, key=f"txt_{item_id}")
            
            if st.button(f"🗑️ Eliminar Item #{item_id}", key=f"del_item_{item_id}"):
                colmena.eliminar_item_banco(item_id)
                st.warning(f"Item #{item_id} eliminado correctamente.")
                st.rerun()
            st.divider()
    else:
        st.info("No hay contenido generado en este momento.")

# --- PESTAÑA 4: VISOR DE MANGA (Con borrado) ---
with tab_manga:
    st.header("🎨 Visor de Planchas de Manga (Control de Borrado)")
    st.write("Revisa los guiones estructurados por Hércules basados en tus capítulos.")
    
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
                    st.warning("Plancha eliminada del sistema.")
                    st.rerun()
            st.divider()
    else:
        st.info("No hay planchas de manga generadas todavía.")

# --- PESTAÑA 5: CONEXIÓN WATTPAD ---
with tab_wattpad:
    st.header("🔗 Conexión con Wattpad")
    url_wattpad = st.text_input("Pega el enlace público de Wattpad para extraer el lore:")
    if st.button("Asimilar Lore"):
        if url_wattpad:
            res = colmena.asimilar_historia_wattpad(url_wattpad)
            st.success("¡Lore asimilado con éxito!")
            st.text_area("Resultado:", res, height=150)

# --- PESTAÑA 6: CONFIGURACIÓN ---
with tab_config:
    st.header("⚙️ Configuración del Sistema")
    st.json({"Modo": "Control Estricto y Manual", "Capítulos Soportados": "Del 0 al 25 en la raíz"})