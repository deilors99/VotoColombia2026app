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

# CSS con Fondo Animado Estilo TikTok
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;700;900&display=swap');
    
    /* Contenedor principal */
    .stApp {
        position: relative;
        overflow: hidden;
    }
    
    /* Fondo animado con imágenes verticales estilo TikTok */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Overlay oscuro para mejor legibilidad */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: -1;
        pointer-events: none;
    }
    
    /* Contenedor de columnas de imágenes */
    .background-images {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -2;
        display: flex;
        gap: 20px;
        overflow: hidden;
    }
    
    /* Columnas de imágenes */
    .image-column {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 20px;
        animation: scrollDown 60s linear infinite;
    }
    
    .image-column:nth-child(1) {
        animation-duration: 50s;
        animation-delay: 0s;
    }
    
    .image-column:nth-child(2) {
        animation-duration: 65s;
        animation-delay: -15s;
    }
    
    .image-column:nth-child(3) {
        animation-duration: 55s;
        animation-delay: -30s;
    }
    
    .image-column:nth-child(4) {
        animation-duration: 70s;
        animation-delay: -10s;
    }
    
    .image-column:nth-child(5) {
        animation-duration: 60s;
        animation-delay: -25s;
    }
    
    @keyframes scrollDown {
        0% {
            transform: translateY(-50%);
        }
        100% {
            transform: translateY(0%);
        }
    }
    
    /* Imágenes individuales */
    .bg-image {
        width: 100%;
        height: 400px;
        object-fit: cover;
        border-radius: 15px;
        opacity: 0.6;
        transition: opacity 0.3s ease;
        flex-shrink: 0;
    }
    
    .bg-image:hover {
        opacity: 0.8;
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
        z-index: 10;
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
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.6), 0 0 30px rgba(255, 215, 0, 0.4);
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
            0 8px 25px rgba(255, 215, 0, 0.5),
            inset 0 2px 0 rgba(255, 255, 255, 0.3),
            inset 0 -2px 0 rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        position: relative !important;
        overflow: hidden !important;
        z-index: 10 !important;
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
            0 15px 40px rgba(255, 215, 0, 0.7),
            inset 0 3px 0 rgba(255, 255, 255, 0.4),
            inset 0 -3px 0 rgba(0, 0, 0, 0.4) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    /* Cards modernas con glassmorphism mejorado */
    .card-modern {
        background: linear-gradient(135deg, 
            rgba(0, 0, 0, 0.85) 0%, 
            rgba(15, 12, 41, 0.9) 100%);
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            0 0 40px rgba(255, 215, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        z-index: 5;
    }
    
    .card-modern::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.08) 0%, transparent 70%);
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
            0 20px 60px rgba(255, 215, 0, 0.4),
            0 0 60px rgba(255, 215, 0, 0.25),
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
        text-shadow: 0 0 40px rgba(255, 215, 0, 0.6);
        animation: pulse 2s ease-in-out infinite;
        filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.5));
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
        text-shadow: 0 0 15px rgba(135, 206, 235, 0.5);
    }
    
    /* Inputs modernos */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        font-family: 'Exo 2', sans-serif !important;
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.8), rgba(30, 40, 55, 0.85)) !important;
        backdrop-filter: blur(15px) !important;
        color: white !important;
        border: 2px solid rgba(135, 206, 235, 0.4) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 1rem !important;
        box-shadow: 
            inset 0 2px 5px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(135, 206, 235, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #FFD700 !important;
        box-shadow: 
            0 0 30px rgba(255, 215, 0, 0.5),
            inset 0 2px 5px rgba(0, 0, 0, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTextInput>label,
    .stSelectbox>label {
        font-family: 'Exo 2', sans-serif !important;
        color: #87CEEB !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        text-shadow: 0 0 10px rgba(135, 206, 235, 0.4) !important;
        text-transform: uppercase !important;
    }
    
    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(15, 20, 25, 0.9));
        backdrop-filter: blur(20px);
        padding: 15px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.7), rgba(30, 40, 55, 0.8)) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        color: #87CEEB !important;
        font-weight: 700 !important;
        border: 2px solid rgba(135, 206, 235, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #FFD700 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #FFD700, #FFA500) !important;
        color: black !important;
        font-weight: 900 !important;
        border: 2px solid #FFD700 !important;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.7) !important;
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
    
    /* Sidebar mejorado */
    .stSidebar {
        background: linear-gradient(180deg, 
            rgba(0, 0, 0, 0.92) 0%, 
            rgba(15, 20, 25, 0.95) 100%) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 3px solid rgba(255, 215, 0, 0.4) !important;
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.7) !important;
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border-radius: 10px;
        border: 2px solid rgba(0, 0, 0, 0.6);
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
            rgba(255, 215, 0, 0.7), 
            transparent) !important;
        margin: 40px 0 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5) !important;
    }
    
    /* Banner de bienvenida mejorado */
    .welcome-banner {
        background: linear-gradient(135deg, 
            rgba(0, 0, 0, 0.85) 0%, 
            rgba(15, 12, 41, 0.9) 100%);
        backdrop-filter: blur(30px) saturate(180%);
        border-radius: 30px;
        padding: 80px 40px;
        border: 3px solid rgba(255, 215, 0, 0.5);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.8),
            0 0 60px rgba(255, 215, 0, 0.2),
            inset 0 2px 0 rgba(255, 255, 255, 0.1);
        max-width: 900px;
        margin: 0 auto;
        animation: floatBanner 6s ease-in-out infinite;
        position: relative;
        z-index: 10;
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
    
    /* Info boxes mejorados */
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 15px !important;
        padding: 20px !important;
        border-left: 5px solid !important;
        backdrop-filter: blur(15px) !important;
        animation: slideInLeft 0.4s ease-out !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
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
    
    /* Dataframe */
    .stDataFrame {
        background: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(135, 206, 235, 0.3) !important;
    }
</style>

<!-- Fondo con imágenes animadas estilo TikTok -->
<div class="background-images">
    <!-- Columna 1 -->
    <div class="image-column">
        <img class="bg-image" src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600&q=80" alt="Colombia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&q=80" alt="Voto">
        <img class="bg-image" src="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=600&q=80" alt="Democracia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=600&q=80" alt="Elecciones">
        <img class="bg-image" src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600&q=80" alt="Colombia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&q=80" alt="Voto">
    </div>
    
    <!-- Columna 2 -->
    <div class="image-column">
        <img class="bg-image" src="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=600&q=80" alt="Votación">
        <img class="bg-image" src="https://images.unsplash.com/photo-1555664424-778a1e5e1b48?w=600&q=80" alt="Congreso">
        <img class="bg-image" src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600&q=80" alt="Bandera">
        <img class="bg-image" src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=600&q=80" alt="Participación">
        <img class="bg-image" src="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=600&q=80" alt="Votación">
        <img class="bg-image" src="https://images.unsplash.com/photo-1555664424-778a1e5e1b48?w=600&q=80" alt="Congreso">
    </div>
    
    <!-- Columna 3 -->
    <div class="image-column">
        <img class="bg-image" src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&q=80" alt="Colombia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=600&q=80" alt="Voto">
        <img class="bg-image" src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600&q=80" alt="Democracia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=600&q=80" alt="Elecciones">
        <img class="bg-image" src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&q=80" alt="Colombia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=600&q=80" alt="Voto">
    </div>
    
    <!-- Columna 4 -->
    <div class="image-column">
        <img class="bg-image" src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=600&q=80" alt="Participación">
        <img class="bg-image" src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600&q=80" alt="Colombia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1555664424-778a1e5e1b48?w=600&q=80" alt="Gobierno">
        <img class="bg-image" src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&q=80" alt="Votación">
        <img class="bg-image" src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=600&q=80" alt="Participación">
        <img class="bg-image" src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600&q=80" alt="Colombia">
    </div>
    
    <!-- Columna 5 -->
    <div class="image-column">
        <img class="bg-image" src="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=600&q=80" alt="Democracia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&q=80" alt="Elecciones">
        <img class="bg-image" src="https://images.unsplash.com/photo-1589975876581-7ef2b0f7e7ac?w=600&q=80" alt="Voto">
        <img class="bg-image" src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600&q=80" alt="Colombia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=600&q=80" alt="Democracia">
        <img class="bg-image" src="https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&q=80" alt="Elecciones">
    </div>
</div>
""", unsafe_allow_html=True)

# ... [El resto del código Python permanece exactamente igual, solo copiar desde aquí todo el código anterior]
