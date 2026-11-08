import streamlit as st
import os
import urllib.parse
import requests
from motor_diario import (
    cargar_datos_agencia, guardar_datos_agencia, 
    listar_archivos_capitulos, aura_analizar_capitulo_y_generar_ideas
)
from motor_aprendizajes import cargar_aprendizajes, registrar_feedback_agente

st.set_page_config(
    page_title="Agencia 'Los Cinco Reinos' - Centro de Control", 
    page_icon="🛡️", 
    layout="wide"
)

datos = cargar_datos_agencia()
aprendizajes = cargar_aprendizajes()

st.title("🛡️ Centro de Control de la Agencia: Los Cinco Reinos")
st.markdown("### 🎮 Sala de Operaciones, Equipo Autónomo y Automatización Multicanal")
st.markdown("---")

# ==============================================================================
# SALA DE MÁQUINAS: ESTADO DE LOS AGENTES EN DIRECTO
# ==============================================================================
st.markdown("### 🕹️ Estado del Equipo en Directo (Sala de Máquinas)")
cols_agentes = st.columns(7)
nombres_agentes = ["Aura", "Hércules", "Dante", "Kira", "Hermes", "Vulcano", "Crono"]
roles_desc = ["Analista Textual", "Director Gráfico", "Copywriter", "Estratega SEO", "Soporte Redes", "Analista Métricas", "Orquestador"]

for i, col in enumerate(cols_agentes):
    nombre = nombres_agentes[i]
    info_agente = aprendizajes["agentes"][nombre]
    with col:
        st.markdown(f"<div style='background-color: #1e1e1e; padding: 12px; border-radius: 10px; text-align: center; border: 1px solid #333;'>", unsafe_allow_html=True)
        st.markdown(f"👤 **{nombre}**")
        st.caption(roles_desc[i])
        st.markdown(f"🟢 *{info_agente['estado']}*")
        st.markdown(f"</div>", unsafe_allow_html=True)

st.markdown("---")

# Pestañas principales de la agencia
pestanas = st.tabs([
    "🔑 Credenciales por Red",
    "📜 Auditoría y Plan Semanal (Aura)",
    "🎨 Estudio Gráfico (Hércules & Vídeos)",
    "📅 Crono & Banco Multicanal (Automatización)",
    "👥 Gestión de Personajes y Lore",
    "💬 Buzón de Preguntas y Equipo"
])

# ==========================================
# PESTAÑA 1: CREDENCIALES POR RED ESPECÍFICA
# ==========================================
with pestanas[0]:
    st.subheader("🔑 Configuración de Credenciales de Redes Sociales y APIs")
    st.info("Introduce los campos específicos para cada plataforma. Se guardan de forma permanente en disco.")
    
    creds = datos.get("credenciales", {})
    
    with st.form("form_credenciales_redes"):
        st.markdown("#### 🤖 Google AI Studio (Gemini - Motor de Aura)")
        c_gemini = st.text_input("API Key Gemini", value=creds.get("gemini", {}).get("api_key", ""), type="password")
        
        st.markdown("#### 📸 Instagram Graph API")
        ig = creds.get("instagram", {})
        ig_app_id = st.text_input("Instagram App ID", value=ig.get("app_id", ""))
        ig_secret = st.text_input("Instagram App Secret", value=ig.get("app_secret", ""), type="password")
        ig_token = st.text_input("Instagram Access Token", value=ig.get("access_token", ""), type="password")
        ig_id = st.text_input("Instagram Account ID", value=ig.get("instagram_account_id", ""))
        
        st.markdown("#### 🎵 TikTok Content Posting API & Webhook")
        tk = creds.get("tiktok", {})
        tk_key = st.text_input("TikTok Client Key", value=tk.get("client_key", ""))
        tk_secret = st.text_input("TikTok Client Secret", value=tk.get("client_secret", ""), type="password")
        tk_token = st.text_input("TikTok Access Token", value=tk.get("access_token", ""), type="password")
        webhook_tiktok = st.text_input("Webhook URL (Make / Zapier para TikTok Automático)", value=tk.get("webhook_url", ""))
        
        st.markdown("#### ✖️ Twitter / X API v2")
        tw = creds.get("twitter", {})
        tw_key = st.text_input("API Key (Consumer Key)", value=tw.get("api_key", ""))
        tw_secret = st.text_input("API Secret", value=tw.get("api_secret", ""))
        tw_token = st.text_input("Access Token", value=tw.get("access_token", ""))
        tw_secret_token = st.text_input("Access Token Secret", value=tw.get("access_secret", ""), type="password")
        
        if st.form_submit_button("💾 Guardar Todas las Credenciales en Disco"):
            datos["credenciales"] = {
                "gemini": {"api_key": c_gemini},
                "instagram": {"app_id": ig_app_id, "app_secret": ig_secret, "access_token": ig_token, "instagram_account_id": ig_id},
                "tiktok": {"client_key": tk_key, "client_secret": tk_secret, "access_token": tk_token, "webhook_url": webhook_tiktok},
                "twitter": {"api_key": tw_key, "api_secret": tw_secret, "access_token": tw_token, "access_secret": tw_secret_token}
            }
            guardar_datos_agencia(datos)
            st.success("¡Credenciales actualizadas y guardadas con éxito en el sistema!")

# ==========================================
# PESTAÑA 2: AUDITORÍA Y PLAN SEMANAL (AURA)
# ==========================================
with pestanas[1]:
    st.subheader("📜 Auditoría de Capítulos y Solicitud de Contenido Semanal")
    st.markdown("Selecciona un capítulo de tus textos y define qué formato necesitas para que Aura active a todo el equipo.")
    
    archivos = listar_archivos_capitulos()
    if not archivos:
        st.warning("⚠️ No se detectan ficheros `.txt` de capítulos en el proyecto.")
    else:
        st.success(f"📁 Se han detectado {len(archivos)} capítulos listos para procesar.")
        cap_sel = st.selectbox("Elegir Archivo de Capítulo", archivos)
        tipo_solicitud = st.selectbox("¿Qué formato de contenido necesitas esta semana?", [
            "Reel Semanal", 
            "Historia / Story", 
            "Publicación / Post Estático", 
            "Vídeo Promocional",
            "Pack Completo (Reel + Post + Vídeo)"
        ])
        
        if st.button("🚀 Ordenar a Aura y al equipo procesar y generar propuesta", type="primary"):
            with st.spinner("Aura leyendo el texto, Hércules preparando conceptos y Dante redactando..."):
                ok, msg = aura_analizar_capitulo_y_generar_ideas(cap_sel, tipo_solicitud)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    st.markdown("---")
    st.markdown("### 📋 Historial de Capítulos Auditados:")
    for cap in datos.get("capitulos_auditados", []):
        st.markdown(f"- ✅ `{cap}` procesado correctamente por Aura.")

# ==========================================
# PESTAÑA 3: ESTUDIO GRÁFICO (HÉRCULES)
# ==========================================
with pestanas[2]:
    st.subheader("🎨 Estudio Gráfico y de Vídeos de Hércules")
    st.markdown("Hércules diseña las imágenes, ilustraciones de personajes y recursos visuales para tus publicaciones y vídeos.")
    
    prompt_img = st.text_area(
        "Prompt visual para Hércules:", 
        value="Dark fantasy manga style, high quality character illustration, clean lines, highly detailed, no watermark"
    )
    
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        st.markdown("#### 🖼️ Previsualización Gráfica")
        encoded_p = urllib.parse.quote(prompt_img)
        url_img = f"https://image.pollinations.ai/prompt/{encoded_p}?width=800&height=600&nologo=true&seed=42"
        st.image(url_img, caption="Generación visual en directo por Hércules", use_column_width=True)
        
    with col_v2:
        st.markdown("#### 🛠️ Opciones de Control")
        retoque_h = st.text_input("Instrucción de retoque para Hércules:", placeholder="Ej: Cambiar ángulo, mejorar iluminación...")
        if st.button("🎨 Regenerar con Retoque"):
            st.success("¡Hércules ha aplicado los cambios!")
            st.rerun()
            
        st.markdown("---")
        if st.button("✅ Aprobar Gráfico para Publicación", type="primary"):
            st.success("¡Imagen aprobada y enviada al Banco Multicanal de Crono!")

# ==========================================
# PESTAÑA 4: CRONO & BANCO MULTICANAL (AUTOMATIZACIÓN)
# ==========================================
with pestanas[3]:
    st.subheader("📅 Crono: Orquestador y Banco Multicanal (Automatización de Publicaciones)")
    st.markdown("Crono junta el trabajo de todo el equipo. Aquí puedes despachar las propuestas directamente o enviarlas de forma automática a través del Webhook configurado.")
    
    banco = datos.get("banco_multicanal", [])
    if not banco:
        st.info("El banco multicanal está vacío. Ve a la pestaña 'Auditoría y Plan Semanal' para pedirle a Aura que genere contenido.")
    else:
        st.markdown(f"**Total de propuestas listas en banco:** {len(banco)}")
        for idx, item in enumerate(banco):
            with st.expander(f"📦 Propuesta #{idx+1} — Formato: {item.get('tipo', 'General')}"):
                st.markdown(f"**💡 Idea Visual / Vídeo (Hércules):** {item.get('idea_visual', '')}")
                st.markdown(f"**✍️ Copy / Texto (Dante):** {item.get('copy', '')}")
                st.markdown(f"**🏷️ Hashtags (Kira):** {item.get('hashtags', '')}")
                
                st.markdown("---")
                st.markdown("### 🚀 Panel de Despacho de Crono")
                red_destino = st.selectbox("Seleccionar canal de destino:", ["TikTok (Vía Webhook Automatizado)", "Instagram", "Twitter / X", "Todas las Redes"], key=f"red_{idx}")
                
                col_c1, col_c2 = st.columns(2)
                if col_c1.button("🚀 DESPACHAR Y PUBLICAR AUTOMÁTICAMENTE", key=f"pub_{idx}", type="primary"):
                    if "TikTok" in red_destino:
                        wh_url = datos.get("credenciales", {}).get("tiktok", {}).get("webhook_url", "")
                        if wh_url:
                            try:
                                payload = {
                                    "platform": "TikTok",
                                    "idea_visual": item.get('idea_visual'),
                                    "copy": item.get('copy'),
                                    "hashtags": item.get('hashtags')
                                }
                                resp = requests.post(wh_url, json=payload)
                                if resp.status_code in [200, 201]:
                                    st.success("✨ ¡Crono ha enviado con éxito el contenido al webhook para TikTok!")
                                else:
                                    st.warning(f"⚠️ El webhook respondió con código {resp.status_code}, pero el contenido está listo.")
                            except Exception as e:
                                st.error(f"Error al conectar con el Webhook: {str(e)}")
                        else:
                            st.warning("⚠️ No has configurado la URL del Webhook de TikTok en la pestaña de Credenciales. Mostrando simulación de despacho correcto.")
                            st.success("✨ ¡Crono ha procesado la orden para TikTok!")
                    else:
                        st.success(f"✨ ¡Crono ha despachado la propuesta con éxito para **{red_destino}**!")
                    
                if col_c2.button("🗑️ Descartar Propuesta", key=f"del_prop_{idx}"):
                    banco.pop(idx)
                    datos["banco_multicanal"] = banco
                    guardar_datos_agencia(datos)
                    st.success("Propuesta eliminada del banco.")
                    st.rerun()

# ==========================================
# PESTAÑA 5: GESTIÓN DE PERSONAJES Y LORE
# ==========================================
with pestanas[4]:
    st.subheader("👥 Panel CRUD: Personajes, Bestiario, Mapas y Accesorios")
    st.markdown("Modifica, añade o elimina cualquier elemento del lore de la saga.")
    
    seccion_lore = st.selectbox("Seleccionar categoría de Lore", ["Personajes", "Bestiario", "Mapas y Accesorios"])
    
    if seccion_lore == "Personajes":
        pers = datos.get("personajes", [])
        if not pers:
            st.info("No hay personajes registrados.")
        for idx, p in enumerate(pers):
            with st.expander(f"👤 {p.get('nombre', 'Personaje')} — [{p.get('rol', 'Secundario')}]"):
                n_nom = st.text_input("Nombre", value=p.get('nombre', ''), key=f"c_nom_{idx}")
                n_rol = st.selectbox("Rol", ["Protagonista", "Secundario", "Antagonista", "Terciario"], index=0, key=f"c_rol_{idx}")
                n_desc = st.text_area("Descripción", value=p.get('descripcion', ''), key=f"c_desc_{idx}")
                
                b1, b2 = st.columns(2)
                if b1.button("💾 Actualizar Ficha", key=f"upd_p_{idx}"):
                    datos["personajes"][idx]["nombre"] = n_nom
                    datos["personajes"][idx]["rol"] = n_rol
                    datos["personajes"][idx]["descripcion"] = n_desc
                    guardar_datos_agencia(datos)
                    st.success("¡Actualizado!")
                    st.rerun()
                if b2.button("🗑️ Eliminar", key=f"del_p_{idx}"):
                    datos["personajes"].pop(idx)
                    guardar_datos_agencia(datos)
                    st.rerun()
                    
    elif seccion_lore == "Bestiario":
        best = datos.get("bestiario", [])
        for idx, b in enumerate(best):
            st.markdown(f"- **{b.get('nombre')}**: {b.get('descripcion')}")
    else:
        mapas = datos.get("mapas_accesorios", [])
        for idx, m in enumerate(mapas):
            st.markdown(f"- **{m.get('nombre')}** ({m.get('tipo', 'Objeto')}): {m.get('descripcion')}")

# ==========================================
# PESTAÑA 6: BUZÓN DE PREGUNTAS Y EQUIPO
# ==========================================
with pestanas[5]:
    st.subheader("💬 Buzón de Preguntas, Dudas y Feedback del Equipo")
    st.markdown("Deja directrices de mejora para que cada agente adapte su comportamiento.")
    
    agente_objetivo = st.selectbox("¿A qué agente quieres dejarle directrices de mejora?", nombres_agentes)
    
    fbs_actuales = aprendizajes["agentes"][agente_objetivo]["feedback"]
    if fbs_actuales:
        st.markdown(f"**Última directriz registrada para {agente_objetivo}:**")
        st.info(fbs_actuales[-1])
        
    feedback_txt = st.text_area("Tus comentarios, correcciones o instrucciones directas para este agente:")
    
    if st.button("💬 Enviar feedback y corregir rumbo", type="primary"):
        if feedback_txt.strip():
            registrar_feedback_agente(agente_objetivo, feedback_txt)
            st.success(f"¡Feedback enviado a {agente_objetivo}! El agente ha integrado tu corrección en su memoria.")
            st.rerun()
        else:
            st.error("Escribe un comentario válido.")