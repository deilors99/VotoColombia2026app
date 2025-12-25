import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random  # Para simular IP si quieres

# ================= CONFIG =================
st.set_page_config(
    layout="wide",
    page_title="🇨🇴 Elecciones Colombia 2026",
    page_icon="🇨🇴"
)

# ================= CSS =================
st.markdown("""
<style>
.stApp {
    background: none;
}
.background-carousel {
    position: fixed;
    inset: 0;
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
.background-carousel img:nth-child(1){animation-delay:0s;}
.background-carousel img:nth-child(2){animation-delay:8s;}
.background-carousel img:nth-child(3){animation-delay:16s;}
@keyframes carousel {
    0%{opacity:0;}
    10%{opacity:1;}
    30%{opacity:1;}
    40%{opacity:0;}
}
.stApp::after{
    content:'';
    position:fixed;
    inset:0;
    background:rgba(0,0,0,.75);
    z-index:-1;
}
</style>
""", unsafe_allow_html=True)

# ================= CARRUSEL =================
st.markdown("""
<div class="background-carousel">
    <img src="https://images.unsplash.com/photo-1582213782179-4841c6f00b1d?ixlib=rb-4.0.3&auto=format&fit=crop&q=80"> <!-- Petro ejemplo -->
    <img src="https://images.unsplash.com/photo-1578301978018-7e9d8f5e5d9d?ixlib=rb-4.0.3&auto=format&fit=crop&q=80"> <!-- Bandera Colombia -->
    <img src="https://images.unsplash.com/photo-1561417268-3b6e8e4a9d9e?ixlib=rb-4.0.3&auto=format&fit=crop&q=80"> <!-- Elecciones ejemplo -->
</div>
""", unsafe_allow_html=True)

# ================= DATA =================
candidatos = [
    "Gustavo Petro (hipotético)",
    "Sergio Fajardo",
    "Iván Cepeda",
    "Paloma Valencia",
    "Vicky Dávila",
    "Otro"
]

if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(
        columns=["candidato","hora","nombre","ult5","departamento"]
    )

# ================= HEADER =================
st.title("🇨🇴 Elecciones Colombia 2026")
st.markdown("### Análisis electoral hipotético")
st.markdown("---")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🗳️ Emitir voto")
    with st.form("voto"):
        nombre = st.text_input("Nombre")
        departamento = st.selectbox("Departamento", [
            "Selecciona...", "Antioquia","Bogotá D.C.","Valle","Cundinamarca"
        ])
        ult5 = st.text_input("Últimos 5 dígitos cédula", max_chars=5, type="password")
        candidato = st.selectbox("Candidato", candidatos)
        enviar = st.form_submit_button("Votar")
        if enviar:
            if not nombre or departamento=="Selecciona..." or len(ult5)!=5:
                st.error("Datos incompletos")
            elif ult5 in st.session_state.datos_votos["ult5"].values:
                st.error("Esta cédula ya votó")
            else:
                st.session_state.datos_votos.loc[len(st.session_state.datos_votos)] = [
                    candidato, datetime.now(), nombre, ult5, departamento
                ]
                st.success("Voto registrado 🇨🇴")
                st.balloons()
                st.rerun()

# ================= RESULTADOS =================
if not st.session_state.datos_votos.empty:
    resumen = (
        st.session_state.datos_votos
        .groupby("candidato")
        .size()
        .reset_index(name="votos")
    )
    fig = px.pie(
        resumen,
        values="votos",
        names="candidato",
        hole=.5
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<p style="text-align:center; color:#FFD700;">
<b>Desarrollado por Deiber Yesid López Ramírez</b><br>
Encuesta académica – No oficial ➡️
</p>
""", unsafe_allow_html=True)
