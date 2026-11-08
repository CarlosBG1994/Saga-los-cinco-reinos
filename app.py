import streamlit as st
import os
import urllib.parse
from motor_diario import (
    cargar_datos_saga, guardar_datos_saga, 
    listar_archivos_capitulos, aura_auditar_capitulo_real
)
from motor_aprendizajes import cargar_aprendizajes, registrar_feedback_hercules

st.set_page_config(page_title="Agencia Literaria - Los Cinco Reinos", layout="wide")

datos = cargar_datos_saga()
aprendizajes = cargar_aprendizajes()

st.title("🛡️ Agencia de Marketing Literario: Los Cinco Reinos")
st.markdown("---")

pestanas = st.tabs([
    "🔑 Credenciales Aisladas", 
    "📜 Auditoría de Capítulos (Aura)", 
    "👥 Gestión de Personajes", 
    "🎨 Taller de Hércules (Aprendizaje)", 
    "📖 Estudio de Manga Paso a Paso"
])

# --- PESTAÑA 1: CREDENCIALES ---
with pestanas[0]:
    st.subheader("Configuración de Credenciales")
    creds = datos.get("credenciales", {})
    with st.form("form_credenciales"):
        c_gemini = st.text_input("Clave API Google AI Studio (Gemini)", value=creds.get("gemini", ""), type="password")
        c_insta = st.text_input("Credenciales Instagram", value=creds.get("instagram", ""))
        c_tik = st.text_input("Credenciales TikTok", value=creds.get("tiktok", ""))
        c_tw = st.text_input("Credenciales Twitter / X", value=creds.get("twitter", ""))
        
        if st.form_submit_button("Guardar Credenciales"):
            datos["credenciales"] = {"gemini": c_gemini, "instagram": c_insta, "tiktok": c_tik, "twitter": c_tw}
            guardar_datos_saga(datos)
            st.success("¡Credenciales guardadas con éxito!")

# --- PESTAÑA 2: AUDITORÍA DE CAPÍTULOS CON AURA ---
with pestanas[1]:
    st.subheader("Auditoría de Capítulos Dinámica con Aura")
    st.markdown("Selecciona cualquiera de tus 25 capítulos para que Aura lea el archivo de texto y extraiga los personajes de forma autónoma.")
    
    archivos = listar_archivos_capitulos()
    if not archivos:
        st.warning("⚠️ No se detectan archivos `.txt` de capítulos en el proyecto. Asegúrate de tener tus capítulos subidos en formato texto.")
    else:
        cap_elegido = st.selectbox("Seleccionar Archivo de Capítulo", archivos)
        if st.button("🔍 Forzar a Aura a Leer y Extraer Personajes"):
            with st.spinner("Aura está analizando el capítulo con Gemini..."):
                ok, msg = aura_auditar_capitulo_real(cap_elegido)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    st.markdown("### Capítulos procesados por Aura:")
    for cap in datos.get("capitulos_auditados", []):
        st.markdown(f"- ✅ `{cap}`")

# --- PESTAÑA 3: GESTIÓN DE PERSONAJES ---
with pestanas[2]:
    st.subheader("Biblioteca Jerárquica de Personajes (Extraídos por Aura)")
    st.markdown("Clasifica a los personajes (Protagonista, Secundario, Terciario, Antagonista), edítalos, elimínalos o añade notas personales para Hércules.")
    
    personajes = datos.get("personajes", [])
    if not personajes:
        st.info("No hay personajes registrados todavía. Ve a la pestaña 'Auditoría de Capítulos' para que Aura los extraiga de tus textos.")
    
    for idx, p in enumerate(personajes):
        with st.expander(f"👤 {p['nombre']} — [{p['rol']}] (Edad/Tipo: {p.get('edad', 'N/A')})"):
            col1, col2 = st.columns(2)
            with col1:
                opciones_rol = ["Protagonista", "Secundario", "Antagonista", "Terciario"]
                rol_actual = p['rol'] if p['rol'] in opciones_rol else "Secundario"
                nuevo_rol = st.selectbox("Jerarquía", opciones_rol, index=opciones_rol.index(rol_actual), key=f"rol_{idx}")
                nueva_desc = st.text_area("Descripción física", value=p['descripcion'], key=f"desc_{idx}")
            with col2:
                nuevas_notas = st.text_area("Notas / Feedback para Hércules", value=p.get('notas', ''), key=f"notas_{idx}")
            
            b_col1, b_col2 = st.columns(2)
            if b_col1.button("💾 Actualizar", key=f"act_{idx}"):
                datos["personajes"][idx]["rol"] = nuevo_rol
                datos["personajes"][idx]["descripcion"] = nueva_desc
                datos["personajes"][idx]["notas"] = nuevas_notas
                guardar_datos_saga(datos)
                st.success("¡Actualizado con éxito!")
                st.rerun()
            if b_col2.button("🗑️ Eliminar", key=f"del_{idx}"):
                datos["personajes"].pop(idx)
                guardar_datos_saga(datos)
                st.rerun()

# --- PESTAÑA 4: TALLER DE HÉRCULES ---
with pestanas[3]:
    st.subheader("Memoria de Aprendizaje de Hércules")
    st.markdown("Instrucciones registradas para que Hércules mejore sus diseños en base a tus correcciones.")
    for pref in aprendizajes.get('preferencias_estilo', []):
        st.markdown(f"- *{pref}*")
    
    tipo_corr = st.selectbox("Tipo de directriz", ["Estilo General", "Personaje Específico", "Regla para el Manga"])
    detalle_corr = st.text_area("Escribe tu instrucción de mejora")
    if st.button("Enseñar a Hércules"):
        if detalle_corr.strip():
            tipo_key = 'estilo' if tipo_corr == 'Estilo General' else ('personaje' if tipo_corr == 'Personaje Específico' else 'manga')
            registrar_feedback_hercules(tipo_key, 'general', detalle_corr)
            st.success("¡Aprendizaje guardado!")
            st.rerun()

# --- PESTAÑA 5: ESTUDIO DE MANGA PASO A PASO ---
with pestanas[4]:
    st.subheader("Estudio de Manga: Generación y Validación Viñeta a Viñeta")
    st.markdown("Hércules genera la imagen de la viñeta actual. **No se avanza a la siguiente viñeta hasta que hagas clic en Aprobar.**")
    
    if "vineta_actual" not in st.session_state:
        st.session_state.vineta_actual = 1
    if "prompt_custom" not in st.session_state:
        st.session_state.prompt_custom = ""

    archivos = listar_archivos_capitulos()
    if archivos:
        cap_manga = st.selectbox("Capítulo a trabajar", archivos, key="cap_manga_select")
        
        st.markdown(f"### 🎬 Viñeta Activa #{st.session_state.vineta_actual}")
        
        prompt_defecto = f"Manga panel page, dark fantasy anime style, scene {st.session_state.vineta_actual}, highly detailed, black and white lineart, clean, no watermark"
        prompt_final = st.text_area("Prompt visual para Hércules:", value=st.session_state.prompt_custom or prompt_defecto)
        
        col_img, col_ctrl = st.columns([2, 1])
        
        with col_img:
            prompt_encoded = urllib.parse.quote(prompt_final)
            img_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=600&nologo=true&seed={st.session_state.vineta_actual}"
            st.image(img_url, caption=f"Viñeta {st.session_state.vineta_actual} generada por Hércules (Sin marcas de agua)", use_column_width=True)
            
        with col_ctrl:
            st.markdown("#### 🛠️ Control de Calidad")
            retoque = st.text_input("¿Qué deseas cambiar en esta viñeta?", placeholder="Ej: Asegurar que Esther sea rubia y pequeña...")
            
            if st.button("🎨 Regenerar con Retoque"):
                st.session_state.prompt_custom = prompt_final + ", " + retoque
                st.rerun()
                
            st.markdown("---")
            if st.button("✅ APROBAR VIÑETA Y PASAR A LA SIGUIENTE", type="primary"):
                st.success(f"¡Viñeta #{st.session_state.vineta_actual} aprobada con éxito!")
                st.session_state.vineta_actual += 1
                st.session_state.prompt_custom = ""
                st.rerun()
                
            if st.session_state.vineta_actual > 1:
                if st.button("⬅️ Volver a la Viñeta Anterior"):
                    st.session_state.vineta_actual -= 1
                    st.session_state.prompt_custom = ""
                    st.rerun()