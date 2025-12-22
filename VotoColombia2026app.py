import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib

# Configuración de página
st.set_page_config(
    layout="wide", 
    page_title="Voto Colombia 2026 🇨🇴", 
    page_icon="🗳️",
    initial_sidebar_state="expanded"
)

# CSS mejorado
st.markdown("""
<style>
    /* Fondo principal */
    .main {
        background: linear-gradient(135deg, #0a0e17 0%, #1a2332 50%, #0a0e17 100%);
        color: #e0e0e0;
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, #1a1f2e 0%, #0f1419 100%);
    }
    
    /* Títulos */
    h1 {
        color: #FFD700;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-size: 3rem !important;
    }
    
    h2 {
        color: #87CEEB;
        text-align: center;
        font-size: 2rem !important;
    }
    
    h3 {
        color: #FFD700;
        font-size: 1.5rem !important;
    }
    
    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 15px 30px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
    }
    
    /* Mensajes */
    .stSuccess {
        background-color: #006400;
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00ff00;
    }
    
    .stError {
        background-color: #8B0000;
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff0000;
    }
    
    .stWarning {
        background-color: #FF8C00;
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #FFD700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #87CEEB;
        font-size: 1.2rem;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #2d3748;
        color: white;
        border: 2px solid #4a5568;
        border-radius: 8px;
        padding: 10px;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #FFD700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2d3748;
        border-radius: 8px;
        padding: 10px 20px;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black;
    }
    
    /* Cards personalizadas */
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 215, 0, 0.2);
        margin: 10px 0;
    }
</style>
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

if "votado" not in st.session_state:
    st.session_state.votado = False

# Función para generar hash único
def generar_hash(cedula):
    return hashlib.sha256(cedula.encode()).hexdigest()[:16]

# Header principal
col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
with col_header2:
    st.title("🇨🇴 VOTO COLOMBIA PRESIDENCIALES 2026")
    st.markdown("<h2 style='color: #87CEEB;'>Encuesta Electoral Segura</h2>", unsafe_allow_html=True)
    st.markdown("**Creador: Deiber Yesid López Ramírez - Data Analyst**")

st.divider()

# Sidebar para votación
with st.sidebar:
    st.header("🗳️ EMITE TU VOTO")
    st.caption("Solo ciudadanos colombianos")
    
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
            # Validaciones
            if not nombre.strip():
                st.error("❌ Por favor ingresa tu nombre")
            elif departamento == "Selecciona...":
                st.error("❌ Por favor selecciona tu departamento")
            elif not ult5.strip() or not ult5.isdigit() or len(ult5) != 5:
                st.error("❌ Ingresa exactamente 5 dígitos numéricos")
            elif ult5 in st.session_state.datos_votos["ult5"].values:
                st.error("❌ Esta cédula ya votó. Un voto por persona.")
            else:
                # Registrar voto
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
                st.session_state.votado = True
                st.success("✅ ¡Voto registrado exitosamente! 🇨🇴")
                st.balloons()
                st.rerun()
    
    # Estadísticas rápidas en sidebar
    st.divider()
    total_votos = len(st.session_state.datos_votos)
    st.metric("📊 Total de Votos", total_votos)
    
    if total_votos > 0:
        ultimo_voto = st.session_state.datos_votos.iloc[-1]
        st.info(f"🕐 Último voto: {ultimo_voto['hora'].strftime('%H:%M:%S')}")

# Contenido principal
if st.session_state.datos_votos.empty:
    st.info("🗳️ **¡Sé el primero en votar!** Inicia la encuesta electoral colombiana.", icon="👋")
else:
    # Calcular resultados
    resumen = (st.session_state.datos_votos
               .groupby("candidato")["votos"]
               .sum()
               .reset_index()
               .sort_values("votos", ascending=False))
    
    total = resumen["votos"].sum()
    resumen["porcentaje"] = (resumen["votos"] / total * 100).round(2)
    
    # Tabs para organizar información
    tab1, tab2, tab3, tab4 = st.tabs(["📊 RESULTADOS", "📈 ANÁLISIS", "🗺️ POR REGIÓN", "📋 DATOS"])
    
    with tab1:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🥇 LÍDER",
                resumen.iloc[0]["candidato"],
                f"{resumen.iloc[0]['porcentaje']}%"
            )
        
        with col2:
            st.metric("📊 Total Votos", total)
        
        with col3:
            if len(resumen) > 1:
                diferencia = resumen.iloc[0]["porcentaje"] - resumen.iloc[1]["porcentaje"]
                st.metric("📉 Diferencia", f"{diferencia:.1f}%")
        
        with col4:
            departamentos_unicos = st.session_state.datos_votos["departamento"].nunique()
            st.metric("🗺️ Departamentos", departamentos_unicos)
        
        st.divider()
        
        # Gráficos principales
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("🏆 RANKING ELECTORAL")
            for idx, row in resumen.iterrows():
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"**{row['candidato']}**")
                        st.progress(row['porcentaje']/100)
                    with col_b:
                        st.metric("", f"{row['porcentaje']}%", f"{row['votos']} votos")
        
        with col_right:
            st.subheader("📊 DISTRIBUCIÓN DE VOTOS")
            
            # Gráfico de torta mejorado
            fig_pie = go.Figure(data=[go.Pie(
                labels=resumen['candidato'],
                values=resumen['votos'],
                hole=.5,
                marker=dict(
                    colors=['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', 
                            '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'],
                    line=dict(color='#1a1f2e', width=2)
                ),
                textinfo='label+percent',
                textfont_size=12,
                hovertemplate='<b>%{label}</b><br>Votos: %{value}<br>Porcentaje: %{percent}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab2:
        st.subheader("📈 ANÁLISIS COMPARATIVO")
        
        # Gráfico de barras horizontal
        fig_bar = px.bar(
            resumen,
            x='votos',
            y='candidato',
            orientation='h',
            color='porcentaje',
            color_continuous_scale='sunset',
            text='porcentaje',
            title='Comparativa de Candidatos'
        )
        
        fig_bar.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        
        fig_bar.update_layout(
            yaxis={'categoryorder':'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Evolución temporal
        st.subheader("⏰ EVOLUCIÓN TEMPORAL")
        votos_tiempo = st.session_state.datos_votos.copy()
        votos_tiempo['hora_redondeada'] = votos_tiempo['hora'].dt.floor('5min')
        votos_acumulados = votos_tiempo.groupby('hora_redondeada').size().cumsum()
        
        fig_time = px.line(
            x=votos_acumulados.index,
            y=votos_acumulados.values,
            title='Participación Acumulada',
            labels={'x': 'Hora', 'y': 'Votos Acumulados'}
        )
        
        fig_time.update_traces(line_color='#FFD700', line_width=3)
        fig_time.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_time, use_container_width=True)
    
    with tab3:
        st.subheader("🗺️ ANÁLISIS POR DEPARTAMENTO")
        
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
                    title='Top 10 Departamentos con Más Participación',
                    color='total_votos',
                    color_continuous_scale='tealgrn'
                )
                
                fig_depto.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_depto, use_container_width=True)
            
            with col_map2:
                # Candidato líder por departamento
                lider_depto = (st.session_state.datos_votos
                              .groupby(['departamento', 'candidato'])
                              .size()
                              .reset_index(name='votos'))
                
                idx = lider_depto.groupby('departamento')['votos'].idxmax()
                lideres = lider_depto.loc[idx].sort_values('votos', ascending=False).head(10)
                
                st.write("**🏆 Líder por Departamento (Top 10)**")
                for _, row in lideres.iterrows():
                    st.write(f"**{row['departamento']}:** {row['candidato']} ({row['votos']} votos)")
    
    with tab4:
        st.subheader("📋 BASE DE DATOS DE VOTOS")
        
        # Opciones de filtro
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            filtro_candidato = st.multiselect(
                "Filtrar por candidato",
                options=candidatos,
                default=candidatos
            )
        
        with col_filter2:
            if 'departamento' in st.session_state.datos_votos.columns:
                deptos_disponibles = st.session_state.datos_votos['departamento'].unique()
                filtro_depto = st.multiselect(
                    "Filtrar por departamento",
                    options=deptos_disponibles,
                    default=deptos_disponibles
                )
        
        # Aplicar filtros
        datos_filtrados = st.session_state.datos_votos[
            (st.session_state.datos_votos['candidato'].isin(filtro_candidato)) &
            (st.session_state.datos_votos['departamento'].isin(filtro_depto))
        ].copy()
        
        # Mostrar datos (sin mostrar cédulas completas por privacidad)
        datos_mostrar = datos_filtrados[['nombre', 'candidato', 'departamento', 'hora']].copy()
        datos_mostrar['hora'] = datos_mostrar['hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        st.dataframe(
            datos_mostrar,
            use_container_width=True,
            height=400
        )
        
        # Botón de descarga
        csv = datos_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Datos (CSV)",
            data=csv,
            file_name=f'votos_colombia_2026_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
        )

# Footer
st.divider()
col_footer = st.columns([1, 2, 1])
with col_footer[1]:
    st.caption("✨ Desarrollado por **Deiber Yesid López Ramírez** • Data Analyst")
    st.caption("📧 Contacto: [LinkedIn](https://linkedin.com) | [GitHub](https://github.com)")
