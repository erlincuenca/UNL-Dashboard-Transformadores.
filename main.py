import streamlit as st

# Configuración básica de la página principal
st.set_page_config(
    page_title="Tablero de Control - Transformadores",
    page_icon="⚡",
    layout="wide"
)

# --- INYECCIÓN DE ESTILO CSS GLOBAL (LETRAS GRANDES Y VISIBILIDAD MÁXIMA) ---
st.markdown("""
    <style>
    /* Texto general (párrafos, listas y viñetas) */
    p, li, div {
        font-size: 22px !important;
        line-height: 1.6 !important;
    }
    
    /* Encabezados de secciones principales (H3) */
    .stMarkdown h3 {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #4A90E2 !important;
        margin-top: 20px !important;
    }
    
    /* Subtítulos dentro de cajas informativas (st.info, st.success) */
    .element-container div[data-testid="stMarkdownContainer"] h3 {
        font-size: 24px !important;
        color: #FFFFFF !important;
    }
    
    /* Números de las tarjetas de métricas (st.metric) */
    div[data-testid="stMetricValue"] {
        font-size: 40px !important;
        font-weight: bold !important;
    }
    
    /* Etiquetas/Títulos sobre las métricas */
    div[data-testid="stMetricLabel"] {
        font-size: 22px !important;
        font-weight: 600 !important;
    }

    /* Pestañas (st.tabs) más grandes y visibles */
    button[data-baseweb="tab"] p {
        font-size: 22px !important;
        font-weight: bold !important;
    }

    /* Texto de la barra lateral (Sidebar) */
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label {
        font-size: 19px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título del proyecto y encabezado de presentación
st.title(" Análisis de Transformadores de Potencia")
st.caption("Herramienta interactiva para simulación y análisis de máquinas eléctricas")

st.markdown("""
### Bienvenid@ al Sistema de Simulación

Esta aplicación permite evaluar el comportamiento estacionario de transformadores monofásicos y sistemas de distribución mediante el análisis fasorial, circuito equivalente y unidades en por unidad.

---

####  Instrucciones de Navegación:
Utiliza el **menú de la barra lateral izquierda** para navegar y simular entre los 5 casos de estudio:

1. **Caso 1:** Transformador Ideal y Analisis Fasorial.
2. **Caso 2:** Transformador Real: Circuito Equivalente, Regulacion y Eficiencia.
3. **Caso 3:** Determinacion Experimental del Circuito Equivalente.
4. **Caso 4:** Transformador de Potencia en Sistema Por Unidad (p.u.).
5. **Caso 5:** Sistema Fuente – Alimentador – Transformador – Carga.
6. **Tabla Comparativa:** .
""")