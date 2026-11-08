import streamlit as st
import os
from motor_diario import cargar_datos_saga, guardar_datos_saga, reauditar_capitulo
from motor_aprendizajes import cargar_aprendizajes, registrar_feedback_hercules

st.set_page_config(page_title="Agencia Literaria - Los Cinco Reinos", layout="wide")

# Cargar datos y aprendizajes
datos = cargar_datos_saga()
aprendizajes = cargar_aprendizajes()

st.title("🛡️ Agencia de Marketing Literario: Los Cinco Reinos")
st.markdown("---")

# Pestañas principales de la agencia
pestanas = st.tabs([
    "🔑 Credenciales Aisladas", 
    "📜 Auditoría de Capítulos (Aura)", 
    "👥 Gestión de Personajes", 
    "🎨 Taller de Hércules (Aprendizaje)", 
    "📖 Estudio de Manga (Viñetas)"
])

# --- PESTAÑA 1: CREDENCIALES AISLADAS ---
with pestanas[0]:
    st.subheader("Configuración de Credenciales por Plataforma")
    st.info("Introduce y guarda las claves de forma independiente sin riesgo de pérdida al cambiar de pestaña.")
    
    creds = datos.get("credenciales", {})
    
    with st.form("form_credenciales"):
        c_gemini = st.text_input("Clave API Google AI Studio (Gemini)", value=creds.get("gemini", ""), type="password")
        c_insta = st.text_input("Credenciales Instagram (Token / Usuario)", value=creds.get("instagram", ""))
        c_tik = st.text_input("Credenciales TikTok (Token / Usuario)", value=creds.get("tiktok", ""))
        c_tw = st.text_input("Credenciales Twitter / X (Token / Usuario)", value=creds.get("twitter", ""))
        
        btn_guardar_creds = st.form_submit_button("Guardar Credenciales")
        if btn_guardar_creds:
            datos["credenciales"] = {
                "gemini": c_gemini,
                "instagram": c_insta,
                "tiktok": c_tik,
                "twitter": c_tw
            }
            guardar_datos_saga(datos)
            st.success("¡Credenciales actualizadas y guardadas con éxito en disco!")

# --- PESTAÑA 2: AUDITORÍA DE CAPÍTULOS (AURA) ---
with pestanas[1]:
    st.subheader("Control y Reauditoría de Capítulos con Aura")
    st.markdown("Selecciona un capítulo para que Aura verifique el texto con tranquilidad y extraiga con rigor todos los personajes y matices.")
    
    cap_seleccionado = st.selectbox("Seleccionar Capítulo", ["Capítulo 0", "Capítulo 1", "Capítulo 2 (Próximo)", "Capítulo 3 (Próximo)"])
    
    col_aud1, col_aud2 = st.columns(2)
    with col_aud1:
        if st.button("Reauditar Capítulo con Aura"):
            resultado = reauditar_capitulo(cap_seleccionado)
            st.success(resultado)
            st.experimental_rerun()
            
    st.markdown("### Capítulos auditados actualmente en el sistema:")
    for cap in datos.get("capitulos_auditados", []):
        st.markdown(f"- ✅ **{cap}**: Procesado y verificado por Aura.")

# --- PESTAÑA 3: GESTIÓN DE PERSONAJES ---
with pestanas[2]:
    st.subheader("Biblioteca Jerárquica de Personajes")
    st.markdown("Clasifica a los personajes por su importancia (Protagonista, Secundario, Terciario), elimínalos si no proceden o añade notas de mejora personal.")
    
    personajes = datos.get("personajes", [])
    
    if not personajes:
        st.info("No hay personajes registrados actualmente.")
    
    for idx, p in enumerate(personajes):
        with st.expander(f"👤 {p['nombre']} — [{p['rol']}] (Edad/Tipo: {p.get('edad', 'N/A')})"):
            col1, col2 = st.columns(2)
            with col1:
                nuevo_rol = st.selectbox(
                    "Jerarquía (Protagonista / Secundario / Terciario / Antagonista)", 
                    ["Protagonista", "Secundario", "Antagonista", "Terciario"], 
                    index=["Protagonista", "Secundario", "Antagonista", "Terciario"].index(p['rol']) if p['rol'] in ["Protagonista", "Secundario", "Antagonista", "Terciario"] else 1,
                    key=f"rol_{idx}"
                )
                nueva_desc = st.text_area("Descripción física y trasfondo", value=p['descripcion'], key=f"desc_{idx}")
            with col2:
                nuevas_notas = st.text_area(
                    "Notas de mejora personal (Feedback para Hércules)", 
                    value=p.get('notas', ''), 
                    key=f"notas_{idx}", 
                    placeholder="Ej: Asegurar que Esther tenga el pelo rubio y aspecto infantil real..."
                )
            
            b_col1, b_col2 = st.columns(2)
            if b_col1.button("💾 Actualizar Personaje", key=f"act_{idx}"):
                datos["personajes"][idx]["rol"] = nuevo_rol
                datos["personajes"][idx]["descripcion"] = nueva_desc
                datos["personajes"][idx]["notas"] = nuevas_notas
                guardar_datos_saga(datos)
                st.success(f"¡Personaje '{p['nombre']}' actualizado con éxito!")
                st.experimental_rerun()
                
            if b_col2.button("🗑️ Eliminar Personaje", key=f"del_{idx}"):
                eliminado = datos["personajes"].pop(idx)
                guardar_datos_saga(datos)
                st.warning(f"Personaje '{eliminado['nombre']}' eliminado de la base de datos.")
                st.experimental_rerun()

# --- PESTAÑA 4: TALLER DE HÉRCULES (APRENDIZAJE) ---
with pestanas[3]:
    st.subheader("Estudio Gráfico e Historial de Aprendizaje de Hércules")
    st.markdown("Hércules registra aquí tus correcciones y directrices para aprender de ti y afinar sus resultados estéticos y narrativos.")
    
    st.markdown("### 🧠 Memoria de Aprendizaje Actual:")
    prefs = aprendizajes.get('preferencias_estilo', [])
    st.write(f"- **Preferencias de estilo registradas:** {len(prefs)}")
    for pref in prefs:
        st.markdown(f"  - *{pref}*")
        
    st.markdown("---")
    st.markdown("### ✍️ Enviar Corrección o Nueva Directriz a Hércules")
    tipo_corr = st.selectbox("Tipo de directriz", ["Estilo General", "Personaje Específico", "Regla para el Manga"])
    detalle_corr = st.text_area(
        "Escribe tu instrucción de mejora", 
        placeholder="Ej: Evita que los rostros salgan raros, asegúrate de que no aparezcan marcas de agua externas y cuida los fondos..."
    )
    
    if st.button("Enseñar a Hércules"):
        if detalle_corr.strip():
            tipo_key = 'estilo' if tipo_corr == 'Estilo General' else ('personaje' if tipo_corr == 'Personaje Específico' else 'manga')
            registrar_feedback_hercules(tipo_key, 'general', detalle_corr)
            st.success("¡Instrucción guardada! Hércules ha incorporado este aprendizaje a su base de conocimiento.")
        else:
            st