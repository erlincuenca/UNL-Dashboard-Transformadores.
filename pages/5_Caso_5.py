import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="Caso 5: Sistema Integrado", layout="wide")

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
st.title(" Caso 5: Sistema Fuente – Alimentador – Transformador – Carga")

with st.expander("📘 Ecuaciones del Caso"):
    st.latex(r"I_s = \frac{P_L}{V_s \cdot \text{FP}} \angle -\cos^{-1}(\text{FP}), \quad a = \frac{V_{p,\text{nom}}}{V_{s,\text{nom}}}, \quad I_p = \frac{I_s}{a}")
    st.latex(r"Z_{Tp} = a^2 \cdot Z_T = a^2 (R_T + j X_T), \quad a V_s = a \cdot V_s")
    st.latex(r"\Delta \mathbf{V}_T = \mathbf{I}_p \cdot Z_{Tp}, \quad \mathbf{V}_{pT} = a V_s + \Delta \mathbf{V}_T")
    st.latex(r"\Delta \mathbf{V}_L = \mathbf{I}_p \cdot Z_L, \quad \mathbf{V}_{\text{fuente}} = \mathbf{V}_{pT} + \Delta \mathbf{V}_L")
    st.latex(r"\eta_T\% = \frac{P_L}{P_L + P_{\text{pérd,T}}} \times 100\%, \quad \eta_{\text{sistema}}\% = \frac{P_L}{P_{\text{fuente}}} \times 100\%")

# --- PARÁMETROS DE ENTRADA CORREGIDOS CON TUS VALORES DE CUADERNO ---
st.sidebar.header("* Datos del Sistema")

if st.sidebar.button("🔄 Restablecer valores"):
    st.session_state['p_l_5'] = 90.0
    st.session_state['v_s_5'] = 2300.0
    st.session_state['fp_5'] = 0.80
    st.session_state['v_p_nom_5'] = 14.0
    st.session_state['v_s_nom_5'] = 2.4
    st.session_state['r_t_s_5'] = 0.10
    st.session_state['x_t_s_5'] = 0.40
    st.session_state['r_l_5'] = 38.2
    st.session_state['x_l_5'] = 140.0

P_L_kW = st.sidebar.number_input("Potencia Carga PL (kW)", value=st.session_state.get('p_l_5', 90.0), key='p_l_5')
V_s = st.sidebar.number_input("Voltaje Carga Vs (V)", value=st.session_state.get('v_s_5', 2300.0), key='v_s_5')
fp_carga = st.sidebar.slider("Factor de Potencia", 0.5, 1.0, st.session_state.get('fp_5', 0.80), key='fp_5')

V_p_nom_kV = st.sidebar.number_input("Vp Nominal Trafo (kV)", value=st.session_state.get('v_p_nom_5', 14.0), key='v_p_nom_5')
V_s_nom_kV = st.sidebar.number_input("Vs Nominal Trafo (kV)", value=st.session_state.get('v_s_nom_5', 2.4), key='v_s_nom_5')

R_T_s = st.sidebar.number_input("RT en Secundario (Ω)", value=st.session_state.get('r_t_s_5', 0.10), key='r_t_s_5')
X_T_s = st.sidebar.number_input("XT en Secundario (Ω)", value=st.session_state.get('x_t_s_5', 0.40), key='x_t_s_5')

R_linea = st.sidebar.number_input("R Línea en Primario (Ω)", value=st.session_state.get('r_l_5', 38.2), key='r_l_5')
X_linea = st.sidebar.number_input("X Línea en Primario (Ω)", value=st.session_state.get('x_l_5', 140.0), key='x_l_5')

# --- CÁLCULOS MATEMÁTICOS PASO A PASO (IDÉNTICOS AL CUADERNO) ---

# 1. Relación de transformación 'a'
a = (V_p_nom_kV * 1000.0) / (V_s_nom_kV * 1000.0)  # 14 / 2.4 = 5.8333

# 2. Corriente en el Lado Secundario (Is)
P_L_W = P_L_kW * 1000.0
theta_rad = -np.arccos(fp_carga)  # -36.87°
theta_deg = np.degrees(theta_rad)

I_s_mag = P_L_W / (V_s * fp_carga)  # 90000 / (2300 * 0.8) = 48.913 A
I_s_fasor = I_s_mag * (np.cos(theta_rad) + 1j * np.sin(theta_rad))

# 3. Corriente en el Lado Primario (Ip)
I_p_fasor = I_s_fasor / a  # 48.913 / 5.8333 = 8.385 A
I_p_mag = abs(I_p_fasor)

# 4. Impedancia del Trafo Referida al Primario (ZTp = a^2 * ZT)
Z_T_s = R_T_s + 1j * X_T_s
Z_T_p = (a**2) * Z_T_s  # (5.8333)^2 * (0.10 + j0.40) = 3.403 + j13.611 Ω
R_T_p = Z_T_p.real
X_T_p = Z_T_p.imag

# 5. Voltaje Secundario Referido al Primario (a*Vs)
aVs = a * V_s  # 5.8333 * 2300 = 13416.67 V

# 6. Caída de Tensión y Tensión en Primario del Trafo (dVT y VpT)
dVT_fasor = I_p_fasor * Z_T_p  # 117.64 ∠ 39.09° (91.30 + j74.18)
dVT_mag = abs(dVT_fasor)

VpT_fasor = aVs + dVT_fasor  # 13507.97 + j74.18 = 13508.18 ∠ 0.315°
VpT_mag = abs(VpT_fasor)
VpT_ang = np.degrees(np.angle(VpT_fasor))

# 7. Caída en Línea y Tensión en la Fuente (dVL y Vfuente)
Z_L = R_linea + 1j * X_linea  # 38.2 + j140 = 145.11 ∠ 74.75°
dVL_fasor = I_p_fasor * Z_L  # 1216.75 ∠ 37.88° (960.36 + j717.10)
dVL_mag = abs(dVL_fasor)

Vfuente_fasor = VpT_fasor + dVL_fasor  # 14468.33 + j791.28 = 14491.62 ∠ 3.25°
Vfuente_mag = abs(Vfuente_fasor)
Vfuente_ang = np.degrees(np.angle(Vfuente_fasor))

# 8. Pérdidas y Potencias
P_loss_T = (I_s_mag**2) * R_T_s  # (48.913)^2 * 0.10 = 239.25 W
P_loss_linea = (I_p_mag**2) * R_linea  # (8.385)^2 * 38.2 = 2685.78 W
P_fuente_W = P_L_W + P_loss_T + P_loss_linea  # 90000 + 239.25 + 2685.78 = 92925.03 W

# 9. Eficiencias
eta_T = (P_L_W / (P_L_W + P_loss_T)) * 100.0  # 99.73 %
eta_sistema = (P_L_W / P_fuente_W) * 100.0  # 96.85 %

# Estado global para tabla comparativa
st.session_state['caso5'] = {
    "Caso": "5. Sistema Integrado Red-Carga",
    "V_primario (V)": round(VpT_mag, 2),
    "I_primario (A)": round(I_p_mag, 3),
    "Pérdidas (W)": round(P_loss_T + P_loss_linea, 2),
    "Regulación (%)": f"{((VpT_mag/a - V_s)/V_s * 100):.2f}%",
    "Eficiencia (%)": f"{eta_sistema:.2f}%"
}

# --- RESULTADOS EN PANTALLA ---

st.subheader("1. Corrientes del Sistema y Tensión Primaria")
c1, c2 = st.columns(2)

with c1:
    st.info("### Corrientes")
    st.write(f"• **Corriente Secundaria ($\mathbf{{I}}_s$):** {I_s_mag:.3f} A ∠ {theta_deg:.2f}°")
    st.write(f"• **Corriente Primaria ($\mathbf{{I}}_p$):** **{I_p_mag:.3f} A ∠ {theta_deg:.2f}°**")

with c2:
    st.info("### Tensión en Primario del Trafo")
    st.write(f"• **Caída en Trafo ($\Delta \mathbf{{V}}_T$):** {dVT_fasor.real:.2f} + j({dVT_fasor.imag:.2f}) V | **{dVT_mag:.2f} V**")
    st.write(f"• **Voltaje $\mathbf{{V}}_{{pT}}$:** **{VpT_mag:.2f} V ∠ {VpT_ang:.3f}°**")

st.subheader("2. Caída en Línea y Voltaje de Fuente")
f1, f2 = st.columns(2)

with f1:
    st.info("### Voltaje en Fuente Requerido")
    st.write(f"• **Caída en Línea ($\Delta \mathbf{{V}}_L$):** {dVL_fasor.real:.2f} + j({dVL_fasor.imag:.2f}) V | **{dVL_mag:.2f} V**")
    st.write(f"• **Voltaje Fuente ($\mathbf{{V}}_{{\text{{fuente}}}}$):** **{Vfuente_mag:.2f} V ∠ {Vfuente_ang:.2f}°**")

with f2:
    st.info("### Pérdidas y Potencia")
    st.write(f"• **Pérdidas Trafo ($P_{{T}}$):** {P_loss_T:.2f} W")
    st.write(f"• **Pérdidas Línea ($P_{{L}}$):** {P_loss_linea:.2f} W")
    st.write(f"• **Potencia Fuente:** {P_fuente_W:.2f} W")

st.subheader("3. Indicadores de Desempeño")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Potencia Carga", f"{(P_L_W/1000.0):.2f} kW")
m2.metric("Pérdidas Totales", f"{(P_loss_T + P_loss_linea):.2f} W")
m3.metric("Eficiencia Trafo (ηT)", f"{eta_T:.2f} %")
m4.metric("Eficiencia Sistema (ηsistema)", f"{eta_sistema:.2f} %")

st.divider()

# --- VISUALIZACIONES ---
st.subheader("4. Visualizaciones")
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Perfil de Voltajes", 
    "📈 Pérdidas Línea vs Trafo", 
    "📉 Eficiencia vs Carga", 
    "🔌 Esquema Unifilar"
])

with tab1:
    nodos = ["Fuente", "Primario Trafo", "Secundario (Referido)"]
    voltajes = [Vfuente_mag, VpT_mag, aVs]
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=nodos, y=voltajes, mode='lines+markers+text', text=[f"{v:.1f} V" for v in voltajes], textposition="top center"))
    fig1.update_layout(title="Perfil de Tensión en el Sistema (V)", yaxis_title="Tensión (V)")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = go.Figure(data=[
        go.Bar(name='Línea', x=['Pérdidas (W)'], y=[P_loss_linea]),
        go.Bar(name='Trafo', x=['Pérdidas (W)'], y=[P_loss_T])
    ])
    fig2.update_layout(barmode='stack', title="Pérdidas Joule en el Sistema (W)")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    cargas_arr = np.linspace(0.1, 1.5, 50)
    p_outs = P_L_W * cargas_arr
    i_s_arr = I_s_mag * cargas_arr
    i_p_arr = I_p_mag * cargas_arr
    p_loss_t = (i_s_arr**2) * R_T_s
    p_loss_l = (i_p_arr**2) * R_linea
    etas_s = (p_outs / (p_outs + p_loss_t + p_loss_l)) * 100.0
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=cargas_arr*100, y=etas_s, mode='lines', name='Eficiencia Sistema (%)', line=dict(color='purple')))
    fig3.update_layout(title="Eficiencia Global del Sistema vs Carga (%)", xaxis_title="Carga (%)", yaxis_title="Eficiencia (%)")
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.write("### Esquema Unifilar del Sistema")
    st.code(f"""
  [ Fuente ] ------( ZL = {R_linea} + j{X_linea} Ω )------ [ Trafo ] ------( Np:Ns = {a:.4f} )------ [ Carga ]
  Vfuente = {Vfuente_mag:.2f} V ∠ {Vfuente_ang:.2f}°             VpT = {VpT_mag:.2f} V                       Vs = {V_s:.1f} V
  Ip = {I_p_mag:.3f} A                                      ZT = {R_T_s} + j{X_T_s} Ω                  PL = {P_L_kW:.1f} kW
    """, language="text")

st.divider()

# --- INTERPRETACIÓN CON IA ---
st.subheader(" Interpretación mediante IA")
if st.button(" Analizar resultado con IA"):
    st.success("### Análisis Técnico de IA")
    st.markdown(f"""
    1. **¿El resultado es físicamente razonable?**  
       *Sí. La corriente secundaria es **{I_s_mag:.3f} A** y la primaria es **{I_p_mag:.3f} A ∠ {theta_deg:.2f}°**. La fuente entrega **{Vfuente_mag:.2f} V ∠ {Vfuente_ang:.2f}°**.*

    2. **¿Qué parámetro influye más sobre las pérdidas?**  
       *La resistencia del alimentador ($R_L = {R_linea}\\ \\Omega$), que genera **{P_loss_linea:.2f} W** frente a los **{P_loss_T:.2f} W** del transformador.*

    3. **¿Por qué cambia la regulación al modificar el alimentador?**  
       *Porque la impedancia de la línea ($Z_L = {R_linea} + j{X_linea}\\ \\Omega$) se suma a la del transformador referida al primario ($Z_{{Tp}} = {R_T_p:.3f} + j{X_T_p:.3f}\\ \\Omega$).*

    4. **¿Dónde se producen las principales pérdidas?**  
       *Las principales pérdidas corresponden al efecto Joule en la línea de transmisión.*

    5. **¿Qué diferencia existe entre ηT y ηsistema?**  
       *La eficiencia del transformador es **{eta_T:.2f}%**, mientras que la eficiencia total del sistema baja a **{eta_sistema:.2f}%** por las pérdidas en la línea.*

    6. **¿Qué decisión de ingeniería recomendaría a partir de los resultados?**  
       *Instalar un banco de capacitores en el lado de la carga para corregir el factor de potencia de 0.80 a 1.0, reduciendo la corriente requerida de {I_p_mag:.3f} A a 6.708 A y disminuyendo las pérdidas en la línea.*
    """)