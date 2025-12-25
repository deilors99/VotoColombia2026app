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
    page_title="Voto Colombia 2026 🇨🇴", 
    page_icon="🗳️"
)

# CSS Ultra Mejorado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;700;900&display=swap');
    
    /* Fondo principal con patrón */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        position: relative;
    }
    
    /* Partículas de fondo animadas */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 215, 0, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(135, 206, 235, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(255, 165, 0, 0.06) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        animation: floatParticles 20s ease-in-out infinite;
    }
    
    @keyframes floatParticles {
        0%, 100% { transform: translate(0, 0); }
        25% { transform: translate(10px, -10px); }
        50% { transform: translate(-5px, 10px); }
        75% { transform: translate(15px, 5px); }
    }
    
    /* Títulos con efectos mejorados */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 25%, #FFD700 50%, #FFA500 75%, #FFD700 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        animation: shimmerTitle 3s linear infinite, float 3s ease-in-out infinite;
        letter-spacing: 4px !important;
        margin: 30px 0 !important;
        position: relative;
    }
    
    @keyframes shimmerTitle {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    h2 {
        font-family: 'Exo 2', sans-serif !important;
        background: linear-gradient(135deg, #87CEEB 0%, #4A90E2 50%, #87CEEB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        animation: shimmerTitle 4s linear infinite;
        letter-spacing: 2px !important;
    }
    
    h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #FFD700 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
        letter-spacing: 1px !important;
    }
    
    /* Botones mejorados con efecto 3D */
    .stButton>button {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(145deg, #FFD700, #FFA500) !important;
        color: black !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        padding: 18px 35px !important;
        font-size: 1.1rem !important;
        border: none !important;
        box-shadow: 
            0 8px 25px rgba(255, 215, 0, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.3),
            inset 0 -2px 0 rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button::before {
        content: '' !important;
        position: absolute !important;
        top: -50% !important;
        left: -50% !important;
        width: 200% !important;
        height: 200% !important;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent) !important;
        transform: rotate(45deg) !important;
        transition: all 0.6s !important;
    }
    
    .stButton>button:hover::before {
        left: 100% !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 15px 40px rgba(255, 215, 0, 0.6),
            inset 0 3px 0 rgba(255, 255, 255, 0.4),
            inset 0 -3px 0 rgba(0, 0, 0, 0.4) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 
            0 5px 15px rgba(255, 215, 0, 0.4),
            inset 0 2px 5px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Cards modernas con glassmorphism mejorado */
    .card-modern {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.08) 0%, 
            rgba(255, 255, 255, 0.03) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .card-modern::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.1) 0%, transparent 70%);
        animation: rotateGlow 10s linear infinite;
        pointer-events: none;
    }
    
    @keyframes rotateGlow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .card-modern:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 15px 50px rgba(255, 215, 0, 0.5),
            inset 0 2px 0 rgba(255, 255, 255, 0.2);
        border-color: #FFD700;
    }
    
    /* Métricas con diseño premium */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Exo 2', sans-serif !important;
        color: #87CEEB !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        text-shadow: 0 0 10px rgba(135, 206, 235, 0.3);
    }
    
    /* Inputs modernos */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        font-family: 'Exo 2', sans-serif !important;
        background: linear-gradient(145deg, rgba(45, 55, 72, 0.9), rgba(30, 40, 55, 0.95)) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        border: 2px solid rgba(135, 206, 235, 0.3) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 1rem !important;
        box-shadow: 
            inset 0 2px 5px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(135, 206, 235, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #FFD700 !important;
        box-shadow: 
            0 0 30px rgba(255, 215, 0, 0.4),
            inset 0 2px 5px rgba(0, 0, 0, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTextInput>label,
    .stSelectbox>label {
        font-family: 'Exo 2', sans-serif !important;
        color: #87CEEB !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        text-shadow: 0 0 10px rgba(135, 206, 235, 0.3) !important;
        text-transform: uppercase !important;
    }
    
    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.8), rgba(15, 20, 25, 0.9));
        backdrop-filter: blur(15px);
        padding: 15px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(145deg, rgba(45, 55, 72, 0.7), rgba(30, 40, 55, 0.9)) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        color: #87CEEB !important;
        font-weight: 700 !important;
        border: 2px solid rgba(135, 206, 235, 0.2) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #FFD700 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #FFD700, #FFA500) !important;
        color: black !important;
        font-weight: 900 !important;
        border: 2px solid #FFD700 !important;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.6) !important;
        transform: scale(1.05) !important;
    }
    
    /* Progress bar con estilo premium */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, 
            #FFD700 0%, 
            #FFA500 25%, 
            #FFD700 50%, 
            #FFA500 75%, 
            #FFD700 100%) !important;
        background-size: 200% auto !important;
        animation: shimmer 2s linear infinite !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6) !important;
        border-radius: 10px !important;
        height: 12px !important;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* Dataframe mejorado */
    .stDataFrame {
        background: rgba(30, 40, 55, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(135, 206, 235, 0.2) !important;
        font-family: 'Exo 2', sans-serif !important;
        overflow: hidden !important;
    }
    
    /* Sidebar mejorado */
    .stSidebar {
        background: linear-gradient(180deg, 
            rgba(26, 31, 46, 0.98) 0%, 
            rgba(15, 20, 25, 0.99) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 3px solid rgba(255, 215, 0, 0.3) !important;
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 20, 25, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border-radius: 10px;
        border: 2px solid rgba(15, 20, 25, 0.5);
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FFA500, #FFD700);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
    }
    
    /* Divider estilizado */
    hr {
        border: none !important;
        height: 3px !important;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 215, 0, 0.6), 
            transparent) !important;
        margin: 40px 0 !important;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* Banner de bienvenida mejorado */
    .welcome-banner {
        background: linear-gradient(135deg, 
            rgba(255, 215, 0, 0.1) 0%, 
            rgba(135, 206, 235, 0.1) 50%,
            rgba(255, 165, 0, 0.1) 100%);
        backdrop-filter: blur(30px);
        border-radius: 30px;
        padding: 80px 40px;
        border: 3px solid rgba(255, 215, 0, 0.4);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.6),
            inset 0 2px 0 rgba(255, 255, 255, 0.1);
        max-width: 900px;
        margin: 0 auto;
        animation: floatBanner 6s ease-in-out infinite;
    }
    
    @keyframes floatBanner {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    /* Efectos de entrada para elementos */
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Modal mejorado */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.95);
        backdrop-filter: blur(10px);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s ease-out;
    }
    
    .modal-content {
        background: linear-gradient(135deg, #1a1f2e 0%, #0f1419 100%);
        border-radius: 30px;
        padding: 60px;
        max-width: 700px;
        width: 90%;
        border: 3px solid #FFD700;
        box-shadow: 
            0 30px 100px rgba(255, 215, 0, 0.6),
            inset 0 2px 0 rgba(255, 255, 255, 0.1);
        animation: slideInFromBottom 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    @keyframes slideInFromBottom {
        from {
            transform: translateY(100vh) scale(0.8);
            opacity: 0;
        }
        to {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
    }
    
    /* Efecto de brillo en hover para links */
    a {
        transition: all 0.3s ease !important;
        position: relative !important;
    }
    
    a:hover {
        text-shadow: 0 0 15px currentColor !important;
    }
    
    /* Info boxes mejorados */
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 15px !important;
        padding: 20px !important;
        border-left: 5px solid !important;
        backdrop-filter: blur(10px) !important;
        animation: slideInLeft 0.4s ease-out !important;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# Datos
candidatos = [
    "Gustavo Petro (hipotético)", "Paloma Valencia", "Iván Cepeda",
    "Sergio Fajardo", "Vicky Dávila", "Abelardo de la Espriella",
    "David Luna", "Juan Daniel Oviedo", "Otro"
]

# Emojis para candidatos
candidatos_emoji = {
    "Gustavo Petro (hipotético)": "👤",
    "Paloma Valencia": "👤",
    "Iván Cepeda": "👤",
    "Sergio Fajardo": "👤",
    "Vicky Dávila": "👤",
    "Abelardo de la Espriella": "👤",
    "David Luna": "👤",
    "Juan Daniel Oviedo": "👤",
    "Otro": "❓"
}

# Inicializar estados
if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(
        columns=["candidato", "votos", "hora", "nombre", "ult5", "departamento"]
    )

if "show_vote_modal" not in st.session_state:
    st.session_state.show_vote_modal = False

def generar_hash(cedula):
    return hashlib.sha256(cedula.encode()).hexdigest()[:16]

# HEADER CON ANIMACIÓN
st.markdown("""
<div class="fade-in">
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 4rem; margin-bottom: 10px; animation: pulse 2s ease-in-out infinite;">🗳️</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("🇨🇴 VOTO COLOMBIA PRESIDENCIALES 2026")
st.markdown("### Encuesta Electoral Segura")
st.markdown("**Creador: Deiber Yesid López Ramírez - Data Analyst**")

# Badge de estado
total_actual = len(st.session_state.datos_votos)
st.markdown(f"""
<div style="text-align: center; margin: 20px 0;">
    <span style="
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 165, 0, 0.3));
        padding: 10px 30px;
        border-radius: 50px;
        border: 2px solid #FFD700;
        font-family: 'Orbitron', sans-serif;
        color: #FFD700;
        font-weight: bold;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
        animation: pulse 2s ease-in-out infinite;
    ">
        📊 {total_actual} VOTOS REGISTRADOS
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Enlaces Oficiales con diseño mejorado
st.markdown("### 📊 FUENTES OFICIALES DE ELECCIONES")
st.markdown("<div class='fade-in'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card-modern">
        <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">🏛️</div>
        <h4 style="color: #FFD700; text-align: center; font-family: 'Orbitron';">Registraduría</h4>
        <p style="text-align: center; color: #87CEEB; margin: 15px 0;">
            Portal oficial del Estado colombiano
        </p>
        <p style="text-align: center;">
            <a href="https://estadisticaselectorales.registraduria.gov.co/" target="_blank" 
               style="color: #FFD700; text-decoration: none; font-weight: bold;">
                📈 Ver Estadísticas →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card-modern">
        <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">👁️</div>
        <h4 style="color: #FFD700; text-align: center; font-family: 'Orbitron';">MOE</h4>
        <p style="text-align: center; color: #87CEEB; margin: 15px 0;">
            Misión de Observación Electoral
        </p>
        <p style="text-align: center;">
            <a href="https://moe.org.co/" target="_blank" 
               style="color: #FFD700; text-decoration: none; font-weight: bold;">
                🔍 Portal MOE →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card-modern">
        <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">📚</div>
        <h4 style="color: #FFD700; text-align: center; font-family: 'Orbitron';">CEDAE</h4>
        <p style="text-align: center; color: #87CEEB; margin: 15px 0;">
            Centro de Estudios en Democracia
        </p>
        <p style="text-align: center;">
            <a href="https://cedae.datasketch.co/" target="_blank" 
               style="color: #FFD700; text-decoration: none; font-weight: bold;">
                💾 Base de Datos →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# SIDEBAR MEJORADO
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 3rem; margin-bottom: 10px;">🗳️</div>
        <h2 style="font-family: 'Orbitron'; color: #FFD700; font-size: 1.5rem;">EMITE TU VOTO</h2>
        <p style="color: #87CEEB; font-size: 0.9rem;">Solo ciudadanos colombianos</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_voto_sidebar"):
        nombre = st.text_input("✍️ Nombre", placeholder="Tu nombre completo", key="nombre_sidebar")
        departamento = st.selectbox("📍 Departamento", [
            "Selecciona...", "Antioquia", "Atlántico", "Bogotá D.C.", 
            "Bolívar", "Boyacá", "Caldas", "Caquetá", "Cauca", "Cesar",
            "Córdoba", "Cundinamarca", "Huila", "La Guajira", "Magdalena",
            "Meta", "Nariño", "Norte de Santander", "Quindío", "Risaralda",
            "Santander", "Sucre", "Tolima", "Valle del Cauca"
        ], key="depto_sidebar")
        ult5 = st.text_input("🔢 Últimos 5 dígitos cédula", max_chars=5, type="password", key="cedula_sidebar")
        candidato = st.selectbox("🎯 Candidato", candidatos, key="candidato_sidebar")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅ VOTAR AHORA", use_container_width=True)
        
        if submitted:
            if not nombre or departamento == "Selecciona..." or len(ult5) != 5:
                st.error("❌ Completa todos los campos correctamente")
            elif not ult5.isdigit():
                st.error("❌ La cédula debe contener solo números")
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
    
    # Estadísticas del sidebar
    st.metric("📊 TOTAL VOTOS", len(st.session_state.datos_votos))
    
    if len(st.session_state.datos_votos) > 0:
        ultimo = st.session_state.datos_votos.iloc[-1]
        st.markdown(f"""
        <div style="
            background: rgba(135, 206, 235, 0.1);
            padding: 15px;
            border-radius: 10px;
            border-left: 3px solid #87CEEB;
            margin-top: 15px;
        ">
            <p style="color: #87CEEB; margin: 0; font-size: 0.8rem;">🕐 Último voto</p>
            <p style="color: white; margin: 5px 0 0 0; font-weight: bold;">
                {ultimo['hora'].strftime('%H:%M:%S')}
            </p>
        </div>
        """, unsafe_allow_html=True)

# CONTENIDO PRINCIPAL
if st.session_state.datos_votos.empty:
    # PANTALLA DE BIENVENIDA MEJORADA
    st.markdown("""
    <div class="welcome-banner" style="text-align: center; padding: 100px 20px; margin: 50px 0;">
        <div style="font-size: 6rem; margin-bottom: 30px; animation: float 3s ease-in-out infinite;">🗳️</div>
        <h2 style="
            font-family: 'Orbitron', sans-serif;
            color: #FFD700;
            font-size: 3.5rem;
            margin-bottom: 20px;
            text-shadow: 0 0 40px rgba(255, 215, 0, 0.6);
            animation: shimmerTitle 3s linear infinite;
        ">¡Inicia la Encuesta Electoral!</h2>
        <p style="
            font-family: 'Exo 2', sans-serif;
            color: #87CEEB;
            font-size: 1.8rem;
            margin-bottom: 20px;
        ">Sé el primero en hacer historia</p>
        <p style="
            color: #9CA3AF;
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        ">
            Tu opinión cuenta. Participa en esta encuesta electoral no oficial 
            y conoce las tendencias de opinión en Colombia 🇨🇴
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón grande centrado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 EMITIR MI VOTO AHORA", use_container_width=True, key="btn_iniciar_voto"):
            st.session_state.show_vote_modal = True
            st.rerun()
    
    # Características destacadas
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    
    with col_feat1:
        st.markdown("""
        <div class="card-modern" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 15px;">🔒</div>
            <h4 style="color: #FFD700;">Seguro</h4>
            <p style="color: #87CEEB; font-size: 0.9rem;">
                Un voto por cédula garantiza transparencia
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat2:
        st.markdown("""
        <div class="card-modern" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 15px;">⚡</div>
            <h4 style="color: #FFD700;">Instantáneo</h4>
            <p style="color: #87CEEB; font-size: 0.9rem;">
                Resultados en tiempo real con análisis avanzado
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat3:
        st.markdown("""
        <div class="card-modern" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 15px;">📊</div>
            <h4 style="color: #FFD700;">Analítico</h4>
            <p style="color: #87CEEB; font-size: 0.9rem;">
                Machine Learning y visualizaciones interactivas
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # MODAL DE VOTACIÓN
    if st.session_state.show_vote_modal:
        modal_container = st.container()
        
        with modal_container:
            col_modal1, col_modal2, col_modal3 = st.columns([1, 3, 1])
            
            with col_modal2:
                st.markdown("""
                <div style="text-align: center; margin-bottom: 40px;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🗳️</div>
                    <h2 style="
                        font-family: 'Orbitron', sans-serif;
                        color: #FFD700;
                        font-size: 2.5rem;
                        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
                        margin-bottom: 10px;
                    ">FORMULARIO DE VOTACIÓN</h2>
                    <p style="color: #87CEEB; font-size: 1.2rem;">Completa tus datos para emitir tu voto</p>
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
    # RESULTADOS CUANDO HAY VOTOS
    resumen = (st.session_state.datos_votos
               .groupby("candidato")["votos"]
               .sum()
               .reset_index()
               .sort_values("votos", ascending=False))
    total = resumen["votos"].sum()
    resumen["porcentaje"] = (resumen["votos"] / total * 100).round(2)
    
    # Tabs principales con diseño mejorado
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 RESULTADOS",
        "📈 ANÁLISIS",
        "📋 DATOS",
        "🧠 MACHINE LEARNING"
    ])
    
    with tab1:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        
        # Métricas principales con cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="card-modern" style="text-align: center;">', unsafe_allow_html=True)
            st.metric("🥇 LÍDER", resumen.iloc[0]["candidato"], f"{resumen.iloc[0]['porcentaje']}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card-modern" style="text-align: center;">', unsafe_allow_html=True)
            st.metric("📊 TOTAL", total)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="card-modern" style="text-align: center;">', unsafe_allow_html=True)
            if len(resumen) > 1:
                dif = resumen.iloc[0]["porcentaje"] - resumen.iloc[1]["porcentaje"]
                st.metric("📉 DIFERENCIA", f"{dif:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="card-modern" style="text-align: center;">', unsafe_allow_html=True)
            deptos = st.session_state.datos_votos["departamento"].nunique()
            st.metric("🗺️ DEPARTAMENTOS", deptos)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Gráficos principales
        col_l, col_r = st.columns(2)
        
        with col_l:
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.subheader("🏆 RANKING ELECTORAL")
            
            for idx, row in resumen.iterrows():
                emoji = candidatos_emoji.get(row['candidato'], "👤")
                
                st.markdown(f"""
                <div style="margin: 20px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-family: 'Exo 2'; font-weight: bold; font-size: 1.1rem; color: white;">
                            <span style="color: #FFD700; font-size: 1.5rem;">#{idx + 1}</span> {emoji} {row['candidato']}
                        </span>
                        <span style="font-family: 'Orbitron'; font-weight: bold; font-size: 1.3rem; color: #FFD700;">
                            {row['porcentaje']}%
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.progress(row['porcentaje']/100)
                st.caption(f"✓ {row['votos']} votos")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_r:
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.subheader("📊 DISTRIBUCIÓN DE VOTOS")
            
            fig = px.pie(
                resumen, 
                values='votos', 
                names='candidato',
                hole=0.6,
                color_discrete_sequence=px.colors.sequential.Sunset
            )
            
            fig.update_traces(
                textposition='outside',
                textinfo='label+percent',
                textfont_size=12
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Exo 2'),
                height=500,
                showlegend=False,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        st.markdown('<div class="card-modern">', unsafe_allow_html=True)
        
        st.subheader("📈 ANÁLISIS COMPARATIVO")
        
        fig_bar = px.bar(
            resumen,
            x='votos',
            y='candidato',
            orientation='h',
            color='porcentaje',
            color_continuous_scale='Sunset',
            text='porcentaje'
        )
        
        fig_bar.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            textfont=dict(size=14, family='Orbitron', color='white')
        )
        
        fig_bar.update_layout(
            yaxis={'categoryorder':'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Exo 2'),
            showlegend=False,
            height=500,
            xaxis=dict(gridcolor='rgba(255, 215, 0, 0.1)'),
            yaxis=dict(gridcolor='rgba(255, 215, 0, 0.1)')
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Análisis por departamento
        if len(st.session_state.datos_votos) > 0:
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.subheader("🗺️ PARTICIPACIÓN POR DEPARTAMENTO")
            
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
                color_continuous_scale='Tealgrn',
                title='Top 10 Departamentos con Mayor Participación'
            )
            
            fig_dep.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Exo 2'),
                showlegend=False,
                height=400,
                xaxis=dict(gridcolor='rgba(135, 206, 235, 0.1)'),
                yaxis=dict(gridcolor='rgba(135, 206, 235, 0.1)')
            )
            
            st.plotly_chart(fig_dep, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        st.markdown('<div class="card-modern">', unsafe_allow_html=True)
        
        st.subheader("📋 REGISTRO COMPLETO DE VOTACIÓN")
        
        datos_mostrar = st.session_state.datos_votos[['nombre', 'candidato', 'departamento', 'hora']].copy()
        datos_mostrar['hora'] = datos_mostrar['hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Renombrar columnas para mejor presentación
        datos_mostrar.columns = ['Nombre', 'Candidato', 'Departamento', 'Fecha y Hora']
        
        st.dataframe(
            datos_mostrar,
            use_container_width=True,
            height=400
        )
        
        # Estadísticas adicionales
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        
        with col_stats1:
            st.metric("👥 Total Votantes", len(datos_mostrar))
        
        with col_stats2:
            candidatos_unicos = datos_mostrar['Candidato'].nunique()
            st.metric("🎯 Candidatos Votados", candidatos_unicos)
        
        with col_stats3:
            deptos_unicos = datos_mostrar['Departamento'].nunique()
            st.metric("🗺️ Departamentos", deptos_unicos)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón de descarga
        csv = st.session_state.datos_votos[['nombre', 'candidato', 'departamento', 'hora']].to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar Base de Datos Completa (CSV)",
            data=csv,
            file_name=f'votos_colombia_2026_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 3rem; margin-bottom: 15px;">🧠</div>
            <h2 style="font-family: 'Orbitron'; color: #FFD700;">ANÁLISIS AVANZADO CON MACHINE LEARNING</h2>
            <p style="color: #87CEEB; font-size: 1.1rem;">Clustering y análisis predictivo de comportamiento electoral</p>
        </div>
        """, unsafe_allow_html=True)
        
        if len(st.session_state.datos_votos) < 10:
            st.warning("⚠️ Se necesitan al menos 10 votos para realizar análisis de Machine Learning")
        else:
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            
            # Dataset para ML
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
            st.dataframe(cluster_df, use_container_width=True)
            
            # Normalización
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(
                cluster_df[["total_votos", "diversidad_candidatos"]]
            )
            
            # K-Means
            n_clusters = min(3, len(cluster_df))
            
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init=10
            )
            cluster_df["cluster"] = kmeans.fit_predict(X_scaled)
            
            # Métricas
            col_ml1, col_ml2, col_ml3 = st.columns(3)
            
            with col_ml1:
                if n_clusters > 1:
                    score = silhouette_score(X_scaled, cluster_df["cluster"])
                    st.metric("📐 Silhouette Score", f"{score:.3f}")
            
            with col_ml2:
                st.metric("🔢 Clusters Identificados", n_clusters)
            
            with col_ml3:
                st.metric("📊 Departamentos Analizados", len(cluster_df))
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Visualización de clusters
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.markdown("### 🎯 Clustering de Departamentos")
            
            fig_cluster = px.scatter(
                cluster_df,
                x="total_votos",
                y="diversidad_candidatos",
                color="cluster",
                text="departamento",
                size="total_votos",
                color_continuous_scale="Viridis",
                labels={
                    "total_votos": "Total de Votos",
                    "diversidad_candidatos": "Diversidad de Candidatos",
                    "cluster": "Cluster"
                },
                title="Análisis de Comportamiento Electoral por Departamento"
            )
            
            fig_cluster.update_traces(textposition="top center", textfont_size=10)
            fig_cluster.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", family='Exo 2'),
                height=500
            )
            
            st.plotly_chart(fig_cluster, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # PCA
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.markdown("### 🔬 Análisis de Componentes Principales (PCA)")
            
            pca = PCA(n_components=2)
            pca_result = pca.fit_transform(X_scaled)
            
            pca_df = pd.DataFrame(
                pca_result,
                columns=["Componente Principal 1", "Componente Principal 2"]
            )
            pca_df["departamento"] = cluster_df["departamento"].values
            pca_df["cluster"] = cluster_df["cluster"].values
            
            fig_pca = px.scatter(
                pca_df,
                x="Componente Principal 1",
                y="Componente Principal 2",
                color="cluster",
                text="departamento",
                title="Reducción Dimensional - Proyección PCA",
                color_continuous_scale="Plasma"
            )
            
            fig_pca.update_traces(textposition="top center", textfont_size=10)
            fig_pca.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", family='Exo 2'),
                height=500
            )
            
            st.plotly_chart(fig_pca, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Interpretación
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.markdown("""
            ### 🧠 Interpretación de Resultados
            
            Los clusters identificados representan diferentes patrones de comportamiento electoral:
            
            - **🔴 Cluster 0**: Departamentos con **baja participación electoral** y menor diversidad de preferencias
            - **🟡 Cluster 1**: Comportamiento **mixto y de transición**, participación moderada
            - **🟢 Cluster 2**: **Alta participación** electoral con mayor pluralidad política
            
            ---
            
            #### 📊 Metodología Aplicada:
            
            1. **K-Means Clustering**: Algoritmo no supervisado para identificar patrones
            2. **Normalización StandardScaler**: Estandarización de variables para comparación
            3. **PCA**: Reducción dimensional para visualización mejorada
            4. **Silhouette Score**: Métrica de calidad del clustering (0 a 1)
            
            ---
            
            🔍 **Nota Importante**: Este es un análisis estadístico descriptivo con fines académicos y de investigación. 
            No constituye una predicción electoral ni tiene valor oficial.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer mejorado
st.markdown("---")
st.markdown("""
<div style="
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.08), rgba(135, 206, 235, 0.08));
    border-radius: 20px;
    margin-top: 50px;
    backdrop-filter: blur(10px);
">
    <div style="font-size: 2rem; margin-bottom: 20px;">✨</div>
    <p style="
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3rem;
        color: #FFD700;
        margin: 10px 0;
        letter-spacing: 2px;
        font-weight: bold;
    ">
        DESARROLLADO POR DEIBER YESID LÓPEZ RAMÍREZ
    </p>
    <p style="
        font-family: 'Exo 2', sans-serif;
        color: #87CEEB;
        margin: 5px 0;
        font-size: 1.1rem;
    ">
        📊 Data Analyst • 🇨🇴 Colombia • 🚀 Tech Innovator
    </p>
    <p style="
        color: #9CA3AF;
        font-size: 0.95rem;
        margin: 15px 0 5px 0;
        line-height: 1.6;
    ">
        📧 Encuesta no oficial con fines académicos y demostrativos<br>
        Consulta las fuentes oficiales arriba para información electoral verificada
    </p>
    <p style="
        font-family: 'Exo 2', sans-serif;
        color: #FFD700;
        font-size: 0.85rem;
        margin: 10px 0 0 0;
    ">
        🔗 Datos comparables con: Registraduría Nacional | MOE | CEDAE
    </p>
</div>
""", unsafe_allow_html=True)
