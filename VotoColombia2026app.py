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

# --------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------
st.set_page_config(
    page_title="Voto Colombia 2026 🇨🇴",
    page_icon="🗳️",
    layout="wide"
)

# --------------------------------------------
# ESTILOS (CSS + HTML)
# --------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
.glass {
    background: rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.37);
}
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------
# ESTADO DE SESIÓN
# --------------------------------------------
if "votos" not in st.session_state:
    st.session_state.votos = []

# --------------------------------------------
# HEADER
# --------------------------------------------
st.markdown("""
<div class="glass">
    <div class="title">🗳️ Voto Colombia 2026</div>
    <div class="subtitle">Simulador académico de intención de voto</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --------------------------------------------
# SIDEBAR - FORMULARIO DE VOTACIÓN
# --------------------------------------------
st.sidebar.header("📥 Registrar voto")

departamento = st.sidebar.selectbox(
    "Departamento",
    ["Antioquia", "Cundinamarca", "Valle del Cauca", "Atlántico", "Santander", "Otro"]
)

edad = st.sidebar.slider("Edad", 18, 90, 30)

candidato = st.sidebar.selectbox(
    "Candidato",
    ["Candidato A", "Candidato B", "Candidato C", "Voto en Blanco"]
)

genero = st.sidebar.selectbox(
    "Género",
    ["Masculino", "Femenino", "Otro"]
)

if st.sidebar.button("🗳️ Votar"):
    voto = {
        "id": hashlib.md5(str(datetime.now()).encode()).hexdigest(),
        "fecha": datetime.now(),
        "departamento": departamento,
        "edad": edad,
        "candidato": candidato,
        "genero": genero
    }
    st.session_state.votos.append(voto)
    st.sidebar.success("✅ Voto registrado")

# --------------------------------------------
# DATAFRAME
# --------------------------------------------
df = pd.DataFrame(st.session_state.votos)

# --------------------------------------------
# TABS PRINCIPALES
# --------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Resultados", "📈 Análisis", "🤖 Machine Learning"])

# --------------------------------------------
# TAB 1 - RESULTADOS
# --------------------------------------------
with tab1:
    st.subheader("Resultados generales")

    if df.empty:
        st.info("Aún no hay votos registrados.")
    else:
        conteo = df["candidato"].value_counts().reset_index()
        conteo.columns = ["Candidato", "Votos"]

        fig = px.bar(
            conteo,
            x="Candidato",
            y="Votos",
            color="Candidato",
            title="Distribución de votos"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df)

# --------------------------------------------
# TAB 2 - ANÁLISIS
# --------------------------------------------
with tab2:
    st.subheader("Análisis por departamento")

    if df.empty:
        st.info("No hay datos para analizar.")
    else:
        depto = df.groupby(["departamento", "candidato"]).size().reset_index(name="Votos")

        fig = px.bar(
            depto,
            x="departamento",
            y="Votos",
            color="candidato",
            barmode="group",
            title="Votos por departamento"
        )
        st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------
# TAB 3 - MACHINE LEARNING
# --------------------------------------------
with tab3:
    st.subheader("Clustering de votantes (ML)")

    if len(df) < 10:
        st.warning("Se requieren al menos 10 votos para aplicar Machine Learning.")
    else:
        ml_df = df.copy()

        ml_df["candidato_cod"] = ml_df["candidato"].astype("category").cat.codes
        ml_df["departamento_cod"] = ml_df["departamento"].astype("category").cat.codes
        ml_df["genero_cod"] = ml_df["genero"].astype("category").cat.codes

        X = ml_df[["edad", "candidato_cod", "departamento_cod", "genero_cod"]]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        ml_df["cluster"] = clusters

        pca = PCA(n_components=2)
        components = pca.fit_transform(X_scaled)

        ml_df["PCA1"] = components[:, 0]
        ml_df["PCA2"] = components[:, 1]

        fig = px.scatter(
            ml_df,
            x="PCA1",
            y="PCA2",
            color="cluster",
            title="Segmentación de votantes",
            hover_data=["edad", "candidato", "departamento"]
        )

        st.plotly_chart(fig, use_container_width=True)

        score = silhouette_score(X_scaled, clusters)
        st.metric("Silhouette Score", round(score, 3))

# --------------------------------------------
# FOOTER
# --------------------------------------------
st.caption("Proyecto académico · Data Analytics · Streamlit · Machine Learning · Colombia 2026")
