# =========================================================
# 🇨🇴 VOTO COLOMBIA 2026 - DASHBOARD ANALÍTICO + ML
# Autor: Deiber Yesid López Ramírez
# Rol: Data Analyst / Data Science
# Framework: Streamlit
# Uso: Académico / Analítico (NO OFICIAL)
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------------
st.set_page_config(
    page_title="Voto Colombia 2026 🇨🇴",
    page_icon="🗳️",
    layout="wide"
)

# ---------------------------------------------------------
# ESTILOS CSS
# ---------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}
h1, h2, h3 {
    color: #FFD700;
}
[data-testid="stMetricValue"] {
    font-size: 2rem;
    color: #FFD700;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATOS INICIALES
# ---------------------------------------------------------
candidatos = [
    "Iván Cepeda",
    "Paloma Valencia",
    "Sergio Fajardo",
    "Vicky Dávila",
    "Juan Daniel Oviedo",
    "David Luna",
    "Voto en Blanco",
    "Otro"
]

if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(
        columns=["nombre", "departamento", "candidato", "hora"]
    )

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("🇨🇴 ELECCIONES PRESIDENCIALES 2026")
st.markdown("### Dashboard Analítico y Académico")
st.markdown("**Autor:** Deiber Yesid López Ramírez – Data Analyst")
st.divider()

# ---------------------------------------------------------
# SIDEBAR - REGISTRO DE VOTO (SIMULADO)
# ---------------------------------------------------------
with st.sidebar:
    st.header("🗳️ Registro de Voto (Simulación)")

    with st.form("form_voto"):
        nombre = st.text_input("Nombre")
        departamento = st.selectbox(
            "Departamento",
            [
                "Antioquia", "Atlántico", "Bogotá D.C.", "Bolívar",
                "Boyacá", "Caldas", "Cauca", "Cesar",
                "Córdoba", "Cundinamarca", "Huila",
                "La Guajira", "Magdalena", "Meta",
                "Nariño", "Norte de Santander",
                "Risaralda", "Santander",
                "Tolima", "Valle del Cauca"
            ]
        )
        candidato = st.selectbox("Candidato", candidatos)

        enviar = st.form_submit_button("Registrar voto")

        if enviar:
            if nombre.strip() == "":
                st.error("Debe ingresar nombre")
            else:
                nuevo = pd.DataFrame({
                    "nombre": [nombre],
                    "departamento": [departamento],
                    "candidato": [candidato],
                    "hora": [datetime.now()]
                })
                st.session_state.datos_votos = pd.concat(
                    [st.session_state.datos_votos, nuevo],
                    ignore_index=True
                )
                st.success("Voto registrado (simulación)")
                st.rerun()

# ---------------------------------------------------------
# VALIDACIÓN
# ---------------------------------------------------------
if st.session_state.datos_votos.empty:
    st.info("No hay votos registrados aún.")
    st.stop()

# ---------------------------------------------------------
# RESUMEN GENERAL
# ---------------------------------------------------------
df = st.session_state.datos_votos.copy()

resumen = (
    df.groupby("candidato")
    .size()
    .reset_index(name="votos")
    .sort_values("votos", ascending=False)
)

total_votos = resumen["votos"].sum()
resumen["porcentaje"] = (resumen["votos"] / total_votos * 100).round(2)

# ---------------------------------------------------------
# KPIs INSTITUCIONALES
# ---------------------------------------------------------
st.subheader("📊 Resumen Nacional")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🗳️ Total Votos", total_votos)
col2.metric("🏆 Candidato Líder", resumen.iloc[0]["candidato"])
if len(resumen) > 1:
    dif = resumen.iloc[0]["porcentaje"] - resumen.iloc[1]["porcentaje"]
else:
    dif = 0
col3.metric("📈 Diferencia", f"{dif:.2f}%")
col4.metric("🗺️ Deptos", df["departamento"].nunique())

st.divider()

# ---------------------------------------------------------
# TABS PRINCIPALES
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Resultados",
    "📈 Visualización",
    "🧠 Machine Learning"
])

# ---------------------------------------------------------
# TAB 1 - RESULTADOS
# ---------------------------------------------------------
with tab1:
    st.subheader("Resultados Nacionales")

    fig_bar = px.bar(
        resumen,
        x="candidato",
        y="porcentaje",
        text="porcentaje",
        color="candidato"
    )
    fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_bar.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_pie = px.pie(
        resumen,
        names="candidato",
        values="votos",
        hole=0.4
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------------
# TAB 2 - VISUALIZACIÓN TERRITORIAL
# ---------------------------------------------------------
with tab2:
    st.subheader("Participación por Departamento")

    votos_depto = (
        df.groupby("departamento")
        .size()
        .reset_index(name="votos")
        .sort_values("votos", ascending=False)
    )

    fig_dep = px.bar(
        votos_depto,
        x="votos",
        y="departamento",
        orientation="h",
        color="votos",
        color_continuous_scale="Viridis"
    )
    fig_dep.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    st.plotly_chart(fig_dep, use_container_width=True)

# ---------------------------------------------------------
# TAB 3 - MACHINE LEARNING (CLUSTERING)
# ---------------------------------------------------------
with tab3:
    st.subheader("🧠 Clustering Electoral (K-Means)")

    cluster_df = (
        df.groupby("departamento")
        .agg(
            total_votos=("candidato", "count"),
            diversidad=("candidato", "nunique")
        )
        .reset_index()
    )

    scaler = StandardScaler()
    X = scaler.fit_transform(
        cluster_df[["total_votos", "diversidad"]]
    )

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_df["cluster"] = kmeans.fit_predict(X)

    fig_cluster = px.scatter(
        cluster_df,
        x="total_votos",
        y="diversidad",
        color="cluster",
        text="departamento",
        size="total_votos",
        color_continuous_scale="Turbo"
    )

    fig_cluster.update_traces(textposition="top center")
    fig_cluster.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    st.markdown("""
    **Interpretación académica:**
    - Cluster 0: Baja participación
    - Cluster 1: Participación media
    - Cluster 2: Alta participación y diversidad

    ⚖️ *Análisis estadístico no predictivo*
    """)

# ---------------------------------------------------------
# FOOTER LEGAL
# ---------------------------------------------------------
st.divider()
st.caption(
    "⚖️ Proyecto académico de análisis de datos. "
    "No corresponde a resultados oficiales. "
    "Consulte únicamente la Registraduría Nacional del Estado Civil."
)



