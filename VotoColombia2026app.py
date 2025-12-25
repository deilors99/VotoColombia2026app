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

# ============================================
# CONFIGURACIÓN STREAMLIT (SOLO UNA VEZ)
# ============================================
st.set_page_config(
    page_title="Voto Colombia 2026 🇨🇴",
    page_icon="🗳️",
    layout="wide"
)

# ============================================
# CSS GLOBAL (OPTIMIZADO Y ESTABLE)
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Exo+2:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

h1 {
    font-family: 'Orbitron', sans-serif !important;
    color: #FFD700 !important;
    text-align: center;
    text-shadow: 0 0 25px rgba(255,215,0,.6);
}

h2, h3 {
    font-family: 'Exo 2', sans-serif !important;
    color: #87CEEB !important;
}

.card {
    background: rgba(0,0,0,.6);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 25px;
    border: 2px solid rgba(255,215,0,.3);
    box-shadow: 0 10px 30px rgba(0,0,0,.5);
    margin-bottom: 20px;
}

.stButton>button {
    background: linear-gradient(135deg,#FFD700,#FFA500);
    color: black;
    font-weight: 900;
    border-radius: 12px;
    padding: 15px 25px;
    border: none;
    box-shadow: 0 8px 25px rgba(255,215,0,.5);
}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATOS Y SESSION STATE
# ============================================
candidatos = [
    "Gustavo Petro (hipotético)",
    "Sergio Fajardo",
    "Paloma Valencia",
    "Vicky Dávila",
    "Juan Daniel Oviedo",
    "Otro"
]

if "votos" not in st.session_state:
    st.session_state.votos = pd.DataFrame(
        columns=["nombre", "departamento", "candidato", "hora", "hash"]
    )

def generar_hash(valor: str) -> str:
    return hashlib.sha256(valor.encode()).hexdigest()[:12]

# ============================================
# HEADER
# ============================================
st.title("🇨🇴 VOTO COLOMBIA 2026")
st.markdown("### Encuesta ciudadana no oficial")
st.markdown("---")

# ============================================
# SIDEBAR – VOTACIÓN
# ============================================
with st.sidebar:
    st.header("🗳️ Emitir voto")

    with st.form("form_voto"):
        nombre = st.text_input("Nombre")
        departamento = st.selectbox(
            "Departamento",
            ["Selecciona", "Antioquia", "Bogotá D.C.", "Valle", "Santander", "Atlántico"]
        )
        ult5 = st.text_input("Últimos 5 dígitos cédula", max_chars=5, type="password")
        candidato = st.selectbox("Candidato", candidatos)

        enviar = st.form_submit_button("VOTAR")

        if enviar:
            if not nombre or departamento == "Selecciona" or len(ult5) != 5:
                st.error("❌ Datos incompletos")
            elif ult5 in st.session_state.votos["hash"].values:
                st.error("❌ Esta cédula ya votó")
            else:
                nuevo = {
                    "nombre": nombre,
                    "departamento": departamento,
                    "candidato": candidato,
                    "hora": datetime.now(),
                    "hash": ult5
                }
                st.session_state.votos = pd.concat(
                    [st.session_state.votos, pd.DataFrame([nuevo])],
                    ignore_index=True
                )
                st.success("✅ Voto registrado")
                st.balloons()
                st.rerun()

    st.metric("Total votos", len(st.session_state.votos))

# ============================================
# CONTENIDO PRINCIPAL
# ============================================
if st.session_state.votos.empty:
    st.markdown("""
    <div class="card" style="text-align:center;">
        <h2>📢 Aún no hay votos</h2>
        <p>Sé el primero en participar</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.subheader("📊 Resultados")

    conteo = st.session_state.votos["candidato"].value_counts().reset_index()
    conteo.columns = ["Candidato", "Votos"]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            conteo,
            x="Candidato",
            y="Votos",
            color="Candidato",
            title="Votos por candidato"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            conteo,
            names="Candidato",
            values="Votos",
            title="Distribución porcentual"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🧾 Detalle de votos")
    st.dataframe(st.session_state.votos.drop(columns=["hash"]))


