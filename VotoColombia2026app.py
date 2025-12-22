import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib
import base64

# Configuración de página
st.set_page_config(
    layout="wide", 
    page_title="Voto Colombia 2026 🇨🇴", 
    page_icon="🗳️",
    initial_sidebar_state="expanded"
)

# CSS Ultra Moderno con Efectos Metalizados
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;700&display=swap');
    
    /* Fondo principal con efecto metálico */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #e0e0e0;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Efecto de partículas metálicas de fondo */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(135, 206, 235, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Slider de fondo */
    .slider-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
    }
    
    .slider-image {
        position: absolute;
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0;
        transition: opacity 2s ease-in-out;
        filter: brightness(0.4) blur(2px);
    }
    
    .slider-image.active {
        opacity: 1;
    }
    
    /* Sidebar con efecto metálico */
    .stSidebar {
        background: linear-gradient(180deg, 
            rgba(26, 31, 46, 0.95) 0%, 
            rgba(15, 20, 25, 0.98) 100%);
        backdrop-filter: blur(20px);
        border-right: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Títulos con efecto metálico brillante */
    h1 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 25%, #ffd700 50%, #f9a825 75%, #ffd700 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        animation: shimmer 3s linear infinite;
        letter-spacing: 3px;
        margin: 20px 0 !important;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    h2 {
        font-family: 'Exo 2', sans-serif;
        background: linear-gradient(135deg, #87CEEB 0%, #4A90E2 50%, #87CEEB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 2.5rem !important;
        font-weight: 700;
        animation: shimmer 4s linear infinite;
        letter-spacing: 2px;
    }
    
    h3 {
        font-family: 'Orbitron', sans-serif;
        color: #FFD700;
        font-size: 1.8rem !important;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        letter-spacing: 1px;
    }
    
    /* Botones con efecto metálico 3D */
    .stButton>button {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(145deg, #ffd700, #ffb300);
        color: #000;
        font-weight: 900;
        border-radius: 15px;
        border: none;
        padding: 18px 35px;
        font-size: 1.2rem;
        letter-spacing: 2px;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 8px 25px rgba(255, 215, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3),
            inset 0 -1px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transform: rotate(45deg);
        transition: all 0.6s;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 15px 40px rgba(255, 215, 0, 0.6),
            inset 0 2px 0 rgba(255, 255, 255, 0.4),
            inset 0 -2px 0 rgba(0, 0, 0, 0.4);
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 
            0 5px 15px rgba(255, 215, 0, 0.4),
            inset 0 2px 5px rgba(0, 0, 0, 0.3);
    }
    
    /* Mensajes con efecto glassmorphism */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 255, 127, 0.2), rgba(0, 200, 100, 0.3));
        backdrop-filter: blur(15px);
        border: 2px solid rgba(0, 255, 127, 0.4);
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 255, 127, 0.3);
        animation: slideInRight 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Exo 2', sans-serif;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 50, 50, 0.2), rgba(200, 0, 0, 0.3));
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 50, 50, 0.4);
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(255, 50, 50, 0.3);
        animation: shake 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Exo 2', sans-serif;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(135, 206, 235, 0.2), rgba(74, 144, 226, 0.3));
        backdrop-filter: blur(15px);
        border: 2px solid rgba(135, 206, 235, 0.4);
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(135, 206, 235, 0.3);
        animation: slideInLeft 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Exo 2', sans-serif;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Métricas con efecto neomorphism */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Exo 2', sans-serif;
        color: #87CEEB !important;
        font-size: 1.3rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Inputs con efecto futurista */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background: linear-gradient(145deg, rgba(45, 55, 72, 0.8), rgba(30, 40, 55, 0.9));
        backdrop-filter: blur(10px);
        color: white;
        border: 2px solid rgba(135, 206, 235, 0.3);
        border-radius: 12px;
        padding: 15px;
        font-family: 'Exo 2', sans-serif;
        font-size: 1.1rem;
        box-shadow: 
            inset 0 2px 5px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(135, 206, 235, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #FFD700;
        box-shadow: 
            0 0 30px rgba(255, 215, 0, 0.4),
            inset 0 2px 5px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    .stTextInput>label, .stSelectbox>label {
        font-family: 'Exo 2', sans-serif;
        color: #87CEEB !important;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(135, 206, 235, 0.3);
    }
    
    /* Progress bar con efecto metálico */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, 
            #FFD700 0%, 
            #FFA500 25%, 
            #FFD700 50%, 
            #FFA500 75%, 
            #FFD700 100%);
        background-size: 200% auto;
        animation: shimmer 2s linear infinite;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
        border-radius: 10px;
    }
    
    /* Tabs con efecto metálico */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(15, 20, 25, 0.5);
        backdrop-filter: blur(10px);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(145deg, rgba(45, 55, 72, 0.6), rgba(30, 40, 55, 0.8));
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 15px 25px;
        color: #87CEEB;
        font-weight: 700;
        border: 2px solid rgba(135, 206, 235, 0.2);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #FFD700;
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #FFD700, #FFA500);
        color: black;
        font-weight: 900;
        border: 2px solid #FFD700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
        transform: scale(1.05);
    }
    
    /* Cards metálicas con glassmorphism */
    .glass-card {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.05) 0%, 
            rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid rgba(255, 215, 0, 0.2);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(
            circle,
            rgba(255, 215, 0, 0.1) 0%,
            transparent 70%
        );
        animation: rotate 10s linear infinite;
        pointer-events: none;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 15px 50px rgba(255, 215, 0, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.2);
        border-color: #FFD700;
    }
    
    /* Enlaces oficiales con efecto hover */
    .official-link {
        display: inline-block;
        font-family: 'Exo 2', sans-serif;
        background: linear-gradient(145deg, rgba(74, 85, 104, 0.8), rgba(45, 55, 72, 0.9));
        backdrop-filter: blur(10px);
        color: #FFD700;
        padding: 12px 25px;
        border-radius: 12px;
        text-decoration: none;
        margin: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid #FFD700;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .official-link::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .official-link:hover::before {
        left: 100%;
    }
    
    .official-link:hover {
        background: linear-gradient(145deg, #FFD700, #FFA500);
        color: black;
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 40px rgba(255, 215, 0, 0.5);
    }
    
    /* Galería de imágenes */
    .image-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .gallery-item {
        position: relative;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.4s ease;
        border: 2px solid rgba(255, 215, 0, 0.3);
    }
    
    .gallery-item:hover {
        transform: scale(1.05) translateY(-10px);
        box-shadow: 0 20px 50px rgba(255, 215, 0, 0.4);
        border-color: #FFD700;
    }
    
    .gallery-item img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        transition: all 0.4s ease;
    }
    
    .gallery-item:hover img {
        transform: scale(1.1);
        filter: brightness(1.2);
    }
    
    .gallery-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0, 0, 0, 0.9), transparent);
        color: white;
        padding: 20px;
        transform: translateY(100%);
        transition: transform 0.4s ease;
    }
    
    .gallery-item:hover .gallery-overlay {
        transform: translateY(0);
    }
    
    /* Dataframe mejorado */
    .dataframe {
        background: rgba(30, 40, 55, 0.8) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 2px solid rgba(135, 206, 235, 0.2);
        font-family: 'Exo 2', sans-serif;
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 20, 25, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FFA500, #FFD700);
    }
    
    /* Efectos de carga */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 215, 0, 0.8); }
    }
    
    .loading {
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Divider personalizado */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 215, 0, 0.5), 
            transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript para el slider de fondo
st.markdown("""
<script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slider-image');
    
    function showSlide(n) {
        slides.forEach(slide => slide.classList.remove('active'));
        currentSlide = (n + slides.length) % slides.length;
        slides[currentSlide].classList.add('active');
    }
    
    function nextSlide() {
        showSlide(currentSlide + 1);
    }
    
    // Cambiar slide cada 5 segundos
    setInterval(nextSlide, 5000);
    
    // Mostrar primera imagen
    if(slides.length > 0) {
        slides[0].classList.add('active');
    }
</script>
""", unsafe_allow_html=True)

# Lista de candidatos
candidatos = [
    "Iván Cepeda",
    "Paloma Valencia",
    "Gustavo Petro (hipotético)",
    "Sergio Fajardo",
    "Vicky Dávila",
    "Abelardo de la Espriella",
    "David Luna",
    "Juan Daniel Oviedo",
    "Otro"
]

# Inicializar estado de sesión
if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(
        columns=["candidato", "votos", "hora", "hash_id", "nombre", "ult5", "departamento"]
    )

# Función para generar hash único
def generar_hash(cedula):
    return hashlib.sha256(cedula.encode()).hexdigest()[:16]

# Slider de fondo con imágenes
st.markdown("""
<div class="slider-container">
    <img class="slider-image active" src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=1920&q=80" alt="Colombia">
    <img class="slider-image" src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=1920&q=80" alt="Voting">
    <img class="slider-image" src="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=1920&q=80" alt="Democracy">
    <img class="slider-image" src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=1920&q=80" alt="Colombia Flag">
</div>
""", unsafe_allow_html=True)

# Header principal con efectos
col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
with col_header2:
    st.markdown("<h1>🇨🇴 VOTO COLOMBIA PRESIDENCIALES 2026</h1>", unsafe_allow_html=True)
    st.markdown("<h2>ENCUESTA ELECTORAL SEGURA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #87CEEB; font-family: Exo 2; font-size: 1.2rem; letter-spacing: 1px;'><b>Creador: Deiber Yesid López Ramírez - Data Analyst</b></p>", unsafe_allow_html=True)

# Banner de enlaces oficiales con efecto glassmorphism
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>📊 FUENTES OFICIALES DE ELECCIONES EN COLOMBIA</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #FFD700; font-family: 'Orbitron'; text-align: center; font-size: 1.5rem;">🏛️ REGISTRADURÍA NACIONAL</h4>
        <p style="font-size: 0.95rem; text-align: center; color: #87CEEB; font-family: 'Exo 2';">Sistema oficial de resultados electorales</p>
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://estadisticaselectorales.registraduria.gov.co/" target="_blank" class="official-link">
                📈 Estadísticas
            </a>
            <a href="https://resultados.registraduria.gov.co/" target="_blank" class="official-link">
                🗳️ Resultados
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #FFD700; font-family: 'Orbitron'; text-align: center; font-size: 1.5rem;">👁️ MISIÓN DE OBSERVACIÓN (MOE)</h4>
        <p style="font-size: 0.95rem; text-align: center; color: #87CEEB; font-family: 'Exo 2';">Observación independiente y transparente</p>
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://moe.org.co/" target="_blank" class="official-link">
                🔍 Portal MOE
            </a>
            <a href="https://moe.org.co/datos-electorales/" target="_blank" class="official-link">
                📊 Datos
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #FFD700; font-family: 'Orbitron'; text-align: center; font-size: 1.5rem;">📚 CENTRO DE ESTUDIOS (CEDAE)</h4>
        <p style="font-size: 0.95rem; text-align: center; color: #87CEEB; font-family: 'Exo 2';">Análisis histórico y comparativo</p>
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://cedae.datasketch.co/datos-democracia/resultados-electorales/explora-los-datos/" target="_blank" class="official-link">
                💾 Base Datos
            </a>
            <a href="https://observatorio.registraduria.gov.co/views/electoral/historicos-resultados.php" target="_blank" class="official-link">
                📖 Histórico
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Galería de imágenes - ESPACIO PARA TUS IMÁGENES
st.markdown("<h3 style='text-align: center; margin-top: 40px;'>📸 GALERÍA ELECTORAL COLOMBIA</h3>", unsafe_allow_html=True)
st.markdown("""
<div class="image-gallery">
    <div class="gallery-item">
        <img src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=400&q=80" alt="Bandera Colombia">
        <div class="gallery-overlay">
            <h4 style="margin: 0; font-family: 'Orbitron';">🇨🇴 Colombia Unida</h4>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem;">Tu voz, tu futuro</p>
        </div>
    </div>
    <div class="gallery-item">
        <img src="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=400&q=80" alt="Votación">
        <div class="gallery-overlay">
            <h4 style="margin: 0; font-family: 'Orbitron';">🗳️ Democracia</h4>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem;">Cada voto cuenta</p>
        </div>
    </div>
    <div class="gallery-item">
        <img src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=400&q=80" alt="Colombia">
        <div class="gallery-overlay">
            <h4 style="margin: 0; font-family: 'Orbitron';">🏛️ Elecciones 2026</h4>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem;">Construyendo el futuro</p>
        </div>
    </div>
    <div class="gallery-item">
        <img src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=400&q=80" alt="Participación">
        <div class="gallery-overlay">
            <h4 style="margin: 0; font-family: 'Orbitron';">✊ Participación</h4>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem;">Juntos por Colombia</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar para votación
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>🗳️ EMITE TU VOTO</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #87CEEB; font-family: Exo 2;'>Solo ciudadanos colombianos</p>", unsafe_allow_html=True)
    
    with st.form("formulario_voto", clear_on_submit=True):
        nombre = st.text_input(
            "✍️ Nombre Completo",
            placeholder="Ingresa tu nombre",
            max_chars=100
        )
        
        departamento = st.selectbox(
            "📍 Departamento",
            ["Selecciona...", "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", 
             "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó",
             "Córdoba", "Cundinamarca", "Guainía", "Guaviare", "Huila", "La Guajira",
             "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo", "Quindío",
             "Risaralda", "San Andrés y Providencia", "Santander", "Sucre", "Tolima",
             "Valle del Cauca", "Vaupés", "Vichada", "Bogotá D.C."]
        )
        
        ult5 = st.text_input(
            "🔢 Últimos 5 dígitos de cédula",
            placeholder="12345",
            max_chars=5,
            type="password"
        )
        
        seleccion = st.selectbox(
            "🎯 Candidato de tu preferencia",
            candidatos
        )
        
        submitted = st.form_submit_button("✅ VOTAR AHORA", use_container_width=True)
        
        if submitted:
            if not nombre.strip():
                st.error("❌ Por favor ingresa tu nombre")
            elif departamento == "Selecciona...":
                st.error("❌ Por favor selecciona tu departamento")
            elif not ult5.strip() or not ult5.isdigit() or len(ult5) != 5:
                st.error("❌ Ingresa exactamente 5 dígitos numéricos")
            elif ult5 in st.session_state.datos_votos["ult5"].values:
                st.error("❌ Esta cédula ya votó. Un voto por persona.")
            else:
                hash_id = generar_hash(ult5)
                nuevo_voto = pd.DataFrame({
                    "candidato": [seleccion],
                    "votos": [1],
                    "hora": [datetime.now()],
                    "hash_id": [hash_id],
                    "nombre": [nombre.strip()],
                    "ult5": [ult5],
                    "departamento": [departamento]
                })
                
                st.session_state.datos_votos = pd.concat(
                    [st.session_state.datos_votos, nuevo_voto], 
                    ignore_index=True
                )
                st.success("✅ ¡Voto registrado exitosamente! 🇨🇴")
                st.balloons()
                st.rerun()
    
    st.divider()
    total_votos = len(st.session_state.datos_votos)
    st.metric("📊 TOTAL VOTOS", total_votos)
    
    if total_votos > 0:
        ultimo_voto = st.session_state.datos_votos.iloc[-1]
        st.info(f"🕐 Último voto: {ultimo_voto['hora'].strftime('%H:%M:%S')}")

# Contenido principal
if st.session_state.datos_votos.empty:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 60px;">
        <h3 style="font-size: 3rem; margin-bottom: 20px;">🗳️</h3>
        <h3 style="color: #FFD700;">¡SÉ EL PRIMERO EN VOTAR!</h3>
        <p style="font-size: 1.3rem; color: #87CEEB; font-family: 'Exo 2';">Inicia la encuesta electoral colombiana</p>
    </div>
    """, unsafe_allow_html=True)
else:
    resumen = (st.session_state.datos_votos
               .groupby("candidato")["votos"]
               .sum()
               .reset_index()
               .sort_values("votos", ascending=False))
    
    total = resumen["votos"].sum()
    resumen["porcentaje"] = (resumen["votos"] / total * 100).round(2)
    
    # Tabs ultra modernos
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 RESULTADOS", 
        "📈 ANÁLISIS", 
        "🗺️ POR REGIÓN", 
        "📋 DATOS",
        "🔗 COMPARAR OFICIAL"
    ])
    
    with tab1:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
            """, unsafe_allow_html=True)
            st.metric(
                "🥇 LÍDER",
                resumen.iloc[0]["candidato"],
                f"{resumen.iloc[0]['porcentaje']}%"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
            """, unsafe_allow_html=True)
            st.metric("📊 TOTAL VOTOS", total)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
            """, unsafe_allow_html=True)
            if len(resumen) > 1:
                diferencia = resumen.iloc[0]["porcentaje"] - resumen.iloc[1]["porcentaje"]
                st.metric("📉 DIFERENCIA", f"{diferencia:.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
            """, unsafe_allow_html=True)
            if 'departamento' in st.session_state.datos_votos.columns:
                departamentos_unicos = st.session_state.datos_votos["departamento"].nunique()
                st.metric("🗺️ DEPARTAMENTOS", departamentos_unicos)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("""
            <div class="glass-card">
                <h3 style='text-align: center;'>🏆 RANKING ELECTORAL</h3>
            """, unsafe_allow_html=True)
            
            for idx, row in resumen.iterrows():
                st.markdown(f"""
                <div style="margin: 20px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-family: 'Exo 2'; font-weight: bold; font-size: 1.1rem; color: white;">
                            <span style="color: #FFD700; font-size: 1.3rem;">#{idx + 1}</span> {row['candidato']}
                        </span>
                        <span style="font-family: 'Orbitron'; font-weight: bold; font-size: 1.2rem; color: #FFD700;">
                            {row['porcentaje']}%
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(row['porcentaje']/100)
                st.markdown(f"""
                    <p style="text-align: right; color: #87CEEB; font-family: 'Exo 2'; margin: 5px 0;">
                        {row['votos']} votos
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_right:
            st.markdown("""
            <div class="glass-card">
                <h3 style='text-align: center;'>📊 DISTRIBUCIÓN DE VOTOS</h3>
            """, unsafe_allow_html=True)
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=resumen['candidato'],
                values=resumen['votos'],
                hole=.6,
                marker=dict(
                    colors=['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', 
                            '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'],
                    line=dict(color='#1a1f2e', width=3)
                ),
                textinfo='label+percent',
                textfont=dict(size=14, family='Exo 2', color='white'),
                hovertemplate='<b>%{label}</b><br>Votos: %{value}<br>Porcentaje: %{percent}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Exo 2'),
                height=450,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="glass-card">
            <h3 style='text-align: center;'>📈 ANÁLISIS COMPARATIVO</h3>
        """, unsafe_allow_html=True)
        
        fig_bar = px.bar(
            resumen,
            x='votos',
            y='candidato',
            orientation='h',
            color='porcentaje',
            color_continuous_scale=['#4ECDC4', '#FFD700', '#FF6B6B'],
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
            height=500,
            showlegend=False,
            xaxis=dict(gridcolor='rgba(255, 215, 0, 0.1)'),
            yaxis=dict(gridcolor='rgba(255, 215, 0, 0.1)')
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h3 style='text-align: center;'>⏰ EVOLUCIÓN TEMPORAL</h3>
        """, unsafe_allow_html=True)
        
        votos_tiempo = st.session_state.datos_votos.copy()
        votos_tiempo['hora_redondeada'] = votos_tiempo['hora'].dt.floor('5min')
        votos_acumulados = votos_tiempo.groupby('hora_redondeada').size().cumsum()
        
        fig_time = go.Figure()
        fig_time.add_trace(go.Scatter(
            x=votos_acumulados.index,
            y=votos_acumulados.values,
            mode='lines+markers',
            line=dict(color='#FFD700', width=4, shape='spline'),
            marker=dict(size=8, color='#FFA500', line=dict(color='#FFD700', width=2)),
            fill='tozeroy',
            fillcolor='rgba(255, 215, 0, 0.2)',
            name='Votos Acumulados'
        ))
        
        fig_time.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Exo 2'),
            height=400,
            xaxis=dict(gridcolor='rgba(255, 215, 0, 0.1)', title='Hora'),
            yaxis=dict(gridcolor='rgba(255, 215, 0, 0.1)', title='Votos Acumulados'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_time, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="glass-card">
            <h3 style='text-align: center;'>🗺️ ANÁLISIS POR DEPARTAMENTO</h3>
        """, unsafe_allow_html=True)
        
        if 'departamento' in st.session_state.datos_votos.columns:
            votos_depto = (st.session_state.datos_votos
                          .groupby('departamento')
                          .size()
                          .reset_index(name='total_votos')
                          .sort_values('total_votos', ascending=False))
            
            col_map1, col_map2 = st.columns(2)
            
            with col_map1:
                fig_depto = px.bar(
                    votos_depto.head(10),
                    x='total_votos',
                    y='departamento',
                    orientation='h',
                    color='total_votos',
                    color_continuous_scale=['#4ECDC4', '#FFD700', '#FFA500']
                )
                
                fig_depto.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', family='Exo 2'),
                    height=400,
                    showlegend=False,
                    title=dict(text='Top 10 Departamentos', font=dict(color='#FFD700', size=16)),
                    xaxis=dict(gridcolor='rgba(255, 215, 0, 0.1)'),
                    yaxis=dict(gridcolor='rgba(255, 215, 0, 0.1)')
                )
                
                st.plotly_chart(fig_depto, use_container_width=True)
            
            with col_map2:
                lider_depto = (st.session_state.datos_votos
                              .groupby(['departamento', 'candidato'])
                              .size()
                              .reset_index(name='votos'))
                
                idx = lider_depto.groupby('departamento')['votos'].idxmax()
                lideres = lider_depto.loc[idx].sort_values('votos', ascending=False).head(10)
                
                st.markdown("<h4 style='color: #FFD700; font-family: Orbitron;'>🏆 Líder por Departamento</h4>", unsafe_allow_html=True)
                for _, row in lideres.iterrows():
                    st.markdown(f"""
                    <div style="background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #FFD700;">
                        <strong style="color: #FFD700; font-family: 'Orbitron';">{row['departamento']}</strong><br>
                        <span style="color: #87CEEB; font-family: 'Exo 2';">{row['candidato']} ({row['votos']} votos)</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="glass-card">
            <h3 style='text-align: center;'>📋 BASE DE DATOS DE VOTOS</h3>
        """, unsafe_allow_html=True)
        
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            filtro_candidato = st.multiselect(
                "🎯 Filtrar por candidato",
                options=candidatos,
                default=candidatos
            )
        
        with col_filter2:
            if 'departamento' in st.session_state.datos_votos.columns:
                deptos_disponibles = st.session_state.datos_votos['departamento'].unique()
                filtro_depto = st.multiselect(
                    "📍 Filtrar por departamento",
                    options=deptos_disponibles,
                    default=deptos_disponibles
                )
        
        datos_filtrados = st.session_state.datos_votos[
            (st.session_state.datos_votos['candidato'].isin(filtro_candidato)) &
            (st.session_state.datos_votos['departamento'].isin(filtro_depto))
        ].copy()
        
        datos_mostrar = datos_filtrados[['nombre', 'candidato', 'departamento', 'hora']].copy()
        datos_mostrar['hora'] = datos_mostrar['hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        st.dataframe(
            datos_mostrar,
            use_container_width=True,
            height=400
        )
        
        csv = datos_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DESCARGAR DATOS (CSV)",
            data=csv,
            file_name=f'votos_colombia_2026_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab5:
        st.markdown("""
        <div class="glass-card">
            <h3 style='text-align: center;'>🔗 COMPARAR CON FUENTES OFICIALES</h3>
            <div style="background: rgba(255, 215, 0, 0.1); padding: 25px; border-radius: 15px; border: 2px solid #FFD700; margin: 20px 0;">
                <p style="font-size: 1.1rem; text-align: center; color: white; font-family: 'Exo 2';">
                Esta es una encuesta de intención de voto <b style="color: #FFD700;">NO OFICIAL</b>. 
                Para información electoral oficial y verificada, consulta las siguientes fuentes:
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #FFD700; font-family: 'Orbitron'; text-align: center;">🏛️ REGISTRADURÍA NACIONAL</h4>
                <p style="font-family: 'Exo 2'; color: #87CEEB; text-align: center;"><b>Portal Oficial de Resultados Electorales</b></p>
                
                <div style="margin: 20px 0;">
                    <a href="https://estadisticaselectorales.registraduria.gov.co/" target="_blank" class="official-link">
                        📊 Estadísticas Electorales
                    </a>
                    <a href="https://resultados.registraduria.gov.co/" target="_blank" class="official-link">
                        🗳️ Resultados en Tiempo Real
                    </a>
                    <a href="https://observatorio.registraduria.gov.co/" target="_blank" class="official-link">
                        📈 Observatorio Electoral
                    </a>
                    <a href="https://www.registraduria.gov.co/-Historico-de-resultados-electorales-.html" target="_blank" class="official-link">
                        📖 Histórico 1997-2023
                    </a>
                    <a href="https://wapp.registraduria.gov.co/electoral/" target="_blank" class="official-link">
                        📋 Preconteo y Escrutinio
                    </a>
                </div>
                
                <div style="background: rgba(135, 206, 235, 0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
                    <p style="font-family: 'Exo 2'; font-size: 0.9rem; margin: 0;"><b>Características:</b></p>
                    <ul style="font-family: 'Exo 2'; font-size: 0.9rem;">
                        <li>✅ Fuente oficial del Estado</li>
                        <li>✅ Datos en tiempo real el día de elecciones</li>
                        <li>✅ Histórico completo desde 1958</li>
                        <li>✅ Descarga de archivos CSV</li>
                        <li>✅ Actas de escrutinio digitalizadas</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_comp2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #FFD700; font-family: 'Orbitron'; text-align: center;">👁️ MISIÓN DE OBSERVACIÓN ELECTORAL</h4>
                <p style="font-family: 'Exo 2'; color: #87CEEB; text-align: center;"><b>Organización Independiente de Observación</b></p>
                
                <div style="margin: 20px 0;">
                    <a href="https://moe.org.co/" target="_blank" class="official-link">
                        🔍 Portal Principal MOE
                    </a>
                    <a href="https://moe.org.co/datos-electorales/" target="_blank" class="official-link">
                        📊 Datos Electorales
                    </a>
                    <a href="https://moe.org.co/publicaciones/" target="_blank" class="official-link">
                        📚 Publicaciones y Análisis
                    </a>
                    <a href="https://moe.org.co/lo-que-observamos/" target="_blank" class="official-link">
                        📋 Informes en Tiempo Real
                    </a>
                </div>
                
                <div style="background: rgba(135, 206, 235, 0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
                    <p style="font-family: 'Exo 2'; font-size: 0.9rem; margin: 0;"><b>Características:</b></p>
                    <ul style="font-family: 'Exo 2'; font-size: 0.9rem;">
                        <li>✅ Observación independiente</li>
                        <li>✅ Red de 3,000+ observadores</li>
                        <li>✅ Reportes de irregularidades</li>
                        <li>✅ Análisis de riesgo electoral</li>
                        <li>✅ Monitoreo de violencia política</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #FFD700; font-family: 'Orbitron'; text-align: center;">📚 CENTRO DE ESTUDIOS EN DEMOCRACIA (CEDAE)</h4>
            <div style="text-align: center; margin: 20px 0;">
                <a href="https://cedae.datasketch.co/datos-democracia/resultados-electorales/explora-los-datos/" target="_blank" class="official-link">
                    💾 Explorador de Datos
                </a>
                <a href="https://cedae.datasketch.co/" target="_blank" class="official-link">
                    📖 Repositorio Histórico
                </a>
            </div>
            <div style="background: rgba(135, 206, 235, 0.1); padding: 15px; border-radius: 10px;">
                <ul style="font-family: 'Exo 2'; font-size: 0.9rem;">
                    <li>📊 Base de datos descargable (CSV)</li>
                    <li>📈 Herramientas de visualización interactiva</li>
                    <li>🔍 Análisis comparativo 1958-2023</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer con efecto metálico
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 30px; background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(135, 206, 235, 0.1)); border-radius: 15px; margin-top: 40px;">
    <p style="font-family: 'Orbitron'; font-size: 1.2rem; color: #FFD700; margin: 5px 0; letter-spacing: 2px;">
        ✨ DESARROLLADO POR <b>DEIBER YESID LÓPEZ RAMÍREZ</b>
    </p>
    <p style="font-family: 'Exo 2'; color: #87CEEB; margin: 5px 0;">
        📊 Data Analyst • 🇨🇴 Colombia
    </p>
    <p style="font-family: 'Exo 2'; color: white; font-size: 0.9rem; margin: 10px 0;">
        📧 Herramienta de encuesta no oficial • Consulta fuentes oficiales arriba
    </p>
    <p style="font-family: 'Exo 2'; color: #FFD700; font-size: 0.85rem; margin: 5px 0;">
        🔗 Datos comparables con: Registraduría Nacional | MOE | CEDAE
    </p>
</div>
""", unsafe_allow_html=True)
