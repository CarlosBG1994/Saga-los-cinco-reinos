import streamlit as st
from motor_diario import ColmenaBufferInfinito, HermesVulcanoPostPublicacion

st.set_page_config(page_title="Centro de Mando - Saga: Los Cinco Reinos", layout="wide", page_icon="👑")

if 'colmena_buffer' not in st.session_state:
    st.session_state.colmena_buffer = ColmenaBufferInfinito()
if 'hermes_vulcano' not in st.session_state:
    st.session_state.hermes_vulcano = HermesVulcanoPostPublicacion()

st.title("👑 Centro de Mando: Saga: Los Cinco Reinos (Modo Persistente 24/7)")
st.markdown("Tus datos se guardan automáticamente en la nube. Accede desde cualquier dispositivo sin perder nada.")

# Pestañas del panel
tab_war, tab_banco, tab_manga, tab_redes, tab_comentarios, tab_config = st.tabs([
    "🖥️ War Room (Buffer en Vivo)", 
    "📦 Banco de Contenidos", 
    "📖 Visor de Manga (Hércules)", 
    "📅 Frecuencias y Redes", 
    "💬 Comentarios & Métricas",
    "⚙️ Configuración"
])

with tab_war:
    st.subheader("Estado de Producción Continua (Buffer Infinito)")
    st.info("💡 Todo lo que generes aquí quedará grabado de forma permanente en el sistema.")
    
    instruccion_libre = st.text_input("Directriz para que Aura y Hércules alimenten el buffer:", "Escena de la batalla en el puente colgante...")
    if st.button("⚡ Forzar Ciclo de Creación para el Buffer"):
        with st.spinner("Generando contenido y guardando en la nube..."):
            st.session_state.colmena_buffer.ciclo_produccion_continua(instruccion_libre)
        st.success("¡Contenido creado y guardado permanentemente en el banco!")

with tab_banco:
    st.subheader("📦 Banco de Contenidos Listos")
    st.write("Material acumulado por los agentes listo para enviar a redes o plataformas.")
    
    if not st.session_state.colmena_buffer.banco_contenido_semanal:
        st.warning("El banco está vacío. Genera contenido desde el War Room.")
    else:
        for item in st.session_state.colmena_buffer.banco_contenido_semanal:
            with st.expander(f"Contenido #{item['id']} ({item['timestamp']}) - Estado: {item['estado']}"):
                st.write(f"**Texto / Lore:** {item['texto']}")
                st.write(f"**Copy Comercial:** {item['copy_comercial']} *(Amazon & Letrame)*")
                st.write(f"**Hashtags:** {item['hashtags']}")
                
                if st.button(f"🚀 Aprobar y Enviar a Redes #{item['id']}", key=f"env_{item['id']}"):
                    item['estado'] = "Publicado / Programado"
                    st.session_state.colmena_buffer.sincronizar()
                    st.success(f"¡Contenido #{item['id']} actualizado y guardado!")

with tab_manga:
    st.subheader("📖 Visor y Editor del Manga de la Saga")
    st.write("Revisa las planchas de Hércules y déjale notas de corrección guardadas para siempre.")
    
    escena_manga = st.text_input("Indica a Hércules la escena a convertir en Manga:", "El despertar del soberano en las ruinas...")
if st.button("✏️ Ordenar a Hércules Dibujar Plancha"):
    st.session_state.colmena_buffer.hercules_modo_mangaka(escena_manga)
    st.success("¡Página generada y guardada en el visor!")

    st.markdown("---")
    st.markdown("### 📚 Planchas Actuales del Manga")
    
    if not st.session_state.colmena_buffer.paginas_manga:
        st.info("Todavía no hay páginas de manga generadas.")
    else:
        for pag in st.session_state.colmena_buffer.paginas_manga:
            st.markdown(f"#### Página #{pag['pag_id']} — Escena: *{pag['escena']}*")
            st.image(pag['imagen_url'], caption=f"Página #{pag['pag_id']}")
            
            # Mostrar historial de correcciones guardadas
            if pag['correcciones']:
                st.markdown("**📝 Historial de correcciones enviadas:**")
                for corr in pag['correcciones']:
                    st.text(f"- [{corr['fecha']}] {corr['nota']}")
            
            feedback_usuario = st.text_input(f"Indicar cambios para la Página #{pag['pag_id']}:", key=f"feed_{pag['pag_id']}")
            if st.button(f"Enviar corrección a Hércules (Pág #{pag['pag_id']})", key=f"btn_{pag['pag_id']}"):
                if feedback_usuario:
                    st.session_state.colmena_buffer.guardar_correccion_manga(pag['pag_id'], feedback_usuario)
                    st.success(f"¡Corrección guardada para la página #{pag['pag_id']}!")
                else:
                    st.warning("Escribe una nota antes de enviar.")

with tab_redes:
    st.subheader("📅 Programador de Frecuencias")
    st.selectbox("Ritmo de extracción del Banco", ["1 vez al día", "2 veces al día", "Solo aprobación manual (Recomendado)"], index=2)
    st.markdown("### 🌐 Redes Soportadas")
    st.checkbox("TikTok (Activo)", value=True)
    st.checkbox("Wattpad (Activo)", value=True)
    st.checkbox("Instagram / Reels", value=False)

with tab_comentarios:
    st.subheader("💬 Módulo Post-Publicación: Hermes & Vulcano")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📊 Actualizar Métricas (Hermes)"):
            stats = st.session_state.hermes_vulcano.actualizar_metricas()
            st.metric("Vistas Totales", stats["vistas"])
            st.metric("Clics en Amazon/Letrame", stats["clicks_amazon"])
    with c2:
        if st.button("💬 Responder Comentarios (Vulcano)"):
            st.success(st.session_state.hermes_vulcano.gestionar_comentarios())

with tab_config:
    st.subheader("⚙️ Configuración y Credenciales")
    st.text_input("Token API TikTok", type="password")
    st.text_input("Credenciales Wattpad", value="saga.loscincoreinos@gmail.com")
    st.text_input("Enlace Amazon", value="https://amazon.es/...")
    st.text_input("Enlace Letrame", value="https://letrame.com/...")
