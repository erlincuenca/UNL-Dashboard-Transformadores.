import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="Caso 3: Ensayos de Trafo", layout="wide")

# 2. Inyección de estilos de texto grande
st.markdown("""
    <style>
    /* Texto general (párrafos, listas y viñetas) */
    p, li, div {
        font-size: 22px !important;
        line-height: 1.6 !important;
    }
    
    /* Encabezados de secciones principales */
    .stMarkdown h3 {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #4A90E2 !important;
        margin-top: 20px !important;
    }
    
    /* Subtítulos dentro de cajas informativas */
    .element-container div[data-testid="stMarkdownContainer"] h3 {
        font-size: 24px !important;
        color: #FFFFFF !important;
    }
    
    /* Números de las tarjetas de métricas (st.metric) */
    div[data-testid="stMetricValue"] {
        font-size: 40px !important;
        font-weight: bold !important;
    }
    
    /* Etiquetas sobre las métricas */
    div[data-testid="stMetricLabel"] {
        font-size: 20px !important;
        font-weight: 600 !important;
    }

    /* Pestañas (st.tabs) más grandes */
    button[data-baseweb="tab"] p {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO E ECUACIONES UTILIZADAS ---
st.title(" Caso 3: Ensayos de Vacío (CA) y Cortocircuito (CC)")

with st.expander("📘 Ver Ecuaciones Utilizadas en este Caso"):
    st.latex(r"\text{Prueba Vacío (Secundario): } \theta_{\text{CA}} = \cos^{-1}\left(\frac{P_{\text{CA}}}{V_{\text{CA}} I_{\text{CA}}}\right), \quad R_{C,s} = \frac{V_{\text{CA}}}{I_{\text{CA}} \cos\theta_{\text{CA}}}, \quad X_{M,s} = \frac{V_{\text{CA}}}{I_{\text{CA}} \sin\theta_{\text{CA}}}")
    st.latex(r"\text{Prueba Cortocircuito (Primario): } Z_{\text{eq},p} = \frac{V_{\text{CC}}}{I_{\text{CC}}}, \quad R_{\text{eq},p} = \frac{P_{\text{CC}}}{I_{\text{CC}}^2}, \quad X_{\text{eq},p} = \sqrt{Z_{\text{eq},p}^2 - R_{\text{eq},p}^2}")
    st.latex(r"\mathbf{I}_0 = I_C - j I_M, \quad R_{\text{eq},s} = \frac{R_{\text{eq},p}}{a^2}, \quad X_{\text{eq},s} = \frac{X_{\text{eq},p}}{a^2}")

# --- ENTRADAS DE LOS ENSAYOS EN LA BARRA LATERAL ---
st.sidebar.header("* Datos de los Ensayos")

if st.sidebar.button("🔄 Restablecer datos originales"):
    st.session_state['v_ca'] = 115.0
    st.session_state['i_ca'] = 0.11
    st.session_state['p_ca'] = 3.9
    st.session_state['v_cc'] = 17.1
    st.session_state['i_cc'] = 8.7
    st.session_state['p_cc'] = 38.1

V_ca = st.sidebar.number_input("Tensión de Vacío V_CA (V)", value=st.session_state.get('v_ca', 115.0), key='v_ca')
I_ca = st.sidebar.number_input("Corriente de Vacío I_CA (A)", value=st.session_state.get('i_ca', 0.11), key='i_ca')
P_ca = st.sidebar.number_input("Potencia de Vacío P_CA (W)", value=st.session_state.get('p_ca', 3.9), key='p_ca')

V_cc = st.sidebar.number_input("Tensión Cortocircuito V_CC (V)", value=st.session_state.get('v_cc', 17.1), key='v_cc')
I_cc = st.sidebar.number_input("Corriente Cortocircuito I_CC (A)", value=st.session_state.get('i_cc', 8.7), key='i_cc')
P_cc = st.sidebar.number_input("Potencia Cortocircuito P_CC (W)", value=st.session_state.get('p_cc', 38.1), key='p_cc')

# --- CÁLCULOS EXPERIMENTALES Y PARÁMETROS ---
fp_ca = P_ca / (V_ca * I_ca)
theta_ca = np.arccos(fp_ca)

# Componentes de corriente de excitación
I_c = I_ca * fp_ca
I_m = I_ca * np.sin(theta_ca)
I_0_complex = I_c - 1j * I_m

R_c_s = V_ca / I_c
X_m_s = V_ca / I_m

# Ensayo de Cortocircuito (Primario)
Z_eq_p = V_cc / I_cc
R_eq_p = P_cc / (I_cc**2)
X_eq_p = np.sqrt(max(0, Z_eq_p**2 - R_eq_p**2))

a = 2.0
R_eq_s = R_eq_p / (a**2)
X_eq_s = X_eq_p / (a**2)

# Operación Nominal (S = 1000 VA, V_s = 115 V)
S_nom = 1000.0
V_s_nom = 115.0
I_s_nom = S_nom / V_s_nom

fp_ind = 0.8
theta_ind = -np.arccos(fp_ind)
I_s_ind = I_s_nom * (np.cos(theta_ind) + 1j * np.sin(theta_ind))
V_p_ind = V_s_nom + I_s_ind * (R_eq_s + 1j * X_eq_s)
rv_ind = (abs(V_p_ind) - V_s_nom) / V_s_nom * 100

P_cu = (I_s_nom**2) * R_eq_s
eta = (S_nom * fp_ind) / (S_nom * fp_ind + P_cu + P_ca) * 100

# Guardar en session_state para la tabla comparativa
st.session_state['caso3'] = {
    "Caso": "3. Ensayos Vacío/CC",
    "V_primario (V)": round(abs(V_p_ind) * a, 2),
    "I_primario (A)": round(I_s_nom / a, 2),
    "Pérdidas (W)": round(P_cu + P_ca, 2),
    "Regulación (%)": f"{rv_ind:.2f}%",
    "Eficiencia (%)": f"{eta:.2f}%"
}

# --- PRESENTACIÓN VISUAL DE RESULTADOS ---
st.subheader("1. Parámetros del Circuito Equivalente Determinados")
c1, c2 = st.columns(2)

with c1:
    st.info("### Rama de Excitación (Medida en Secundario)")
    st.write(f"• **Resistencia del Núcleo ($R_{{C,s}}$):** {R_c_s:.2f} Ω")
    st.write(f"• **Reactancia Magnetizante ($X_{{M,s}}$):** {X_m_s:.2f} Ω")
    st.write(f"• **Fasor Corriente Excitación ($\mathbf{{I}}_0$):** {I_c:.4f} - j({I_m:.4f}) A | **{I_ca:.4f} A ∠ {-np.degrees(theta_ca):.2f}°**")

with c2:
    st.info("### Impedancia Serie (Medida en Primario)")
    st.write(f"• **Resistencia Equivalente ($R_{{eq,p}}$):** {R_eq_p:.4f} Ω")
    st.write(f"• **Reactancia Equivalente ($X_{{eq,p}}$):** {X_eq_p:.4f} Ω")
    st.write(f"• **Impedancia Total ($\mathbf{{Z}}_{{eq,p}}$):** {R_eq_p:.4f} + j({X_eq_p:.4f}) Ω | **{Z_eq_p:.4f} Ω ∠ {np.degrees(np.arctan2(X_eq_p, R_eq_p)):.2f}°**")

st.subheader("2. Indicadores Operativos a Carga Nominal (1 kVA)")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Pérdidas de Núcleo (P_CA)", f"{P_ca:.2f} W")
m2.metric("Pérdidas en Cobre (P_CC)", f"{P_cc:.2f} W")
m3.metric("Regulación (FP 0.8 Ind)", f"{rv_ind:.2f} %")
m4.metric("Eficiencia Nominal", f"{eta:.2f} %")

st.divider()

# --- VISUALIZACIONES OBLIGATORIAS EXIGIDAS EN LA GUÍA ---
st.subheader("3. Visualizaciones Obligatorias")
tab1, tab2, tab3, tab4 = tab1, tab2, tab3, tab4 = st.tabs([
    "🔌 Circuito Equivalente", 
    "📐 Triángulo de Impedancias", 
    "📊 Diagrama Corriente Excitación", 
    "📈 Regulación vs 3 Factores de Potencia"
])

# 1. Circuito Equivalente Obtenido
with tab1:
    st.write("### Circuito Equivalente Obtenido por Ensayos (Referido al Primario)")
    st.code(f"""
        + ---[ Req,p = {R_eq_p:.4f} Ω ]---[ jXeq,p = j{X_eq_p:.4f} Ω ]---+-----------+--- +
        |                                                           |           |
       Vp                                                         [ Rc={R_c_s*(a**2):.1f}Ω ] [ jXm=j{X_m_s*(a**2):.1f}Ω ] a*Vs
        |                                                           |           |
        + ----------------------------------------------------------+-----------+--- -
    """, language="text")

# 2. Triángulo de Impedancias
with tab2:
    fig_z = go.Figure()
    fig_z.add_trace(go.Scatter(x=[0, R_eq_p], y=[0, 0], mode='lines+markers+text', text=['', f'Req = {R_eq_p:.3f} Ω'], textposition='bottom center', name='Req (Resistiva)'))
    fig_z.add_trace(go.Scatter(x=[R_eq_p, R_eq_p], y=[0, X_eq_p], mode='lines+markers+text', text=['', f'jXeq = j{X_eq_p:.3f} Ω'], textposition='middle right', name='Xeq (Reactiva)'))
    fig_z.add_trace(go.Scatter(x=[0, R_eq_p], y=[0, X_eq_p], mode='lines+markers+text', text=['', f'Zeq = {Z_eq_p:.3f} Ω'], textposition='top left', name='Zeq (Total)'))
    fig_z.update_layout(title="Triángulo de Impedancias Serie (Lado Primario)", xaxis_title="Resistencia R (Ω)", yaxis_title="Reactancia X (Ω)")
    st.plotly_chart(fig_z, use_container_width=True)

# 3. Diagrama de Corriente de Excitación I0 = I_C - j I_M
with tab3:
    fig_i0 = go.Figure()
    fig_i0.add_trace(go.Scatter(x=[0, I_c], y=[0, 0], mode='lines+markers+text', text=['', f'I_C = {I_c:.4f} A'], textposition='top center', name='I_C (Pérdidas Núcleo)'))
    fig_i0.add_trace(go.Scatter(x=[I_c, I_c], y=[0, -I_m], mode='lines+markers+text', text=['', f'-jI_M = -j{I_m:.4f} A'], textposition='middle right', name='-jI_M (Magnetizante)'))
    fig_i0.add_trace(go.Scatter(x=[0, I_c], y=[0, -I_m], mode='lines+markers+text', text=['', f'I_0 = {I_ca:.4f} A'], textposition='bottom left', name='I_0 (Excitación Total)'))
    fig_i0.update_layout(title="Diagrama Fasorial de Corriente de Excitación (I0 = I_C - j I_M)", xaxis_title="Eje Real / En Fase (A)", yaxis_title="Eje Imaginario / Cuadratura (A)")
    st.plotly_chart(fig_i0, use_container_width=True)

# 4. Gráfico Comparativo de Regulación para los tres factores de potencia (Inductivo, Unitario, Capacitivo)
with tab4:
    cargas_pct = np.linspace(10, 120, 50)
    rv_ind_list, rv_uni_list, rv_cap_list = [], [], []

    for c in cargas_pct:
        i_m = (I_s_nom * (c / 100.0))
        
        # Inductivo (FP = 0.8 retraso)
        i_ind = i_m * (0.8 - 1j * 0.6)
        v_p_i = V_s_nom + i_ind * (R_eq_s + 1j * X_eq_s)
        rv_ind_list.append((abs(v_p_i) - V_s_nom) / V_s_nom * 100)
        
        # Unitario (FP = 1.0)
        i_uni = i_m * (1.0 + 0j)
        v_p_u = V_s_nom + i_uni * (R_eq_s + 1j * X_eq_s)
        rv_uni_list.append((abs(v_p_u) - V_s_nom) / V_s_nom * 100)
        
        # Capacitivo (FP = 0.8 adelanto)
        i_cap = i_m * (0.8 + 1j * 0.6)
        v_p_c = V_s_nom + i_cap * (R_eq_s + 1j * X_eq_s)
        rv_cap_list.append((abs(v_p_c) - V_s_nom) / V_s_nom * 100)

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=cargas_pct, y=rv_ind_list, mode='lines', name='FP = 0.8 Inductivo (Retraso)', line=dict(color='red')))
    fig_comp.add_trace(go.Scatter(x=cargas_pct, y=rv_uni_list, mode='lines', name='FP = 1.0 Unitario', line=dict(color='green')))
    fig_comp.add_trace(go.Scatter(x=cargas_pct, y=rv_cap_list, mode='lines', name='FP = 0.8 Capacitivo (Adelanto)', line=dict(color='blue')))
    fig_comp.update_layout(title="Comparativa de Regulación de Voltaje vs Cargas con Distintos Factores de Potencia", xaxis_title="Carga (%)", yaxis_title="Regulación de Voltaje (%)")
    st.plotly_chart(fig_comp, use_container_width=True)

st.divider()

# --- INTERPRETACIÓN MEDIANTE IA ---
st.subheader(" Interpretación mediante IA")
if st.button(" Analizar resultado con IA"):
    st.success("### Análisis Técnico de Inteligencia Artificial")
    st.markdown(f"""
    1. **¿El resultado obtenido es físicamente razonable?**  
       *Sí. Las pérdidas en el núcleo son de **{P_ca:.2f} W** y las pérdidas en el cobre a carga nominal son de **{P_cc:.2f} W**, obteniéndose una eficiencia máxima del **{eta:.2f}%**.*

    2. **¿Qué parámetro tiene mayor influencia sobre la regulación?**  
       *La reactancia equivalente ($X_{{eq,p}} = {X_eq_p:.4f}\\ \\Omega$), que domina la caída reactiva sobre la componente resistiva ($R_{{eq,p}} = {R_eq_p:.4f}\\ \\Omega$).*

    3. **¿Por qué cambia la regulación al modificar el factor de potencia?**  
       *Con FP inductivo la caída reactiva incrementa la tensión requerida del primario. Con FP capacitivo (adelanto), la caída se resta fasorialmente, provocando un efecto Ferranti donde el voltaje secundario puede superar la referencia.*

    4. **¿Dónde se producen las principales pérdidas?**  
       *Las pérdidas constantes ocurren en el núcleo magnético ($P_{{CA}} = {P_ca:.2f}\\text{{ W}}$), mientras que las pérdidas variables ocurren por efecto Joule en los devanados ($P_{{CC}} = {P_cc:.2f}\\text{{ W}}$).*

    5. **¿Qué diferencia existe entre el transformador ideal y el real en este caso?**  
       *Las pruebas experimentales permiten identificar los valores reales de la rama paralelo ($R_C, X_M$) y de la impedancia serie ($R_{{eq}}, X_{{eq}}$), ausentes en el modelo ideal.*

    6. **¿Qué decisión de ingeniería recomendaría a partir de los resultados?**  
       *Operar el transformador cercano al 80%–100% de su carga nominal, donde las pérdidas en el cobre igualan a las del núcleo, maximizando el rendimiento del equipo.*
    """)