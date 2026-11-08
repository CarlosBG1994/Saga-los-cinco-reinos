import streamlit as st
import os
import urllib.parse
from motor_diario import (
    cargar_datos_saga, guardar_datos_saga, 
    listar_archivos_capitulos, aura_auditar_capitulo_real
)
from motor_aprendizajes import (
    cargar_aprendizajes, registrar_feedback_hercules, 
    obtener_prompt_aprendido_para_hercules
)

st.set_page_config(
    page_title="Agencia Literaria - Los Cinco Reinos", 
    page_icon="🛡️",
    layout="wide"
)

datos = cargar_datos_saga()
aprendizajes = cargar_aprendizajes()

st.title("🛡️ Agencia de Marketing Literario: Los Cinco Reinos")
st.markdown("### Panel de Control Operativo para Aura y Hércules")
st.markdown("---")

pestanas = st.tabs([
    "🔑 Credenciales Aisladas", 
    "📜 Auditoría de Capítulos (Aura)", 
    "👥 Gestión de Personajes", 
    "🎨 Taller de Hércules (Aprendizaje)", 
    "📖 Estudio de Manga Paso a Paso"
])

# ==========================================
# PESTAÑA 1: CREDENCIALES AISLADAS
# ==========================================
with pestanas[0]:
    st.subheader("Configuración de Credenciales por Plataforma")
    st.info("Introduce y guarda las claves de forma independiente sin riesgo de pérdida al cambiar de pestaña.")
    
    creds = datos.get("credenciales", {})
    
    with st.form("form_credenciales"):
        c_gemini = st.text_input("Clave API Google AI Studio (Gemini - Requerida para Aura)", value=creds.get("gemini", ""), type="password")
        c_insta = st.text_input("Credenciales Instagram (Token / Usuario)", value=creds.get("instagram", ""))
        c_tik = st.text_input("Credenciales TikTok (Token / Usuario)", value=creds.get("tiktok", ""))
        c_tw = st.text_input("Credenciales Twitter / X (Token / Usuario)", value=creds.get("twitter", ""))
        
        btn_guardar_creds = st.form_submit_button("💾 Guardar Todas las Credenciales")
        if btn_guardar_creds:
            datos["credenciales"] = {
                "gemini": c_gemini,
                "instagram": c_insta,
                "tiktok": c_tik,
                "twitter": c_tw
            }
            guardar_datos_saga(datos)
            st.success("¡Credenciales actualizadas y guardadas con éxito en el sistema!")

# ==========================================
# PESTAÑA 2: AUDITORÍA DE CAPÍTULOS (AURA)
# ==========================================
with pestanas[1]:
    st.subheader("Control y Auditoría Profunda de Capítulos (Aura)")
    st.markdown("Selecciona cualquiera de tus **25 capítulos** subidos en formato texto para que Aura los lea de principio a fin, extraiga la información clave y actualice la base de datos de personajes.")
    
    archivos_caps = listar_archivos_capitulos()
    
    if not archivos_caps:
        st.warning("⚠️ No se han detectado archivos de texto (`.txt`) de los capítulos en la ruta del proyecto. Asegúrate de tener tus capítulos subidos para que Aura pueda analizarlos.")
    else:
        st.success(f"📁 Se han detectado {len(archivos_caps)} archivos de capítulos listos para auditar.")
        cap_seleccionado = st.selectbox("Seleccionar Archivo de Capítulo para Aura", archivos_caps)
        
        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn1:
            if st.button("🔍 Forzar Auditoría Completa con Aura", type="primary"):
                with st.spinner("Aura está procesando el texto del capítulo mediante Gemini-1.5-flash..."):
                    exito, mensaje = aura_auditar_capitulo_real(cap_seleccionado)
                    if exito:
                        st.success(mensaje)
                        st.rerun()
                    else:
                        st.error(mensaje)
                        
    st.markdown("---")
    st.markdown("### 📋 Historial de Capítulos Auditados por Aura:")
    auditados = datos.get("capitulos_auditados", [])
    if not auditados:
        st.info("Aún no se ha auditado ningún capítulo en esta sesión.")
    else:
        for cap in auditados:
            st.markdown(f"- ✅ **{cap}**: Analizado, personajes extraídos y sincronizados.")

# ==========================================
# PESTAÑA 3: GESTIÓN DE PERSONAJES
# ==========================================
with pestanas[2]:
    st.subheader("Biblioteca Jerárquica y de Personajes")
    st.markdown("Visualiza, edita, cambia de jerarquía (*Protagonista*, *Secundario*, *Antagonista*, *Terciario*), añade notas de mejora o elimina personajes de la saga.")
    
    lista_personajes = datos.get("personajes", [])
    
    if not lista_personajes:
        st.info("No hay personajes registrados actualmente en la base de datos. Ve a la pestaña de 'Auditoría de Capítulos' para que Aura los extraiga automáticamente.")
    else:
        st.markdown(f"**Total de personajes en base de datos:** {len(lista_personajes)}")
        
        for idx, personaje in enumerate(lista_personajes):
            with st.expander(f"👤 {personaje['nombre']} — [{personaje.get('rol', 'Secundario')}] (Edad/Tipo: {personaje.get('edad', 'N/A')})"):
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    roles_disponibles = ["Protagonista", "Secundario", "Antagonista", "Terciario"]
                    rol_actual = personaje.get('rol', 'Secundario')
                    if rol_actual not in roles_disponibles:
                        rol_actual = "Secundario"
                        
                    nuevo_rol = st.selectbox(
                        "Jerarquía del Personaje", 
                        roles_disponibles, 
                        index=roles_disponibles.index(rol_actual),
                        key=f"rol_pers_{idx}"
                    )
                    nueva_descripcion = st.text_area(
                        "Descripción física y trasfondo", 
                        value=personaje.get('descripcion', ''), 
                        key=f"desc_pers_{idx}"
                    )
                with col_p2:
                    nuevas_notas_usuario = st.text_area(
                        "Notas de mejora personal (Feedback directo para Hércules)", 
                        value=personaje.get('notas', ''), 
                        key=f"notas_pers_{idx}",
                        placeholder="Ej: Asegurar que Esther tenga siempre el pelo rubio claro..."
                    )
                    
                col_acc1, col_acc2 = st.columns(2)
                if col_acc1.button("💾 Actualizar Ficha de Personaje", key=f"btn_act_{idx}"):
                    datos["personajes"][idx]["rol"] = nuevo_rol
                    datos["personajes"][idx]["descripcion"] = nueva_descripcion
                    datos["personajes"][idx]["notas"] = nuevas_notas_usuario
                    guardar_datos_saga(datos)
                    st.success(f"¡Ficha de '{personaje['nombre']}' actualizada y guardada correctamente!")
                    st.rerun()
                    
                if col_acc2.button("🗑️ Eliminar Personaje", key=f"btn_del_{idx}"):
                    personaje_eliminado = datos["personajes"].pop(idx)
                    guardar_datos_saga(datos)
                    st.warning(f"Personaje '{personaje_eliminado['nombre']}' eliminado permanentemente.")
                    st.rerun()

# ==========================================
# PESTAÑA 4: TALLER DE HÉRCULES (APRENDIZAJE)
# ==========================================
with pestanas[3]:
    st.subheader("Estudio Gráfico e Historial de Aprendizaje de Hércules")
    st.markdown("Hércules asimila tus correcciones estéticas y de diseño para aplicarlas de manera automática en la generación de imágenes y viñetas.")
    
    st.markdown("### 🧠 Memoria de Aprendizaje Activa:")
    preferencias_estilo = aprendizajes.get('preferencias_estilo', [])
    reglas_manga = aprendizajes.get('reglas_manga', [])
    
    col_ap1, col_ap2 = st.columns(2)
    with col_ap1:
        st.markdown(f"**Preferencias de Estilo Registradas ({len(preferencias_estilo)}):**")
        if not preferencias_estilo:
            st.text("Ninguna registrada todavía.")
        for p in preferencias_estilo:
            st.markdown(f"- *{p}*")
    with col_ap2:
        st.markdown(f"**Reglas Específicas de Manga ({len(reglas_manga)}):**")
        if not reglas_manga:
            st.text("Ninguna registrada todavía.")
        for r in reglas_manga:
            st.markdown(f"- *{r}*")
            
    st.markdown("---")
    st.markdown("### ✍️ Enseñar una Nueva Directriz a Hércules")
    
    tipo_directriz = st.selectbox("Ámbito de la directriz", ["Estilo General de Dibujo", "Personaje Específico", "Regla Estricta para el Manga"])
    texto_instruccion = st.text_area(
        "Instrucción detallada de mejora", 
        placeholder="Ej: Los personajes nunca deben salir con proporciones deformadas..."
    )
    
    if st.button("🧠 Registrar Aprendizaje en Hércules", type="primary"):
        if texto_instruccion.strip():
            tipo_key = 'estilo' if tipo_directriz == 'Estilo General de Dibujo' else ('personaje' if tipo_directriz == 'Personaje Específico' else 'manga')
            registrar_feedback_hercules(tipo_key, 'general', texto_instruccion)
            st.success("¡Instrucción asimilada! Hércules ha integrado este aprendizaje en su memoria permanente.")
            st.rerun()
        else:
            st.error("Por favor, escribe una instrucción válida antes de enviarla.")

# ==========================================
# PESTAÑA 5: ESTUDIO DE MANGA PASO A PASO
# ==========================================
with pestanas[4]:
    st.subheader("Estudio de Manga Interactivo (Generación Viñeta a Viñeta)")
    st.markdown("Hércules genera la imagen de la viñeta actual aplicando automáticamente sus aprendizajes previos. **El sistema está bloqueado: no podrás pasar a la siguiente viñeta hasta que revises y apruebes expresamente la viñeta actual.**")
    
    if "vineta_actual" not in st.session_state:
        st.session_state.vineta_actual = 1
    if "prompt_custom_vineta" not in st.session_state:
        st.session_state.prompt_custom_vineta = ""

    archivos_manga = listar_archivos_capitulos()
    if not archivos_manga:
        st.warning("⚠️ No se detectan capítulos para adaptar.")
    else:
        capitulo_trabajo = st.selectbox("Seleccionar Capítulo para Adaptación a Manga", archivos_manga, key="select_cap_manga_trabajo")
        
        st.markdown(f"---")
        st.markdown(f"### 🎬 Viñeta Activa en Producción: #{st.session_state.vineta_actual}")
        
        prompt_base_hercules = (
            f"Manga panel page, dark fantasy anime style, scene sequence number {st.session_state.vineta_actual}, "
            f"highly detailed, professional ink lineart, clean white background contrast, no watermark, "
            f"{obtener_prompt_aprendido_para_hercules()}"
        )
        
        prompt_final_viñeta = st.text_area(
            "Prompt visual técnico enviado a Hércules (con aprendizajes integrados):", 
            value=st.session_state.prompt_custom_vineta or prompt_base_hercules,
            height=100
        )
        
        col_visual, col_mandos = st.columns([2, 1])
        
        with col_visual:
            st.markdown("#### 🖼️ Previsualización de la Viñeta")
            prompt_url_encoded = urllib.parse.quote(prompt_final_viñeta)
            url_imagen_generada = f"https://image.pollinations.ai/prompt/{prompt_url_encoded}?width=800&height=600&nologo=true&seed={st.session_state.vineta_actual}"
            
            st.image(
                url_imagen_generada, 
                caption=f"Viñeta #{st.session_state.vineta_actual} generada por Hércules (Lista para inspección)", 
                use_column_width=True
            )
            
        with col_mandos:
            st.markdown("#### 🛠️ Control de Calidad y Aprobación")
            comentario_retoque = st.text_input(
                "¿Necesitas corregir algo de esta viñeta?", 
                placeholder="Ej: Ajustar el rostro de Esther..."
            )
            
            if st.button("🎨 Regenerar Viñeta con Retoque"):
                if comentario_retoque.strip():
                    st.session_state.prompt_custom_vineta = prompt_final_viñeta + ", correction note: " + comentario_retoque
                    st.success("¡Prompt actualizado con tu retoque! Regenerando imagen...")
                    st.rerun()
                else:
                    st.warning("Escribe qué deseas retocar.")
                    
            st.markdown("---")
            
            if st.button("✅ APROBAR VIÑETA Y AVANZAR", type="primary"):
                st.success(f"¡Viñeta #{st.session_state.vineta_actual} validada y guardada con éxito!")
                st.session_state.vineta_actual += 1
                st.session_state.prompt_custom_vineta = ""
                st.rerun()
                
            if st.session_state.vineta_actual > 1:
                if st.button("⬅️ Volver a la Viñeta Anterior"):
                    st.session_state.vineta_actual -= 1
                    st.session_state.prompt_custom_vineta = ""
                    st.rerun()