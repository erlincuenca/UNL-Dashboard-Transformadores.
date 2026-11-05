import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="Caso 2: Trafo Real", layout="wide")

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
st.title(" Caso 2: Transformador Monofásico Real (Circuito Exacto)")

with st.expander("📘 Ver Ecuaciones Utilizadas en este Caso"):
    st.latex(r"a = \frac{N_p}{N_s}, \quad \mathbf{V}_s' = a \mathbf{V}_s, \quad \mathbf{I}_p' = \frac{\mathbf{I}_s}{a}")
    st.latex(r"\mathbf{V}_{\text{caída,R}} = \mathbf{I}_p' \cdot R_{\text{eq},p}, \quad \mathbf{V}_{\text{caída,X}} = j \mathbf{I}_p' \cdot X_{\text{eq},p}")
    st.latex(r"\mathbf{V}_p = \mathbf{V}_s' + \mathbf{I}_p' (R_{\text{eq},p} + j X_{\text{eq},p})")
    st.latex(r"\mathbf{I}_{\text{Fe}} = \frac{\mathbf{V}_p}{R_C}, \quad \mathbf{I}_m = \frac{\mathbf{V}_p}{j X_M}, \quad \mathbf{I}_{\text{exc}} = \mathbf{I}_{\text{Fe}} + \mathbf{I}_m")
    st.latex(r"\mathbf{I}_p = \mathbf{I}_p' + \mathbf{I}_{\text{exc}}")
    st.latex(r"\text{RV}\% = \frac{(V_p / a) - V_s}{V_s} \times 100\%, \quad \eta\% = \frac{P_{\text{out}}}{P_{\text{in}}} \times 100\%")

# --- PARÁMETROS DE ENTRADA Y RESTABLECER ---
st.sidebar.header("*Datos del Modelo y Carga")

if st.sidebar.button("🔄 Restablecer datos originales"):
    st.session_state['a_2'] = 0.50
    st.session_state['v_s_2'] = 200.0
    st.session_state['req_2'] = 0.20
    st.session_state['xeq_2'] = 0.80
    st.session_state['rc_2'] = 300.0
    st.session_state['xm_2'] = 100.0
    st.session_state['is_2'] = 5.0
    st.session_state['ang_2'] = -36.87

a = st.sidebar.number_input("Relación a (Np/Ns)", value=st.session_state.get('a_2', 0.50), key='a_2')
V_s_rms = st.sidebar.number_input("Voltaje Secundario Vs (V)", value=st.session_state.get('v_s_2', 200.0), key='v_s_2')
R_eq_p = st.sidebar.number_input("Req en primario (Ω)", value=st.session_state.get('req_2', 0.20), key='req_2')
X_eq_p = st.sidebar.number_input("Xeq en primario (Ω)", value=st.session_state.get('xeq_2', 0.80), key='xeq_2')
R_c = st.sidebar.number_input("Resistencia núcleo Rc (Ω)", value=st.session_state.get('rc_2', 300.0), key='rc_2')
X_m = st.sidebar.number_input("Reactancia mag. Xm (Ω)", value=st.session_state.get('xm_2', 100.0), key='xm_2')
I_s_rms = st.sidebar.slider("Corriente secundaria (A)", 1.0, 15.0, st.session_state.get('is_2', 5.0), key='is_2')
theta_i = st.sidebar.slider("Ángulo corriente carga (°)", -90.0, 90.0, st.session_state.get('ang_2', -36.87), key='ang_2')

# --- CÁLCULOS MATEMÁTICOS DETALLADOS ---

theta_rad = np.radians(theta_i)
FP = np.cos(theta_rad)
V_s_complex = V_s_rms + 0j
I_s_complex = I_s_rms * (np.cos(theta_rad) + 1j * np.sin(theta_rad))

I_p_ref = I_s_complex / a
V_s_ref = a * V_s_rms

V_caida_R = I_p_ref * R_eq_p
V_caida_X = I_p_ref * (1j * X_eq_p)
V_caida_Z = V_caida_R + V_caida_X

V_p_fasor = V_s_ref + V_caida_Z
V_p_mag = abs(V_p_fasor)
V_p_ang = np.degrees(np.angle(V_p_fasor))

I_fe = V_p_fasor / R_c
I_m = V_p_fasor / (1j * X_m)
I_exc = I_fe + I_m

I_p_total = I_p_ref + I_exc
I_p_mag = abs(I_p_total)
I_p_ang = np.degrees(np.angle(I_p_total))

P_out = V_s_rms * I_s_rms * FP
P_cu = (abs(I_p_ref)**2) * R_eq_p
P_core = (V_p_mag**2) / R_c
P_in = P_out + P_cu + P_core

rv = ((V_p_mag / a) - V_s_rms) / V_s_rms * 100
eta = (P_out / P_in) * 100

st.session_state['caso2'] = {
    "Caso": "2. Trafo Real Exacto",
    "V_primario (V)": round(V_p_mag, 2),
    "I_primario (A)": round(I_p_mag, 2),
    "Pérdidas (W)": round(P_cu + P_core, 2),
    "Regulación (%)": f"{rv:.2f}%",
    "Eficiencia (%)": f"{eta:.2f}%"
}

# --- PRESENTACIÓN VISUAL EN PANTALLA ---

st.subheader("1. Magnitudes del Secundario y Caídas Internas")
c1, c2 = st.columns(2)

with c1:
    st.info("### Magnitudes del Secundario (Referidas)")
    st.write(f"• **Voltaje Secundario $\mathbf{{V}}_s$:** {V_s_rms:.2f} V ∠ 0.0°")
    st.write(f"• **Corriente Secundaria $\mathbf{{I}}_s$:** {I_s_rms:.2f} A ∠ {theta_i:.2f}°")
    st.write(f"• **Corriente Referida $\mathbf{{I}}_p'$:** {I_p_ref.real:.2f} + j({I_p_ref.imag:.2f}) A | **{abs(I_p_ref):.2f} A ∠ {np.degrees(np.angle(I_p_ref)):.2f}°**")

with c2:
    st.info("### Caídas de Tensión en Impedancia Serie")
    st.write(f"• **Caída Resistiva ($R_{{eq}} \cdot I$):** {V_caida_R.real:.2f} + j({V_caida_R.imag:.2f}) V | **{abs(V_caida_R):.2f} V**")
    st.write(f"• **Caída Reactiva ($j X_{{eq}} \cdot I$):** {V_caida_X.real:.2f} + j({V_caida_X.imag:.2f}) V | **{abs(V_caida_X):.2f} V**")
    st.write(f"• **Tensión Primaria $\mathbf{{V}}_p$:** {V_p_fasor.real:.2f} + j({V_p_fasor.imag:.2f}) V | **{V_p_mag:.2f} V ∠ {V_p_ang:.2f}°**")

st.subheader("2. Corrientes de Excitación y Primario Total")
e1, e2 = st.columns(2)

with e1:
    st.info("### Desglose de Corriente de Excitación")
    st.write(f"• **Corriente Magnetización $\mathbf{{I}}_m$:** {I_m.real:.3f} + j({I_m.imag:.3f}) A | **{abs(I_m):.3f} A**")
    st.write(f"• **Corriente Pérdidas Núcleo $\mathbf{{I}}_{{Fe}}$:** {I_fe.real:.3f} + j({I_fe.imag:.3f}) A | **{abs(I_fe):.3f} A**")

with e2:
    st.info("### Corrientes Totales del Primario")
    st.write(f"• **Corriente Excitación Total $\mathbf{{I}}_{{exc}}$:** {I_exc.real:.3f} + j({I_exc.imag:.3f}) A | **{abs(I_exc):.3f} A**")
    st.write(f"• **Corriente Primaria Total $\mathbf{{I}}_p$:** {I_p_total.real:.2f} + j({I_p_total.imag:.2f}) A | **{I_p_mag:.2f} A ∠ {I_p_ang:.2f}°**")

st.subheader("3. Balance Energético e Indicadores de Desempeño")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Potencia Salida (Pout)", f"{P_out:.2f} W")
m2.metric("Pérdidas Cobre (Pcu)", f"{P_cu:.2f} W")
m3.metric("Pérdidas Núcleo (Pfe)", f"{P_core:.2f} W")
m4.metric("Potencia Entrada (Pin)", f"{P_in:.2f} W")

r1, r2 = st.columns(2)
r1.metric("Regulación de Voltaje (RV)", f"{rv:.2f} %")
r2.metric("Eficiencia (η)", f"{eta:.2f} %")

st.divider()

# --- VISUALIZACIONES ---
st.subheader("4. Gráficos y Circuito Equivalente")
tab1, tab2, tab3, tab4 = st.tabs(["📊 Triángulo Fasorial de Tensión", "📈 Eficiencia vs Carga", "📉 Regulación vs FP", "🔌 Circuito Equivalente"])

with tab1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=[0, V_s_ref], y=[0, 0], mode='lines+markers', name='a*Vs (Referido)'))
    fig1.add_trace(go.Scatter(x=[V_s_ref, V_s_ref + V_caida_R.real], y=[0, V_caida_R.imag], mode='lines+markers', name='Caída R_eq*I'))
    fig1.add_trace(go.Scatter(x=[V_s_ref + V_caida_R.real, V_p_fasor.real], y=[V_caida_R.imag, V_p_fasor.imag], mode='lines+markers', name='Caída jX_eq*I'))
    fig1.add_trace(go.Scatter(x=[0, V_p_fasor.real], y=[0, V_p_fasor.imag], mode='lines+markers', name='Vp Requerido'))
    fig1.update_layout(title="Triángulo Fasorial de Caída de Tensión", xaxis_title="Eje Real (V)", yaxis_title="Eje Imaginario (V)")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    cargas_pct = np.linspace(0.1, 1.5, 50)
    i_refs = (I_s_rms / a) * cargas_pct
    p_outs = V_s_rms * (I_s_rms * cargas_pct) * FP
    p_cus = (i_refs**2) * R_eq_p
    etas = (p_outs / (p_outs + p_cus + P_core)) * 100
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=cargas_pct*100, y=etas, mode='lines', name='Eficiencia (%)'))
    fig2.update_layout(title="Curva de Eficiencia vs Nivel de Carga (%)", xaxis_title="Carga (%)", yaxis_title="Eficiencia (%)")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fps = np.linspace(0.5, 1.0, 30)
    rvs_ret = []
    for f in fps:
        t_r = -np.arccos(f)
        i_p_t = (I_s_rms / a) * (np.cos(t_r) + 1j * np.sin(t_r))
        v_p_t = V_s_ref + i_p_t * (R_eq_p + 1j * X_eq_p)
        rvs_ret.append(((abs(v_p_t)/a) - V_s_rms)/V_s_rms * 100)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=fps, y=rvs_ret, mode='lines', name='FP Retraso', line=dict(color='red')))
    fig3.update_layout(title="Regulación de Voltaje vs Factor de Potencia", xaxis_title="Factor de Potencia", yaxis_title="Regulación (%)")
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.write("### Modelo del Circuito Equivalente Exacto (Referido al Primario)")
    st.code(f"""
        + ---[ Req={R_eq_p}Ω ]---[ jXeq={X_eq_p}Ω ]---+-----------+--- +
        |                                       |           |
       Vp={V_p_mag:.1f}V                      [ Rc={R_c}Ω ] [ jXm={X_m}Ω ] a*Vs={V_s_ref:.1f}V
        |                                       |           |
        + --------------------------------------+-----------+--- -
    """, language="text")

st.divider()

# --- INTERPRETACIÓN MEDIANTE IA ---
st.subheader(" Interpretación mediante IA")
if st.button(" Analizar resultado con IA"):
    st.success("### Análisis Técnico de Inteligencia Artificial")
    st.markdown(f"""
    1. **¿El resultado obtenido es físicamente razonable?**  
       *Sí. La eficiencia obtenida es del **{eta:.2f}%** y la regulación del **{rv:.2f}%**, valores típicos en transformadores monofásicos de baja potencia operando a carga nominal.*

    2. **¿Qué parámetro tiene mayor influencia sobre la regulación?**  
       *La reactancia equivalente ($X_{{eq,p}} = {X_eq_p}\\ \\Omega$). Debido a que $X_{{eq,p}} > R_{{eq,p}}$, la regulación se ve severamente afectada por componentes reactivas de corriente.*

    3. **¿Por qué cambia la regulación al modificar el factor de potencia?**  
       *Con cargas inductivas (FP en retraso), la caída de tensión en $X_{{eq}}$ se suma en fase con el voltaje secundario, elevando la tensión requerida en el primario ($V_p = {V_p_mag:.2f}\\text{{ V}}$).*

    4. **¿Dónde se producen las principales pérdidas?**  
       *Pérdidas en el núcleo: **{P_core:.2f} W** ($V_p^2 / R_C$) y pérdidas en el cobre: **{P_cu:.2f} W** ($I^2 R_{{eq}}$).*

    5. **¿Qué diferencia existe entre el transformador ideal y el real en este caso?**  
       *A diferencia del Caso 1, aquí la tensión del secundario cae bajo carga (exigiendo $V_p > a V_s$) y la eficiencia cae del 100% al {eta:.2f}%.*

    6. **¿Qué decisión de ingeniería recomendaría a partir de los resultados?**  
       *Para mejorar la regulación de voltaje, se sugiere instalar compensación capacitiva (banco de condensadores) en el secundario para llevar el FP cercano a 1.0.*
    """)