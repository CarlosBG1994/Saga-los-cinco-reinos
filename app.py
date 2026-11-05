import streamlit as st
from motor_diario import ColmenaBufferInfinito

# Configuración de la página
st.set_page_config(
    page_title="Saga: Los Cinco Reinos - Centro de Mando",
    page_icon="👑",
    layout="wide"
)

# Inicializar el estado de la sesión para el motor diario y la colmena
if "colmena_buffer" not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBuffer()

st.title("👑 Centro de Mando 24/7 - Saga: Los Cinco Reinos")
st.markdown("---")

# Pestañas principales del centro de mando
tab_redes, tab_manga, tab_config = st.tabs(["📢 Redes Sociales", "🎨 Visor de Manga", "⚙️ Configuración"])

with tab_redes:
    st.subheader("📢 Gestión y Automatización de Redes Sociales")
    st.write("Administra el contenido programado para difundir la saga.")

    # Mostrar elementos pendientes o simulados de redes
    if not hasattr(st.session_state.colmena_buffer, "items_redes"):
        st.session_state.colmena_buffer.items_redes = [
            {"id": 1, "texto": "¡El despertar de los cinco reinos se acerca! Descubre el adelanto exclusivo.", "estado": "Pendiente"}
        ]

    for item in st.session_state.colmena_buffer.items_redes:
        st.markdown(f"**Item #{item['id']}**: {item['texto']}")
        st.write(f"Estado actual: `{item['estado']}`")
        if st.button(f"🚀 Aprobar y Enviar a Redes #{item['id']}", key=f"env_{item['id']}"):
            item['estado'] = "Publicado / Programado"
            st.session_state.colmena_buffer.sincronizar()
            st.success(f"¡Contenido #{item['id']} actualizado y guardado!")

with tab_manga:
    st.subheader("📖 Visor y Editor del Manga de la Saga")
    st.write("Revisa las planchas de Hércules y déjale notas de corrección guardadas para siempre.")

    escena_manga = st.text_input("Indica a Hércules la escena a convertir en Manga:", "El despertar del soberano en las ruinas")
    if st.button("✏️ Ordenar a Hércules Dibujar Plancha"):
        st.session_state.colmena_buffer.hercules_modo_mangaka(escena_manga)
        st.success("¡Página generada y guardada en el visor!")

    st.markdown("---")
    st.markdown("### 📚 Planchas Actuales del Manga")

    if not st.session_state.colmena_buffer.paginas_manga:
        st.info("Todavía no hay páginas de manga generadas.")
    else:
        for pag in st.session_state.colmena_buffer.paginas_manga:
            st.markdown(f"#### Página #{pag['pag_id']} – Escena: *{pag['escena']}*")
            st.image(pag['imagen_url'], caption=f"Página #{pag['pag_id']}")

with tab_config:
    st.subheader("⚙️ Configuración del Sistema 24/7")
    st.write("Parámetros de conexión y estado de los agentes de la colmena.")
    st.json({
        "Estado del Motor": "Activo",
        "Modo de Operación": "Cloud 24/7",
        "Persistencia": "datos_saga.json"
    })