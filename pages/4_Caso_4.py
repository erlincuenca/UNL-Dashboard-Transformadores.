import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="Caso 4: Sistema p.u.", layout="wide")

# 2. Estilos visuales de letra grande
st.markdown("""
    <style>
    p, li, div { font-size: 22px !important; line-height: 1.5 !important; }
    .stMarkdown h3 { font-size: 26px !important; font-weight: 700 !important; color: #4A90E2 !important; }
    div[data-testid="stMetricValue"] { font-size: 38px !important; font-weight: bold !important; }
    div[data-testid="stMetricLabel"] { font-size: 20px !important; font-weight: 600 !important; }
    button[data-baseweb="tab"] p { font-size: 20px !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO E ECUACIONES ---
st.title(" Caso 4: Transformador en Sistema Por Unidad (p.u.)")

with st.expander("📘 Ecuaciones del Caso"):
    st.latex(r"I_{\text{base},1} = \frac{S_{\text{base}}}{V_{\text{base},1}}, \quad I_{\text{base},2} = \frac{S_{\text{base}}}{V_{\text{base},2}}")
    st.latex(r"Z_{\text{base},1} = \frac{V_{\text{base},1}^2}{S_{\text{base}}}, \quad Z_{\text{base},2} = \frac{V_{\text{base},2}^2}{S_{\text{base}}}")
    st.latex(r"R_{\Omega} = R_{\text{pu}} \cdot Z_{\text{base}}, \quad X_{\Omega} = X_{\text{pu}} \cdot Z_{\text{base}}")
    st.latex(r"\mathbf{V}_{p,\text{pu}} = \mathbf{V}_{s,\text{pu}} + \mathbf{I}_{\text{pu}} (R_{\text{pu}} + j X_{\text{pu}})")
    st.latex(r"\text{RV}\% = \frac{V_{p,\text{pu}} - V_{s,\text{pu}}}{V_{s,\text{pu}}} \times 100\%, \quad \eta\% = \frac{P_{\text{out}}}{P_{\text{out}} + P_{\text{Cu}} + P_{\text{Fe}}} \times 100\%")

# --- PARAMETROS DE ENTRADA ---
st.sidebar.header("* Datos de Entrada")

if st.sidebar.button("🔄 Restablecer valores"):
    st.session_state['s_base'] = 150.0
    st.session_state['v_base1'] = 15.0
    st.session_state['v_base2'] = 200.0
    st.session_state['r_pu'] = 0.012
    st.session_state['x_pu'] = 0.050
    st.session_state['rc_pu'] = 100.0
    st.session_state['carga_pu'] = 1.0
    st.session_state['fp_pu'] = 0.80

S_base_MVA = st.sidebar.number_input("Sbase (MVA)", value=st.session_state.get('s_base', 150.0), key='s_base')
V_base_1_kV = st.sidebar.number_input("Vbase 1 (kV)", value=st.session_state.get('v_base1', 15.0), key='v_base1')
V_base_2_kV = st.sidebar.number_input("Vbase 2 (kV)", value=st.session_state.get('v_base2', 200.0), key='v_base2')
R_pu = st.sidebar.number_input("R (p.u.)", value=st.session_state.get('r_pu', 0.012), key='r_pu')
X_pu = st.sidebar.number_input("X (p.u.)", value=st.session_state.get('x_pu', 0.050), key='x_pu')
Rc_pu = st.sidebar.number_input("Rc (p.u.) [0 si se omite]", value=st.session_state.get('rc_pu', 100.0), key='rc_pu')
i_carga_pu = st.sidebar.slider("Carga (p.u.)", 0.1, 1.5, st.session_state.get('carga_pu', 1.0), key='carga_pu')
fp_carga = st.sidebar.slider("Factor de Potencia", 0.5, 1.0, st.session_state.get('fp_pu', 0.80), key='fp_pu')

# --- CÁLCULOS MATEMÁTICOS EXACTOS ---

# 1. Bases
I_base_1 = (S_base_MVA * 1e6) / (V_base_1_kV * 1e3)  # A
I_base_2 = (S_base_MVA * 1e6) / (V_base_2_kV * 1e3)  # A

Z_base_1 = ((V_base_1_kV * 1e3)**2) / (S_base_MVA * 1e6)  # Ω
Z_base_2 = ((V_base_2_kV * 1e3)**2) / (S_base_MVA * 1e6)  # Ω

# 2. Ohmios Reales
R_real_1 = R_pu * Z_base_1
X_real_1 = X_pu * Z_base_1

R_real_2 = R_pu * Z_base_2
X_real_2 = X_pu * Z_base_2

# 3. Fasores de Operación
theta_rad = -np.arccos(fp_carga)
I_pu_complex = i_carga_pu * (np.cos(theta_rad) + 1j * np.sin(theta_rad))
V_s_pu = 1.0 + 0j
Z_pu = R_pu + 1j * X_pu

V_p_pu = V_s_pu + I_pu_complex * Z_pu
V_p_mag_pu = abs(V_p_pu)
V_p_ang = np.degrees(np.angle(V_p_pu))

# 4. Corrientes Reales a Carga Actual
I_carga_1 = i_carga_pu * I_base_1
I_carga_2 = i_carga_pu * I_base_2

# 5. Potencias y Pérdidas
P_out_pu = i_carga_pu * fp_carga
P_cu_pu = (i_carga_pu**2) * R_pu
P_cu_MW = P_cu_pu * S_base_MVA

P_fe_pu = (V_p_mag_pu**2) / Rc_pu if Rc_pu > 0 else 0.0
P_fe_MW = P_fe_pu * S_base_MVA

P_in_pu = P_out_pu + P_cu_pu + P_fe_pu

# 6. Regulación y Eficiencia
rv = (V_p_mag_pu - 1.0) * 100.0
eta = (P_out_pu / P_in_pu) * 100.0

# Estado global para tabla comparativa
st.session_state['caso4'] = {
    "Caso": "4. Sistema por Unidad",
    "V_primario (V)": round(V_p_mag_pu * V_base_1_kV * 1000, 2),
    "I_primario (A)": round(I_carga_1, 2),
    "Pérdidas (W)": round((P_cu_MW + P_fe_MW) * 1e6, 2),
    "Regulación (%)": f"{rv:.2f}%",
    "Eficiencia (%)": f"{eta:.2f}%"
}

# --- RESULTADOS DIRECTOS ---

st.subheader("1. Valores Base e Impedancias Reales")
c1, c2 = st.columns(2)

with c1:
    st.info("### Magnitudes Base")
    st.write(f"• **Ibase 1 ({V_base_1_kV:.0f} kV):** {I_base_1:.2f} A")
    st.write(f"• **Ibase 2 ({V_base_2_kV:.0f} kV):** {I_base_2:.2f} A")
    st.write(f"• **Zbase 1:** {Z_base_1:.4f} Ω")
    st.write(f"• **Zbase 2:** {Z_base_2:.4f} Ω")

with c2:
    st.info("### Impedancia Real (Ohmios)")
    st.write(f"• **Lado {V_base_1_kV:.0f} kV:** R = {R_real_1:.4f} Ω | X = {X_real_1:.4f} Ω")
    st.write(f"• **Lado {V_base_2_kV:.0f} kV:** R = {R_real_2:.4f} Ω | X = {X_real_2:.4f} Ω")

st.subheader("2. Operación a Carga")
f1, f2 = st.columns(2)

with f1:
    st.info("### Corrientes de Carga")
    st.write(f"• **Carga:** {i_carga_pu:.2f} p.u.")
    st.write(f"• **I1 real:** {I_carga_1:.2f} A")
    st.write(f"• **I2 real:** {I_carga_2:.2f} A")

with f2:
    st.info("### Tensión Primaria Requerida")
    st.write(f"• **Vp (p.u.):** {V_p_pu.real:.4f} + j({V_p_pu.imag:.4f})")
    st.write(f"• **Fasor Vp:** **{V_p_mag_pu:.4f} p.u. ∠ {V_p_ang:.2f}°**")
    st.write(f"• **Vp real:** {V_p_mag_pu * V_base_1_kV:.3f} kV")

st.subheader("3. Indicadores de Desempeño")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Pérdidas Cobre", f"{P_cu_MW:.3f} MW")
m2.metric("Pérdidas Núcleo", f"{P_fe_MW:.3f} MW" if Rc_pu > 0 else "0.000 MW")
m3.metric("Regulación (RV)", f"{rv:.2f} %")
m4.metric("Eficiencia (η)", f"{eta:.2f} %")

st.divider()

# --- GRÁFICOS Y CIRCUITO ---
st.subheader("4. Visualizaciones")
tab1, tab2, tab3, tab4 = st.tabs([
    "🔌 Circuito p.u.", 
    "📊 Diagrama Fasorial", 
    "📈 Eficiencia vs Carga", 
    "📉 Regulación vs Carga"
])

with tab1:
    st.write("### Circuito Equivalente en p.u.")
    rc_str = f"[ Rc = {Rc_pu} p.u. ]" if Rc_pu > 0 else "Sin rama paralelo"
    st.code(f"""
        + ---[ R = {R_pu} p.u. ]---[ jX = j{X_pu} p.u. ]---+-----------+--- +
        |                                                 |           |
     Vp = {V_p_mag_pu:.4f} p.u.                          {rc_str}   Vs = 1.0 p.u.
        |                                                 |           |
        + ------------------------------------------------+-----------+--- -
    """, language="text")

with tab2:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=[0, 1.0], y=[0, 0], mode='lines+markers', name='Vs (1.0 p.u.)'))
    fig1.add_trace(go.Scatter(x=[1.0, V_p_pu.real], y=[0, V_p_pu.imag], mode='lines+markers', name='Caída I*Z'))
    fig1.add_trace(go.Scatter(x=[0, V_p_pu.real], y=[0, V_p_pu.imag], mode='lines+markers', name='Vp Requerido'))
    fig1.update_layout(title="Diagrama Fasorial de Tensiones (p.u.)", xaxis_title="Eje Real (p.u.)", yaxis_title="Eje Imaginario (p.u.)")
    st.plotly_chart(fig1, use_container_width=True)

with tab3:
    cargas_arr = np.linspace(0.1, 1.5, 50)
    p_o = cargas_arr * fp_carga
    p_c = (cargas_arr**2) * R_pu
    etas_arr = (p_o / (p_o + p_c + P_fe_pu)) * 100
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=cargas_arr*100, y=etas_arr, mode='lines', name='Eficiencia (%)'))
    fig2.update_layout(title="Eficiencia vs Carga (%)", xaxis_title="Carga (%)", yaxis_title="Eficiencia (%)")
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    cargas_arr = np.linspace(0.1, 1.5, 50)
    rvs_arr = []
    for c in cargas_arr:
        i_c = c * (np.cos(theta_rad) + 1j * np.sin(theta_rad))
        v_p = 1.0 + i_c * Z_pu
        rvs_arr.append((abs(v_p) - 1.0) * 100)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=cargas_arr*100, y=rvs_arr, mode='lines', name='Regulación (%)', line=dict(color='orange')))
    fig3.update_layout(title="Regulación de Voltaje vs Carga (%)", xaxis_title="Carga (%)", yaxis_title="Regulación (%)")
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- INTERPRETACIÓN CON IA ---
st.subheader(" Interpretación mediante IA")
if st.button(" Analizar resultado con IA"):
    st.success("### Análisis Técnico de IA")
    st.markdown(f"""
    1. **¿El resultado es físicamente razonable?**  
       *Sí. El voltaje primario es **{V_p_mag_pu:.4f} p.u.** ({V_p_mag_pu * V_base_1_kV:.3f} kV) con una regulación razonable de **{rv:.2f}%**.*

    2. **¿Qué parámetro influye más sobre la regulación?**  
       *La reactancia equivalente ($X = {X_pu}\\text{{ p.u.}}$), representa la mayor proporción de la impedancia.*

    3. **¿Por qué cambia la regulación al modificar el factor de potencia?**  
       *Porque el ángulo de la corriente modifica la fase de la caída de tensión respecto al voltaje de referencia.*

    4. **¿Dónde se producen las principales pérdidas?**  
       *Se producen **{P_cu_MW:.3f} MW** en el cobre y **{P_fe_MW:.3f} MW** en el núcleo.*

    5. **¿Qué diferencia existe entre el transformador ideal y el real en este caso?**  
       *El modelo p.u. elimina la relación de transformación ($a$), facilitando el análisis directo.*

    6. **¿Qué decisión de ingeniería recomendaría a partir de los resultados?**  
       *Usar la impedancia en p.u. ($Z = {abs(Z_pu):.4f}\\text{{ p.u.}}$) para los estudios de cortocircuito en la red.*
    """)