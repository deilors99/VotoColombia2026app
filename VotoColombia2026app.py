import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

st.set_page_config(layout="wide", page_title="Voto Colombia 2026 🇨🇴", page_icon="🗳️")

st.markdown("""
<style>
    .main {background-color: #0a0e17; color: #e0e0e0;}
    .stSidebar {background-color: #1a1f2e;}
    h1, h2 {color: #FFD700; text-align: center;}
    .stButton>button {background-color: #FFD700; color: black; font-weight: bold; border-radius: 12px;}
    .stSuccess {background-color: #006400; color: white;}
    .stError {background-color: #8B0000; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🇨🇴 VOTO COLOMBIA PRESIDENCIALES 2026")
st.markdown("<h2 style='color: #87CEEB;'>Encuesta Electoral Segura</h2>", unsafe_allow_html=True)
st.markdown("**Creador: Deiber Yesid López Ramírez - Data Analyst**")

candidatos = [
    "Iván Cepeda", "Paloma Valencia", "Gustavo Petro (hipotético)", 
    "Sergio Fajardo", "Vicky Dávila", "Abelardo de la Espriella", 
    "David Luna", "Juan Daniel Oviedo", "Otro"
]

if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(columns=["candidato", "votos", "hora", "ip", "nombre", "ult5"])

with st.sidebar:
    st.header("🗳️ Vota (Solo Colombianos)")
    nombre = st.text_input("Nombre")
    ult5 = st.text_input("Últimos 5 dígitos cédula", max_chars=5)
    seleccion = st.selectbox("Candidato", candidatos)
    
    if st.button("VOTAR"):
        if not nombre or not ult5.isdigit() or len(ult5) != 5:
            st.error("Datos inválidos")
        elif ult5 in st.session_state.datos_votos["ult5"].values:
            st.error("Ya votaste")
        else:
            nuevo = pd.DataFrame({"candidato": [seleccion], "votos": [1], "hora": [datetime.now()], "ip": [random.random()], "nombre": [nombre], "ult5": [ult5]})
            st.session_state.datos_votos = pd.concat([st.session_state.datos_votos, nuevo], ignore_index=True)
            st.success("¡Voto registrado! 🇨🇴")
            st.balloons()

if st.session_state.datos_votos.empty:
    st.info("Sé el primero")
else:
    resumen = st.session_state.datos_votos.groupby("candidato")["votos"].sum().reset_index().sort_values("votos", ascending=False)
    total = resumen["votos"].sum()
    resumen["%"] = (resumen["votos"] / total * 100).round(1)
    
    st.metric("Líder", resumen.iloc[0]["candidato"], f"{resumen.iloc[0]['%']}%")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ranking")
        for _, row in resumen.iterrows():
            st.write(f"**{row['candidato']}** - {row['%']}%")
            st.progress(row["%"]/100)
    with col2:
        fig = px.pie(resumen, values="votos", names="candidato", hole=0.5)
        st.plotly_chart(fig)

st.caption("Desarrollado por Deiber Yesid López Ramírez • Data Analyst")