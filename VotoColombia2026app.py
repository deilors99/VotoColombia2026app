# ============================================
# VOTO COLOMBIA 2026 - Sistema de Encuesta Electoral
# Creador: Deiber Yesid López Ramírez
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# ================= CONFIGURACIÓN =================
st.set_page_config(
    layout="wide",
    page_title="VOTO COLOMBIA PRESIDENCIALES 2026 🇨🇴",
    page_icon="🗳️"
)

# ================= CSS + CARRUSEL RESPONSIVO =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Exo+2:wght@400;700&display=swap');

.stApp {
    background: none;
    position: relative;
    z-index: 1;
}

/* ===== CARRUSEL ===== */
.background-carousel {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    overflow: hidden;
}

.background-carousel img {
    position: absolute;
    width: 100%;
    height: 100vh;
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

h1 {
    font-family: 'Orbitron', sans-serif;
    color: #FFD700;
    text-align: center;
}

.card-modern {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 25px;
    border: 2px solid rgba(255,215,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ================= IMÁGENES DEL CARRUSEL =================
st.markdown("""
<div class="background-carousel">
    <img src="https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1920&h=1080&fit=crop&auto=format&q=80">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Gustavo_Petro_2022.jpg/1920px-Gustavo_Petro_2022.jpg">
    <img src="https://cdn.pixabay.com/photo/2023/05/06/09/36/colombia-flag-7972339_1920.jpg">
</div>
""", unsafe_allow_html=True)

# ================= DATOS =================
candidatos = [
    "Gustavo Petro (hipotético)", "Paloma Valencia", "Iván Cepeda",
    "Sergio Fajardo", "Vicky Dávila", "Abelardo de la Espriella",
    "David Luna", "Juan Daniel Oviedo", "Otro"
]

if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(
        columns=["candidato", "votos", "hora", "nombre", "ult5", "departamento"]
    )

# ================= HEADER =================
st.title("🇨🇴 VOTO COLOMBIA PRESIDENCIALES 2026")
st.markdown("### Encuesta Electoral Académica")
st.markdown("---")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🗳️ EMITE TU VOTO")
    with st.form("form_voto"):
        nombre = st.text_input("Nombre")
        depto = st.selectbox("Departamento", ["Selecciona...", "Antioquia", "Bogotá D.C.", "Valle del Cauca"])
        ult5 = st.text_input("Últimos 5 dígitos cédula", max_chars=5, type="password")
        candidato = st.selectbox("Candidato", candidatos)
        enviar = st.form_submit_button("VOTAR")

        if enviar:
            if not nombre or depto == "Selecciona..." or len(ult5) != 5:
                st.error("Completa todos los campos")
            elif ult5 in st.session_state.datos_votos["ult5"].values:
                st.error("Esta cédula ya votó")
            else:
                nuevo = pd.DataFrame({
                    "candidato": [candidato],
                    "votos": [1],
                    "hora": [datetime.now()],
                    "nombre": [nombre],
                    "ult5": [ult5],
                    "departamento": [depto]
                })
                st.session_state.datos_votos = pd.concat(
                    [st.session_state.datos_votos, nuevo], ignore_index=True
                )
                st.success("Voto registrado")

# ================= RESULTADOS =================
if not st.session_state.datos_votos.empty:
    resumen = (
        st.session_state.datos_votos
        .groupby("candidato")["votos"]
        .sum()
        .reset_index()
    )

    fig = px.pie(resumen, values="votos", names="candidato", hole=0.5)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#87CEEB;">
<b>Desarrollado por Deiber Yesid López Ramírez</b><br>
Encuesta académica no oficial 🇨🇴
</div>
""", unsafe_allow_html=True)
