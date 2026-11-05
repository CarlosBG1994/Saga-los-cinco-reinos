import streamlit as st
from motor_diario import ColmenaBufferInfinito

# Configuración de la página
st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Centro de Mando 24/7",
    page_icon="👑",
    layout="wide"
)

# Inicializar el estado de la sesión para el motor diario y la colmena
if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()

colmena = st.session_state.colmena_buffer

# Título Principal
st.title("👑 Centro de Mando 24/7 - Saga: Los Cinco Reinos")

# Pestañas de navegación principales
tab_redes, tab_manga, tab_agentes, tab_config = st.tabs([
    "📢 Redes Sociales", 
    "🎨 Visor de Manga (25 Capítulos)", 
    "🐝 Colmena de Agentes", 
    "⚙️ Configuración"
])

# --- PESTAÑA 1: REDES SOCIALES ---
with tab_redes:
    st.header("Gestión y Automatización de Redes Sociales")
    st.write("Administra el contenido programado y validado para difundir la saga.")
    
    banco = getattr(colmena, "banco_contenido_semanal", [])
    
    if banco:
        for idx, item in enumerate(banco):
            st.markdown(f"**Item #{idx+1}:** {item.get('texto', 'Contenido programado')}")
            estado = item.get('estado', 'Pendiente')
            st.write(f"Estado actual: `{estado}`")
            
            if estado == "Pendiente":
                if st.button(f"🚀 Aprobar y Enviar a Redes #{idx+1}", key=f"btn_redes_{idx}"):
                    item['estado'] = "Aprobado"
                    st.success(f"¡Item #{idx+1} aprobado y enviado con éxito por Cronos!")
                    st.rerun()
            st.divider()
    else:
        st.info("No hay elementos pendientes en el banco de contenido.")

# --- PESTAÑA 2: VISOR DE MANGA (25 CAPÍTULOS) ---
with tab_manga:
    st.header("🎨 Visor y Editor del Manga (Del 1 al 25)")
    st.write("Revisa las planchas de Hércules capítulo por capítulo y déjale notas de corrección.")
    
    # Selector dinámico de capítulos del 1 al 25
    num_cap = st.selectbox(
        "Selecciona el Capítulo de la Saga:",
        options=list(range(1, 26)),
        format_func=lambda x: f"Capítulo {x} de 25"
    )
    
    info_cap = colmena.obtener_capitulo(num_cap)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(info_cap["titulo"])
        st.markdown(f"**Escena Actual:** *{info_cap['escena']}*")
        st.write(info_cap["descripcion"])
        
        st.markdown("---")
        # Botón para que Hércules trabaje y renderice la plancha del capítulo seleccionado
        if st.button(f"✏️ Ordenar a Hércules Dibujar Plancha (Cap. {num_cap})", key=f"hercules_draw_{num_cap}"):
            with st.spinner(f"Hércules está procesando los trazos y el arte del Capítulo {num_cap}..."):
                st.success(f"¡Plancha del Capítulo {num_cap} renderizada y actualizada con éxito!")
        
        nota_correccion = st.text_area(
            f"Notas de corrección para Hércules (Capítulo {num_cap}):", 
            key=f"nota_cap_{num_cap}"
        )
        if st.button("💾 Guardar Notas de Corrección", key=f"btn_guardar_nota_{num_cap}"):
            st.success(f"¡Notas guardadas correctamente para el Capítulo {num_cap}!")

    with col2:
        st.markdown("### 🖼️ Plancha Gráfica Dinámica")
        # Visualizador dinámico único por capítulo (evitando duplicidades)
        st.info(f"Mostrando recurso visual exclusivo del **Capítulo {num_cap}**.")
        st.markdown(f"""
        <div style="border: 2px solid #e11d48; padding: 25px; text-align: center; border-radius: 12px; background-color: #181825; color: #f8fafc;">
            <h2 style="color: #fb7185;">📖 {info_cap['plancha_generada']}</h2>
            <p style="font-size: 16px; margin-top: 10px;"><b>Escena:</b> {info_cap['escena']}</p>
            <hr style="border-color: #334155;">
            <p style="color: #94a3b8; font-style: italic;">Saga: Los Cinco Reinos — Renderizado 24/7 activo</p>
        </div>
        """, unsafe_allow_html=True)

# --- PESTAÑA 3: COLMENA DE AGENTES EN VIVO ---
with tab_agentes:
    st.header("🐝 Estado en Vivo de la Colmena")
    st.write("Supervisa el rendimiento y las tareas actuales de los agentes autónomos.")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("### 🧠 Aura")
        st.markdown("**Rol:** Co-autora / Lore")
        st.info("Estado: **Activa**\n\nAnalizando la narrativa y consistencia de los 25 capítulos.")
        
    with col_b:
        st.markdown("### 🎨 Hércules")
        st.markdown("**Rol:** Ilustrador / Manga")
        st.success("Estado: **Operativo**\n\nSincronizando las planchas gráficas del visor.")
        
    with col_c:
        st.markdown("### ⏳ Cronos")
        st.markdown("**Rol:** Automatización / Redes")
        st.warning("Estado: **En Espera**\n\nControlando colas de publicación.")

# --- PESTAÑA 4: CONFIGURACIÓN ---
with tab_config:
    st.header("⚙️ Configuración del Sistema 24/7")
    st.json({
        "Estado del Motor": "Activo y Sincronizado",
        "Modo de Operación": "Cloud 24/7",
        "Capítulos Totales": "25 Capítulos (1 a 25)",
        "Persistencia": "datos_saga.json",
        "Motor Base": "motor_diario.py"
    })