# ============================================
# VOTO COLOMBIA 2026 - Sistema de Encuesta Electoral
# Creador: Deiber Yesid López Ramírez
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(
    layout="wide",
    page_title="🇨🇴 Elecciones en Colombia 2026",
    page_icon="🇨🇴"
)

# ================= CSS (oculta el icono original y agrega emoji personalizado) =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Exo+2:wght@400;700;900&display=swap');

    /* Ocultar el icono original del menú hamburger */
    section[data-testid="stSidebar"] > div:first-child > div:first-child > div:first-child > div:first-child > button {
        display: none !important;
    }

    /* Botón personalizado con emoji para abrir sidebar */
    .custom-menu-button {
        position: fixed;
        top: 15px;
        left: 15px;
        z-index: 9999;
        background: linear-gradient(145deg, #FFD700, #FFA500);
        color: #000000;
        font-size: 2.5rem;
        font-weight: 900;
        border: none;
        border-radius: 15px;
        padding: 10px 15px;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .custom-menu-button:hover {
        transform: scale(1.1);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.8);
    }

    /* Resto de tu CSS (fondo, carrusel, títulos, etc.) */
    .stApp {background: none;}
    .background-carousel {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1; overflow: hidden;
    }
    .background-carousel img {
        position: absolute;
        width: 100%; height: 100%;
        object-fit: cover;
        opacity: 0;
        animation: carousel 24s infinite;
    }
    .background-carousel img:nth-child(1) {animation-delay: 0s;}
    .background-carousel img:nth-child(2) {animation-delay: 8s;}
    .background-carousel img:nth-child(3) {animation-delay: 16s;}
    @keyframes carousel {
        0% {opacity: 0;}
        10% {opacity: 1;}
        30% {opacity: 1;}
        40% {opacity: 0;}
        100% {opacity: 0;}
    }

    .stApp::after {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75);
        z-index: -1;
        pointer-events: none;
    }

    /* Tus estilos de texto, títulos, botones, cards, etc. (los mantengo igual) */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FFD700 100%);
        background-size: 200% auto;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-align: center !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        animation: shimmer 3s linear infinite;
        letter-spacing: 4px !important;
        filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8)) !important;
    }

    @keyframes shimmer {
        0% {background-position: 0% 50%;}
        100% {background-position: 200% 50%;}
    }

    h2 {
        font-family: 'Exo 2', sans-serif !important;
        background: linear-gradient(135deg, #87CEEB 0%, #4A90E2 50%, #87CEEB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        animation: shimmer 4s linear infinite;
        letter-spacing: 3px !important;
        filter: drop-shadow(0 0 20px rgba(135, 206, 235, 0.8)) !important;
    }

    .stButton>button {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(145deg, #FFD700, #FFA500) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        padding: 18px 35px !important;
        font-size: 1.3rem !important;
        border: 3px solid #FFD700 !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.8) !important;
    }

    .card-modern {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(15, 12, 41, 0.95));
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        border: 3px solid rgba(255, 215, 0, 0.6);
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
    }

    .stSidebar {
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.95), rgba(15, 20, 25, 0.98));
        backdrop-filter: blur(25px);
        border-right: 4px solid rgba(255, 215, 0, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# ================= BOTÓN PERSONALIZADO CON EMOJI (reemplaza la flecha) =================
# Emoji: 🇨🇴 (bandera Colombia) – cambia por 🗳️ o ☰ si quieres
st.markdown("""
<button class="custom-menu-button" onclick="document.querySelector('[data-testid=\'stSidebarCollapseButton\']').click()">🇨🇴</button>
""", unsafe_allow_html=True)

# ================= CARRUSEL =================
st.markdown("""
<div class="background-carousel">
    <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/Presidente_Gustavo_Petro.jpg">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/1280px-Flag_of_Colombia.svg.png">
    <img src="https://images.unsplash.com/photo-1582213782179-4841c6f00b1d">
</div>
""", unsafe_allow_html=True)

# ================= DATA =================
candidatos = [
    "Gustavo Petro (hipotético)", "Paloma Valencia", "Iván Cepeda",
    "Sergio Fajardo", "Vicky Dávila", "Abelardo de la Espriella",
    "David Luna", "Juan Daniel Oviedo", "Otro"
]

if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(
        columns=["candidato", "hora", "nombre", "ult5", "departamento"]
    )

# ================= HEADER =================
st.title("Elecciones Colombia 2026")
st.markdown("### Analisis Electoral Seguro")
st.markdown("**Vote por el candidato presidencial de su elección para un próximo periodo.**")
st.markdown("**Vote si hipotéticamente GUSTAVO PETRO fuera candidato electo, nos gustaría saber quiénes apoyan al actual presidente para un próximo periodo.**")
st.markdown("**Con su voto aquí plasmado comparamos la diferencia con fuentes REALES.**")
st.markdown("---")

# ================= ENLACES OFICIALES =================
st.markdown("### 📊 FUENTES OFICIALES DE LAS ELECCIONES EN COLOMBIA")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="card-modern">
        <h4 style="color: #FFD700; text-align: center;">🏛️ Registraduría</h4>
        <p style="text-align: center;">
            <a href="https://estadisticaselectorales.registraduria.gov.co/" target="_blank" style="color: #FFD700; text-decoration: none;">📈 Ver Estadísticas</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="card-modern">
        <h4 style="color: #FFD700; text-align: center;">👁️ MOE</h4>
        <p style="text-align: center;">
            <a href="https://moe.org.co/" target="_blank" style="color: #FFD700; text-decoration: none;">🔍 Portal MOE</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="card-modern">
        <h4 style="color: #FFD700; text-align: center;">📚 CEDAE</h4>
        <p style="text-align: center;">
            <a href="https://cedae.datasketch.co/" target="_blank" style="color: #FFD700; text-decoration: none;">💾 Base de Datos</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")

# ================= SIDEBAR - VOTACIÓN =================
with st.sidebar:
    st.header("🗳️ EMITE TU VOTO")
    with st.form("form_voto_sidebar"):
        nombre = st.text_input("✍️ Nombre", placeholder="Tu nombre")
        departamento = st.selectbox("📍 Departamento", [
            "Selecciona...", "Antioquia", "Atlántico", "Bogotá D.C.",
            "Bolívar", "Boyacá", "Caldas", "Caquetá", "Cauca", "Cesar",
            "Córdoba", "Cundinamarca", "Huila", "La Guajira", "Magdalena",
            "Meta", "Nariño", "Norte de Santander", "Quindío", "Risaralda",
            "Santander", "Sucre", "Tolima", "Valle del Cauca"
        ])
        ult5 = st.text_input("🔢 Últimos 5 dígitos cédula", max_chars=5, type="password")
        candidato = st.selectbox("🎯 Candidato", candidatos)
        submitted = st.form_submit_button("✅ VOTAR AHORA", use_container_width=True)
        if submitted:
            if not nombre or departamento == "Selecciona..." or len(ult5) != 5:
                st.error("❌ Completa todos los campos correctamente")
            elif not ult5.isdigit():
                st.error("❌ La cédula debe contener solo números")
            elif ult5 in st.session_state.datos_votos["ult5"].values:
                st.error("❌ Esta cédula ya votó. Un voto por persona.")
            else:
                nuevo_voto = pd.DataFrame({
                    "candidato": [candidato],
                    "hora": [datetime.now()],
                    "nombre": [nombre],
                    "ult5": [ult5],
                    "departamento": [departamento]
                })
                st.session_state.datos_votos = pd.concat([st.session_state.datos_votos, nuevo_voto], ignore_index=True)
                st.success("✅ ¡Voto registrado exitosamente! 🇨🇴")
                st.balloons()
                st.rerun()

    st.divider()
    st.metric("📊 Total Votos", len(st.session_state.datos_votos))

# ================= CONTENIDO PRINCIPAL =================
if st.session_state.datos_votos.empty:
    st.markdown("""
    <div style="text-align: center; padding: 100px 20px;">
        <div style="background: rgba(0, 0, 0, 0.9); backdrop-filter: blur(25px); border-radius: 30px; padding: 80px 40px; border: 3px solid rgba(255, 215, 0, 0.6); box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8); max-width: 800px; margin: 0 auto;">
            <div style="font-size: 5rem; margin-bottom: 30px;">🗳️</div>
            <h2 style="font-family: 'Orbitron', sans-serif; color: #FFD700; font-size: 3rem; margin-bottom: 20px; text-shadow: 0 0 30px rgba(255, 215, 0, 0.8);">¡Inicia la Encuesta Electoral!</h2>
            <p style="font-family: 'Exo 2', sans-serif; color: #FFFFFF; font-size: 1.5rem; margin-bottom: 40px; text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9);">Sé el primero en hacer historia</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    resumen = st.session_state.datos_votos.groupby("candidato").size().reset_index(name="votos").sort_values("votos", ascending=False)
    total = resumen["votos"].sum()
    resumen["porcentaje"] = (resumen["votos"] / total * 100).round(2)

    tab1, tab2, tab3 = st.tabs(["📊 RESULTADOS", "📈 ANÁLISIS", "📋 DATOS"])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🥇 LÍDER", resumen.iloc[0]["candidato"], f"{resumen.iloc[0]['porcentaje']}%")
        with col2:
            st.metric("📊 TOTAL", total)
        with col3:
            if len(resumen) > 1:
                dif = resumen.iloc[0]["porcentaje"] - resumen.iloc[1]["porcentaje"]
                st.metric("📉 DIFERENCIA", f"{dif:.1f}%")
        with col4:
            deptos = st.session_state.datos_votos["departamento"].nunique()
            st.metric("🗺️ DEPARTAMENTOS", deptos)

        st.markdown("---")

        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader("🏆 RANKING")
            for idx, row in resumen.iterrows():
                st.write(f"**#{idx+1} {row['candidato']}** - {row['porcentaje']}%")
                st.progress(row["porcentaje"]/100)
                st.caption(f"{row['votos']} votos")

        with col_r:
            st.subheader("📊 DISTRIBUCIÓN")
            fig = px.pie(resumen, values="votos", names="candidato", hole=0.5)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("📈 COMPARATIVA")
        fig_bar = px.bar(resumen, x="votos", y="candidato", orientation="h", color="porcentaje")
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("🗺️ POR DEPARTAMENTO")
        votos_depto = st.session_state.datos_votos.groupby('departamento').size().reset_index(name='votos').sort_values('votos', ascending=False)
        fig_dep = px.bar(votos_depto, x="votos", y="departamento", orientation="h")
        fig_dep.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig_dep, use_container_width=True)

    with tab3:
        st.subheader("📋 DATOS DE VOTACIÓN")
        datos_mostrar = st.session_state.datos_votos[['nombre', 'candidato', 'departamento', 'hora']].copy()
        datos_mostrar['hora'] = datos_mostrar['hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(datos_mostrar, use_container_width=True)

        csv = datos_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", data=csv, file_name=f'votos_{datetime.now().strftime("%Y%m%d")}.csv', mime='text/csv')

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #FFFFFF; padding: 20px;">
    <p style="font-size: 1.2rem;"><b>✨ Desarrollado por Deiber Yesid López Ramírez - Student Data Analyst</b></p>
    <p>Encuesta no oficial • Consulta fuentes oficiales arriba</p>
</div>
""", unsafe_allow_html=True)
