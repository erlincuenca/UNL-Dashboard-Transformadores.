import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tabla Comparativa", layout="wide")

st.title("📊 Resumen Comparativo de Resultados")
st.write("Consolidación de las métricas obtenidas en cada uno de los 5 casos simulados.")

# Consolidación de datos almacenados en memoria
casos_guardados = [
    st.session_state.get('caso1', None),
    st.session_state.get('caso2', None),
    st.session_state.get('caso3', None),
    st.session_state.get('caso4', None),
    st.session_state.get('caso5', None)
]

# Filtrado de módulos visitados
datos_existentes = [c for c in casos_guardados if c is not None]

if datos_existentes:
    df = pd.DataFrame(datos_existentes)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Para visualizar la tabla comparativa completa, primero navegue por las páginas del Caso 1 al Caso 5 en el menú lateral.")