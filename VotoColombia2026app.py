# ============================================
# VOTO COLOMBIA 2026 - Sistema de Encuesta Electoral
# Creador: Deiber Yesid López Ramírez
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Configuración básica
st.set_page_config(
    layout="wide", 
    page_title="🇨🇴 Elecciones en Colombia 2026", 
    page_icon="🇨🇴"
)

# CSS Optimizado con colores mejorados
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Exo+2:wght@400;700;900&display=swap');
    
    /* ===== FONDO CON CARRUSEL DE IMÁGENES ===== */
    .stApp {
        background: none;
    }

    .background-carousel {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }

    .background-carousel img {
        position: absolute;
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0;
        animation: carousel 24s infinite;
    }

    .background-carousel img:nth-child(1) { animation-delay: 0s; }
    .background-carousel img:nth-child(2) { animation-delay: 8s; }
    .background-carousel img:nth-child(3) { animation-delay: 16s; }

    @keyframes carousel {
        0% { opacity: 0; }
        10% { opacity: 1; }
        30% { opacity: 1; }
        40% { opacity: 0; }
        100% { opacity: 0; }
    }
    
    /* Overlay oscuro para mejor contraste */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.75);
        z-index: -1;
        pointer-events: none;
    }
    
    /* ===== ESTILOS GLOBALES DE TEXTO ===== */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Markdown y párrafos */
    .stMarkdown, .stMarkdown p {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9) !important;
        font-weight: 500 !important;
    }
    
    /* Títulos principales */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FFD700 100%);
        background-size: 200% auto;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-align: center !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        animation: shimmer 3s linear infinite, glow 2s ease-in-out infinite !important;
        letter-spacing: 4px !important;
        margin: 30px 0 !important;
        filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8)) !important;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    @keyframes glow {
        0%, 100% { 
            filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.6));
        }
        50% { 
            filter: drop-shadow(0 0 40px rgba(255, 215, 0, 1));
        }
    }
    
    /* Subtítulos h2 */
    h2 {
        font-family: 'Exo 2', sans-serif !important;
        background: linear-gradient(135deg, #87CEEB 0%, #4A90E2 50%, #87CEEB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        animation: shimmer 4s linear infinite !important;
        letter-spacing: 3px !important;
        filter: drop-shadow(0 0 20px rgba(135, 206, 235, 0.8)) !important;
    }
    
    /* Subtítulos h3 */
    h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #FFD700 !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        text-shadow: 
            0 0 20px rgba(255, 215, 0, 0.8),
            0 0 40px rgba(255, 215, 0, 0.6),
            2px 2px 8px rgba(0, 0, 0, 0.9) !important;
        letter-spacing: 2px !important;
    }
    
    /* Subtítulos h4 */
    h4 {
        color: #FFD700 !important;
        font-family: 'Exo 2', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        text-shadow: 
            0 0 15px rgba(255, 215, 0, 0.7),
            2px 2px 6px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Textos de párrafo */
    p, span, div {
        color: #FFFFFF !important;
        font-family: 'Exo 2', sans-serif !important;
        font-weight: 500 !important;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Botones */
    .stButton>button {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(145deg, #FFD700, #FFA500) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        padding: 18px 35px !important;
        font-size: 1.3rem !important;
        border: 3px solid #FFD700 !important;
        box-shadow: 
            0 8px 25px rgba(255, 215, 0, 0.6),
            inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        text-shadow: none !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 15px 40px rgba(255, 215, 0, 0.8),
            inset 0 3px 0 rgba(255, 255, 255, 0.4) !important;
        background: linear-gradient(145deg, #FFA500, #FFD700) !important;
    }
    
    /* Cards modernas */
    .card-modern {
        background: linear-gradient(135deg, 
            rgba(0, 0, 0, 0.9) 0%, 
            rgba(15, 12, 41, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        border: 3px solid rgba(255, 215, 0, 0.6) !important;
        margin: 20px 0 !important;
        transition: all 0.4s ease !important;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.8),
            0 0 40px rgba(255, 215, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }
    
    .card-modern:hover {
        transform: translateY(-10px) scale(1.02) !important;
        box-shadow: 
            0 20px 60px rgba(255, 215, 0, 0.5),
            0 0 60px rgba(255, 215, 0, 0.4) !important;
        border-color: #FFD700 !important;
    }
    
    .card-modern h4 {
        color: #FFD700 !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.8) !important;
    }
    
    .card-modern p {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9) !important;
    }
    
    .card-modern a {
        color: #FFD700 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-decoration: none !important;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.7) !important;
        transition: all 0.3s ease !important;
    }
    
    .card-modern a:hover {
        color: #FFA500 !important;
        text-shadow: 0 0 25px rgba(255, 215, 0, 1) !important;
        transform: scale(1.1) !important;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: pulse 2s ease-in-out infinite !important;
        filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.8)) !important;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Exo 2', sans-serif !important;
        color: #87CEEB !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        text-shadow: 
            0 0 20px rgba(135, 206, 235, 0.8),
            2px 2px 6px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Labels de inputs */
    .stTextInput>label, .stSelectbox>label {
        font-family: 'Exo 2', sans-serif !important;
        color: #FFD700 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        text-shadow: 
            0 0 15px rgba(255, 215, 0, 0.8),
            2px 2px 6px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Inputs */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        font-family: 'Exo 2', sans-serif !important;
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.9), rgba(30, 40, 55, 0.9)) !important;
        backdrop-filter: blur(15px) !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border: 3px solid rgba(255, 215, 0, 0.5) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 
            inset 0 2px 8px rgba(0, 0, 0, 0.6),
            0 0 20px rgba(255, 215, 0, 0.2) !important;
        transition: all 0.3s ease !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8) !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #FFD700 !important;
        box-shadow: 
            0 0 30px rgba(255, 215, 0, 0.6),
            inset 0 2px 8px rgba(0, 0, 0, 0.6) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(15, 20, 25, 0.95));
        backdrop-filter: blur(20px);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
        border: 2px solid rgba(255, 215, 0, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.8), rgba(30, 40, 55, 0.9)) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        color: #87CEEB !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        border: 3px solid rgba(135, 206, 235, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        text-shadow: 
            0 0 15px rgba(135, 206, 235, 0.7),
            2px 2px 6px rgba(0, 0, 0, 0.9) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #FFD700 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.5) !important;
        color: #FFD700 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #FFD700, #FFA500) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border: 3px solid #FFD700 !important;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.8) !important;
        transform: scale(1.08) !important;
        text-shadow: none !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, 
            #FFD700 0%, 
            #FFA500 25%, 
            #FFD700 50%, 
            #FFA500 75%, 
            #FFD700 100%) !important;
        background-size: 200% auto !important;
        animation: shimmer 2s linear infinite !important;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.8) !important;
        border-radius: 10px !important;
        height: 14px !important;
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, 
            rgba(0, 0, 0, 0.95) 0%, 
            rgba(15, 20, 25, 0.98) 100%) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 4px solid rgba(255, 215, 0, 0.6) !important;
        box-shadow: 5px 0 40px rgba(0, 0, 0, 0.9) !important;
    }
    
    .stSidebar h2, .stSidebar h3 {
        color: #FFD700 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.8) !important;
    }
    
    /* Captions */
    .stCaption, .caption {
        color: #87CEEB !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        text-shadow: 
            0 0 10px rgba(135, 206, 235, 0.7),
            2px 2px 5px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Info boxes */
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 15px !important;
        padding: 20px !important;
        border-left: 5px solid !important;
        backdrop-filter: blur(20px) !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.9) !important;
    }
    
    .stInfo {
        background: rgba(135, 206, 235, 0.2) !important;
        border-color: #87CEEB !important;
        color: #FFFFFF !important;
    }
    
    .stSuccess {
        background: rgba(0, 255, 127, 0.2) !important;
        border-color: #00FF7F !important;
        color: #FFFFFF !important;
    }
    
    .stWarning {
        background: rgba(255, 215, 0, 0.2) !important;
        border-color: #FFD700 !important;
        color: #FFFFFF !important;
    }
    
    .stError {
        background: rgba(255, 50, 50, 0.2) !important;
        border-color: #FF3232 !important;
        color: #FFFFFF !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        background: rgba(0, 0, 0, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 15px !important;
        border: 3px solid rgba(135, 206, 235, 0.4) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 4px !important;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 215, 0, 0.8), 
            transparent) !important;
        margin: 40px 0 !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 16px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border-radius: 10px;
        border: 2px solid rgba(0, 0, 0, 0.7);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FFA500, #FFD700);
        box-shadow: 0 0 25px rgba(255, 215, 0, 1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="background-carousel">
    <img src="https://images.unsplash.com/photo-1581090700227-1e37b190418e">
    <img src="https://images.unsplash.com/photo-1541873676-a18131494184">
    <img src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620">
</div>
""", unsafe_allow_html=True)

# Datos
candidatos = [
    "Gustavo Petro (hipotético)", "Paloma Valencia", "Iván Cepeda",
    "Sergio Fajardo", "Vicky Dávila", "Abelardo de la Espriella",
    "David Luna", "Juan Daniel Oviedo", "Otro"
]

# Inicializar estados
if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(
        columns=["candidato", "votos", "hora", "nombre", "ult5", "departamento"]
    )

if "show_vote_modal" not in st.session_state:
    st.session_state.show_vote_modal = False

def generar_hash(cedula):
    return hashlib.sha256(cedula.encode()).hexdigest()[:16]

# HEADER
st.title("🇨🇴 Elecciones Colombia 2026")
st.markdown("### Encuesta Electoral Segura")
st.markdown("**Vote si hipotéticamente GUSTAVO PETRO fuera candidato electo, nos gustaría saber quiénes apoyan al actual presidente para un próximo periodo**")
st.markdown("---")

# Enlaces Oficiales
st.markdown("### 📊 FUENTES OFICIALES DE ELECCIONES")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card-modern">
        <h4 style="color: #FFD700; text-align: center;">🏛️ Registraduría</h4>
        <p style="text-align: center;">
            <a href="https://estadisticaselectorales.registraduria.gov.co/" target="_blank" 
               style="color: #FFD700; text-decoration: none;">📈 Ver Estadísticas</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card-modern">
        <h4 style="color: #FFD700; text-align: center;">👁️ MOE</h4>
        <p style="text-align: center;">
            <a href="https://moe.org.co/" target="_blank" 
               style="color: #FFD700; text-decoration: none;">🔍 Portal MOE</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card-modern">
        <h4 style="color: #FFD700; text-align: center;">📚 CEDAE</h4>
        <p style="text-align: center;">
            <a href="https://cedae.datasketch.co/" target="_blank" 
               style="color: #FFD700; text-decoration: none;">💾 Base de Datos</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# SIDEBAR - VOTACIÓN
with st.sidebar:
    st.header("🗳️ EMITE TU VOTO")
    
    with st.form("form_voto_sidebar"):
        nombre = st.text_input("✍️ Nombre", placeholder="Tu nombre", key="nombre_sidebar")
        departamento = st.selectbox("📍 Departamento", [
            "Selecciona...", "Antioquia", "Atlántico", "Bogotá D.C.", 
            "Bolívar", "Boyacá", "Caldas", "Caquetá", "Cauca", "Cesar",
            "Córdoba", "Cundinamarca", "Huila", "La Guajira", "Magdalena",
            "Meta", "Nariño", "Norte de Santander", "Quindío", "Risaralda",
            "Santander", "Sucre", "Tolima", "Valle del Cauca"
        ], key="depto_sidebar")
        ult5 = st.text_input("🔢 Últimos 5 dígitos cédula", max_chars=5, type="password", key="cedula_sidebar")
        candidato = st.selectbox("🎯 Candidato", candidatos, key="candidato_sidebar")
        
        submitted = st.form_submit_button("✅ VOTAR AHORA", use_container_width=True)
        
        if submitted:
            if not nombre or departamento == "Selecciona..." or len(ult5) != 5:
                st.error("❌ Completa todos los campos correctamente")
            elif ult5 in st.session_state.datos_votos["ult5"].values:
                st.error("❌ Esta cédula ya votó")
            else:
                nuevo = pd.DataFrame({
                    "candidato": [candidato],
                    "votos": [1],
                    "hora": [datetime.now()],
                    "nombre": [nombre],
                    "ult5": [ult5],
                    "departamento": [departamento]
                })
                st.session_state.datos_votos = pd.concat(
                    [st.session_state.datos_votos, nuevo], ignore_index=True
                )
                st.success("✅ ¡Voto registrado! 🇨🇴")
                st.balloons()
                st.rerun()
    
    st.divider()
    st.metric("📊 Total Votos", len(st.session_state.datos_votos))

# CONTENIDO PRINCIPAL
if st.session_state.datos_votos.empty:
    st.markdown("""
    <div style="text-align: center; padding: 100px 20px;">
        <div style="
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(25px);
            border-radius: 30px;
            padding: 80px 40px;
            border: 3px solid rgba(255, 215, 0, 0.6);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
            max-width: 800px;
            margin: 0 auto;
        ">
            <div style="font-size: 5rem; margin-bottom: 30px;">🗳️</div>
            <h2 style="
                font-family: 'Orbitron', sans-serif;
                color: #FFD700;
                font-size: 3rem;
                margin-bottom: 20px;
                text-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
            ">¡Inicia la Encuesta Electoral!</h2>
            <p style="
                font-family: 'Exo 2', sans-serif;
                color: #FFFFFF;
                font-size: 1.5rem;
                margin-bottom: 40px;
                text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9);
            ">Sé el primero en hacer historia</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 EMITIR MI VOTO AHORA", use_container_width=True, key="btn_iniciar_voto"):
            st.session_state.show_vote_modal = True
            st.rerun()
    
    if st.session_state.show_vote_modal:
        modal_container = st.container()
        
        with modal_container:
            col_modal1, col_modal2, col_modal3 = st.columns([1, 3, 1])
            
            with col_modal2:
                st.markdown("""
                <div style="text-align: center; margin-bottom: 40px;">
                    <h2 style="
                        font-family: 'Orbitron', sans-serif;
                        color: #FFD700;
                        font-size: 2.5rem;
                        text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
                    ">🗳️ FORMULARIO DE VOTACIÓN</h2>
                    <p style="color: #FFFFFF; font-size: 1.2rem; text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9);">Completa tus datos para emitir tu voto</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("✖️ CERRAR", key="btn_cerrar_modal", use_container_width=True):
                    st.session_state.show_vote_modal = False
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                with st.form("form_voto_modal"):
                    nombre_modal = st.text_input(
                        "✍️ Nombre Completo",
                        placeholder="Ingresa tu nombre",
                        key="nombre_modal"
                    )
                    
                    departamento_modal = st.selectbox(
                        "📍 Departamento",
                        [
                            "Selecciona...", "Antioquia", "Atlántico", "Bogotá D.C.", 
                            "Bolívar", "Boyacá", "Caldas", "Caquetá", "Cauca", "Cesar",
                            "Córdoba", "Cundinamarca", "Huila", "La Guajira", "Magdalena",
                            "Meta", "Nariño", "Norte de Santander", "Quindío", "Risaralda",
                            "Santander", "Sucre", "Tolima", "Valle del Cauca"
                        ],
                        key="depto_modal"
                    )
                    
                    ult5_modal = st.text_input(
                        "🔢 Últimos 5 dígitos de cédula",
                        placeholder="12345",
                        max_chars=5,
                        type="password",
                        key="cedula_modal"
                    )
                    
                    candidato_modal = st.selectbox(
                        "🎯 Candidato de tu preferencia",
                        candidatos,
                        key="candidato_modal"
                    )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    submitted_modal = st.form_submit_button(
                        "✅ CONFIRMAR VOTO",
                        use_container_width=True
                    )
                    
                    if submitted_modal:
                        if not nombre_modal or departamento_modal == "Selecciona..." or len(ult5_modal) != 5:
                            st.error("❌ Completa todos los campos correctamente")
                        elif not ult5_modal.isdigit():
                            st.error("❌ La cédula debe contener solo números")
                        elif ult5_modal in st.session_state.datos_votos["ult5"].values:
                            st.error("❌ Esta cédula ya votó. Un voto por persona.")
                        else:
                            nuevo_voto = pd.DataFrame({
                                "candidato": [candidato_modal],
                                "votos": [1],
                                "hora": [datetime.now()],
                                "nombre": [nombre_modal],
                                "ult5": [ult5_modal],
                                "departamento": [departamento_modal]
                            })
                            
                            st.session_state.datos_votos = pd.concat(
                                [st.session_state.datos_votos, nuevo_voto],
                                ignore_index=True
                            )
                            
                            st.success("✅ ¡Voto registrado exitosamente! 🇨🇴")
                            st.balloons()
                            st.session_state.show_vote_modal = False
                            st.rerun()

else:
    resumen = (st.session_state.datos_votos
               .groupby("candidato")["votos"]
               .sum()
               .reset_index()
               .sort_values("votos", ascending=False))
    total = resumen["votos"].sum()
    resumen["porcentaje"] = (resumen["votos"] / total * 100).round(2)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 RESULTADOS",
        "📈 ANÁLISIS",
        "📋 DATOS",
        "🧠 MACHINE LEARNING"
    ])
    
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
                st.progress(row['porcentaje']/100)
                st.caption(f"{row['votos']} votos")
        
        with col_r:
            st.subheader("📊 DISTRIBUCIÓN")
            fig = px.pie(
                resumen, 
                values='votos', 
                names='candidato',
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Sunset
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📈 COMPARATIVA")
        fig_bar = px.bar(
            resumen,
            x='votos',
            y='candidato',
            orientation='h',
            color='porcentaje',
            color_continuous_scale='Sunset',
            text='porcentaje'
        )
        fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_bar.update_layout(
            yaxis={'categoryorder':'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        if len(st.session_state.datos_votos) > 0:
            st.subheader("🗺️ POR DEPARTAMENTO")
            votos_depto = (st.session_state.datos_votos
                          .groupby('departamento')
                          .size()
                          .reset_index(name='votos')
                          .sort_values('votos', ascending=False)
                          .head(10))
            
            fig_dep = px.bar(
                votos_depto,
                x='votos',
                y='departamento',
                orientation='h',
                color='votos',
                color_continuous_scale='Tealgrn'
            )
            fig_dep.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )
            st.plotly_chart(fig_dep, use_container_width=True)
    
    with tab3:
        st.subheader("📋 DATOS DE VOTACIÓN")
        datos_mostrar = st.session_state.datos_votos[['nombre', 'candidato', 'departamento', 'hora']].copy()
        datos_mostrar['hora'] = datos_mostrar['hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(datos_mostrar, use_container_width=True)
        
        csv = datos_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar CSV",
            data=csv,
            file_name=f'votos_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    
    with tab4:
        st.subheader("🧠 Análisis Avanzado con Machine Learning")
        
        if len(st.session_state.datos_votos) < 10:
            st.warning("⚠️ Se necesitan al menos 10 votos para realizar análisis de Machine Learning")
        else:
            cluster_df = (
                st.session_state.datos_votos
                .groupby("departamento")
                .agg(
                    total_votos=("candidato", "count"),
                    diversidad_candidatos=("candidato", "nunique")
                )
                .reset_index()
            )
            
            st.markdown("### 📋 Variables Analizadas")
            st.dataframe(cluster_df)
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(
                cluster_df[["total_votos", "diversidad_candidatos"]]
            )
            
            n_clusters = min(3, len(cluster_df))
            
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init=10
            )
            cluster_df["cluster"] = kmeans.fit_predict(X_scaled)
            
            if n_clusters > 1:
                score = silhouette_score(X_scaled, cluster_df["cluster"])
                st.metric("📐 Silhouette Score", f"{score:.3f}")
            
            fig_cluster = px.scatter(
                cluster_df,
                x="total_votos",
                y="diversidad_candidatos",
                color="cluster",
                text="departamento",
                size="total_votos",
                color_continuous_scale="Viridis",
                labels={
                    "total_votos": "Total de votos",
                    "diversidad_candidatos": "Diversidad de candidatos"
                },
                title="Clustering de Departamentos por Comportamiento Electoral"
            )
            
            fig_cluster.update_traces(textposition="top center")
            fig_cluster.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )
            
            st.plotly_chart(fig_cluster, use_container_width=True)
            
            st.markdown("### 🔬 PCA – Reducción Dimensional")
            
            pca = PCA(n_components=2)
            pca_result = pca.fit_transform(X_scaled)
            
            pca_df = pd.DataFrame(
                pca_result,
                columns=["PC1", "PC2"]
            )
            pca_df["departamento"] = cluster_df["departamento"].values
            pca_df["cluster"] = cluster_df["cluster"].values
            
            fig_pca = px.scatter(
                pca_df,
                x="PC1",
                y="PC2",
                color="cluster",
                text="departamento",
                title="Proyección PCA de Clusters Electorales"
            )
            
            fig_pca.update_traces(textposition="top center")
            fig_pca.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )
            
            st.plotly_chart(fig_pca, use_container_width=True)
            
            st.markdown("""
            ### 🧠 Interpretación Técnica
            
            - **Cluster 0**: Departamentos con baja participación electoral  
            - **Cluster 1**: Comportamiento mixto y transición  
            - **Cluster 2**: Alta participación y pluralidad política  
            
            🔍 *Análisis estadístico no predictivo, con fines académicos.*
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #FFFFFF; padding: 20px;">
    <p style="font-size: 1.2rem; text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9);"><b>✨ Desarrollado por Deiber Yesid López Ramírez - Data Analyst</b></p>
    <p style="text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9);">🇨🇴 Encuesta no oficial • Consulta fuentes oficiales arriba</p>
</div>
""", unsafe_allow_html=True)
