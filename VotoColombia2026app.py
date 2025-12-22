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

# CSS Optimizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Exo+2:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #18c7a1 0%, #c24725 50%, #f7eb0a 100%);
    }
    
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        color: #0c56eb !important;
        text-align: center !important;
        font-size: 3rem !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important;
        animation: glow 2s ease-in-out infinite !important;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
        50% { text-shadow: 0 0 40px rgba(255, 215, 0, 0.8); }
    }
    
    h2 {
        font-family: 'Exo 2', sans-serif !important;
        color: #87CEEB !important;
        text-align: center !important;
    }
    
    h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #FFD700 !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-size: 1.2rem !important;
        border: none !important;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 30px rgba(255, 215, 0, 0.6) !important;
    }
    
    .card-modern {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .card-modern:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #FFD700 !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #87CEEB !important;
        font-size: 1.2rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(45, 55, 72, 0.6) !important;
        color: #87CEEB !important;
        border-radius: 10px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# Datos
candidatos = [
    "Gustavo Petro (hipotético)", "Paloma Valencia", "Iván Cepeda",
    "Sergio Fajardo", "Vicky Dávila", "Abelardo de la Espriella",
    "David Luna", "Juan Daniel Oviedo", "En blanco"
]

# Inicializar
if "datos_votos" not in st.session_state:
    st.session_state.datos_votos = pd.DataFrame(
        columns=["candidato", "votos", "hora", "nombre", "ult5", "departamento"]
    )

def generar_hash(cedula):
    return hashlib.sha256(cedula.encode()).hexdigest()[:16]

# HEADER
st.title("🇨🇴 COLOMBIA ARDE 🔥 PETRO - PRESIDENTE 2026 - 2030")
st.markdown("### Encuesta Electoral Segura, queremos saber su opinion")
st.markdown("**En esta pagina se haran visibles de manera sistematica todos los que apoyan el progreso del empleado, enfoque actual del gobierno Petro**")
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
    
    with st.form("form_voto"):
        nombre = st.text_input("✍️ Nombre", placeholder="Tu nombre")
        departamento = st.selectbox("📍 Departamento", [
            "Selecciona...", "Antioquia", "Atlántico", "Bogotá D.C.", 
            "Bolívar", "Boyacá", "Caldas", "Caquetá", "Cauca", "Cesar",
            "Córdoba", "Cundinamarca", "Huila", "La Guajira", "Magdalena",
            "Meta", "Nariño", "Norte de Santander", "Quindío", "Risaralda",
            "Santander", "Sucre", "Tolima", "Valle del Cauca"
        ])
        ult5 = st.text_input("🔢 Últimos 5 dígitos cédula", max_chars=5, type="password")
        candidato = st.selectbox("🎯 Candidato", candidatos)
        
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
    st.info("🗳️ **¡Sé el primero en votar!**")
else:
    resumen = (st.session_state.datos_votos
               .groupby("candidato")["votos"]
               .sum()
               .reset_index()
               .sort_values("votos", ascending=False))
    total = resumen["votos"].sum()
    resumen["porcentaje"] = (resumen["votos"] / total * 100).round(2)
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 RESULTADOS",
        "📈 ANÁLISIS",
        "📋 DATOS",
        "🧠 MACHINE LEARNING"
    ])
    
    with tab1:
        # Métricas
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
        
        # Gráficos
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
        
        # Por departamento
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
        
        # Descarga
        csv = datos_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar CSV",
            data=csv,
            file_name=f'votos_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    
    with tab4:
        st.subheader("🧠 Análisis Avanzado con Machine Learning")
        
        # Verificar que hay suficientes datos
        if len(st.session_state.datos_votos) < 10:
            st.warning("⚠️ Se necesitan al menos 10 votos para realizar análisis de Machine Learning")
        else:
            # ===============================
            # DATASET PARA ML
            # ===============================
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
            
            # ===============================
            # NORMALIZACIÓN
            # ===============================
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(
                cluster_df[["total_votos", "diversidad_candidatos"]]
            )
            
            # ===============================
            # K-MEANS
            # ===============================
            n_clusters = min(3, len(cluster_df))  # Ajustar según datos disponibles
            
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init=10
            )
            cluster_df["cluster"] = kmeans.fit_predict(X_scaled)
            
            # Métrica de calidad
            if n_clusters > 1:
                score = silhouette_score(X_scaled, cluster_df["cluster"])
                st.metric("📐 Silhouette Score", f"{score:.3f}")
            
            # ===============================
            # VISUALIZACIÓN
            # ===============================
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
            
            # ===============================
            # PCA (REDUCCIÓN DIMENSIONAL)
            # ===============================
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
            
            # ===============================
            # INTERPRETACIÓN
            # ===============================
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
<div style="text-align: center; color: #87CEEB; padding: 20px;">
    <p><b>✨ Desarrollado por Deiber Yesid López Ramírez - Data Analyst</b></p>
    <p>🇨🇴 Encuesta no oficial • Consulta fuentes oficiales arriba</p>
</div>
""", unsafe_allow_html=True)






