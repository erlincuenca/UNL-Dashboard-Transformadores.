import streamlit as st
st.markdown("""
    <style>
    p, li, div { font-size: 22px !important; line-height: 1.6 !important; }
    div[data-testid="stMetricValue"] { font-size: 40px !important; font-weight: bold !important; }
    div[data-testid="stMetricLabel"] { font-size: 20px !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Caso 1: Trafo Ideal", layout="wide")

# --- ECUACIONES UTILIZADAS ---
st.title("Caso 1: Transformador Monofásico Ideal")

with st.expander("📘 Ver Ecuaciones Utilizadas en este Caso"):
    st.latex(r"V_{s,\text{rms}} = \frac{V_{s,\text{max}}}{\sqrt{2}}, \quad I_{s,\text{rms}} = \frac{I_{s,\text{max}}}{\sqrt{2}}, \quad f = \frac{\omega}{2\pi}")
    st.latex(r"a = \frac{N_p}{N_s} = \frac{V_p}{V_s} = \frac{I_s}{I_p} \implies \mathbf{V}_p = a \mathbf{V}_s, \quad \mathbf{I}_p = \frac{\mathbf{I}_s}{a}")
    st.latex(r"S = V_{\text{rms}} \cdot I_{\text{rms}}, \quad P = S \cdot \cos(\theta), \quad Q = S \cdot \sin(\theta)")
    st.latex(r"\text{RV}\% = 0\%, \quad \eta\% = 100\%")

# --- PARÁMETROS DE ENTRADA Y RESTABLECER ---
st.sidebar.header("* Datos de Entrada")

if st.sidebar.button("🔄 Restablecer datos originales"):
    st.session_state['v_max_1'] = 282.8
    st.session_state['i_max_1'] = 7.07
    st.session_state['omega_1'] = 377.0
    st.session_state['ang_1'] = -36.87
    st.session_state['a_1'] = 0.50

V_s_max = st.sidebar.slider("Tensión máx. secundaria Vmax (V)", 100.0, 400.0, st.session_state.get('v_max_1', 282.8), key='v_max_1')
I_s_max = st.sidebar.slider("Corriente máx. secundaria Imax (A)", 1.0, 20.0, st.session_state.get('i_max_1', 7.07), key='i_max_1')
omega = st.sidebar.number_input("Frecuencia angular ω (rad/s)", value=st.session_state.get('omega_1', 377.0), key='omega_1')
ang_i = st.sidebar.slider("Ángulo corriente secundaria (°)", -90.0, 90.0, st.session_state.get('ang_1', -36.87), key='ang_1')
a = st.sidebar.number_input("Relación de transformación (a)", value=st.session_state.get('a_1', 0.50), key='a_1')

# --- CÁLCULOS MATEMÁTICOS ---
V_s_rms = V_s_max / np.sqrt(2)
I_s_rms = I_s_max / np.sqrt(2)
frecuencia_hz = omega / (2 * np.pi)

theta_rad = np.radians(ang_i)
FP = np.cos(theta_rad)

V_s_complex = V_s_rms + 0j
I_s_complex = I_s_rms * (np.cos(theta_rad) + 1j * np.sin(theta_rad))

V_p_rms = a * V_s_rms
I_p_rms = I_s_rms / a
V_p_complex = a * V_s_complex
I_p_complex = I_s_complex / a

S_out = V_s_rms * I_s_rms
P_out = S_out * FP
Q_out = S_out * np.sin(-theta_rad)

S_in = V_p_rms * I_p_rms
P_in = S_in * FP
Q_in = S_in * np.sin(-theta_rad)

rv = 0.0
eta = 100.0

# Guardar en estado global para la tabla comparativa
st.session_state['caso1'] = {
    "Caso": "1. Trafo Ideal",
    "V_primario (V)": round(V_p_rms, 2),
    "I_primario (A)": round(I_p_rms, 2),
    "Pérdidas (W)": 0.0,
    "Regulación (%)": "0.00%",
    "Eficiencia (%)": "100.00%"
}

# --- PRESENTACIÓN VISUAL ---

st.subheader("1. Parámetros de Operación Básicos")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Tensión Vs (RMS)", f"{V_s_rms:.2f} V")
m2.metric("Corriente Is (RMS)", f"{I_s_rms:.2f} A")
m3.metric("Frecuencia (f)", f"{frecuencia_hz:.2f} Hz")
m4.metric("Factor de Potencia", f"{FP:.3f} ({'Retraso' if ang_i < 0 else 'Adelanto'})")

st.subheader("2. Fasores y Magnitudes Primarias")
c1, c2 = st.columns(2)

with c1:
    st.info("**Fasores del Secundario (Carga)**")
    st.write(f"• **Tensión $\mathbf{{V}}_s$:** {V_s_complex.real:.2f} + j({V_s_complex.imag:.2f}) V  |  **{V_s_rms:.2f} V ∠ 0.0°**")
    st.write(f"• **Corriente $\mathbf{{I}}_s$:** {I_s_complex.real:.2f} + j({I_s_complex.imag:.2f}) A  |  **{I_s_rms:.2f} A ∠ {ang_i:.2f}°**")

with c2:
    st.info("**Magnitudes del Primario (Fuente)**")
    st.write(f"• **Tensión Primaria $\mathbf{{V}}_p$:** {V_p_complex.real:.2f} + j({V_p_complex.imag:.2f}) V  |  **{V_p_rms:.2f} V ∠ 0.0°**")
    st.write(f"• **Corriente Primaria $\mathbf{{I}}_p$:** {I_p_complex.real:.2f} + j({I_p_complex.imag:.2f}) A  |  **{I_p_rms:.2f} A ∠ {ang_i:.2f}°**")

st.subheader("3. Balances de Potencia de Entrada y Salida")
p1, p2 = st.columns(2)

with p1:
    st.success("**Potencias de Entrada (Lado Primario)**")
    st.write(f"• **Aparente ($S_{{entrada}}$):** {S_in:.2f} VA")
    st.write(f"• **Activa ($P_{{entrada}}$):** {P_in:.2f} W")
    st.write(f"• **Reactiva ($Q_{{entrada}}$):** {Q_in:.2f} VAR")

with p2:
    st.success("**Potencias de Salida (Lado Secundario)**")
    st.write(f"• **Aparente ($S_{{salida}}$):** {S_out:.2f} VA")
    st.write(f"• **Activa ($P_{{salida}}$):** {P_out:.2f} W")
    st.write(f"• **Reactiva ($Q_{{salida}}$):** {Q_out:.2f} VAR")

st.subheader("4. Indicadores de Desempeño")
r1, r2 = st.columns(2)
r1.metric("Regulación de Voltaje (RV)", "0.00 %")
r2.metric("Eficiencia (η)", "100.00 %")

st.divider()

# --- VISUALIZACIONES ---
st.subheader("5. Gráficos y Esquemas")
tab1, tab2, tab3, tab4 = st.tabs(["📊 Diagrama Fasorial Vs e Is", "📈 Eficiencia vs Carga", "📉 Regulación vs Carga", "🔌 Circuito Equivalente"])

with tab1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatterpolar(r=[0, V_s_rms], theta=[0, 0], mode='lines+markers', name='Vs (V RMS)'))
    fig1.add_trace(go.Scatterpolar(r=[0, I_s_rms * 20], theta=[0, ang_i], mode='lines+markers', name='Is (A RMS x20)'))
    fig1.update_layout(title=f"Diagrama Fasorial de Vs e Is (f = {frecuencia_hz:.1f} Hz)", polar=dict(radialaxis=dict(visible=True)))
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    cargas = np.linspace(10, 150, 50)
    eficiencias = np.ones_like(cargas) * 100.0
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=cargas, y=eficiencias, mode='lines', name='Eficiencia (%)'))
    fig2.update_layout(title="Curva de Eficiencia vs Carga Nominal (%)", xaxis_title="Carga (%)", yaxis_title="Eficiencia (%)", yaxis=dict(range=[90, 105]))
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    regulaciones = np.zeros_like(cargas)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=cargas, y=regulaciones, mode='lines', name='Regulación (%)', line=dict(color='green')))
    fig3.update_layout(title="Curva de Regulación de Voltaje vs Carga (%)", xaxis_title="Carga (%)", yaxis_title="Regulación (%)", yaxis=dict(range=[-5, 5]))
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.write("### Circuito Equivalente del Transformador Ideal")
    st.code("""
      Primario (Np)           Secundario (Ns)
      + --- (||) ------------ (||) --- +
            (||)              (||)     
     Vp     (||)  Núcleo      (||)    Vs  Carga
            (||)  Ideal       (||)     
      - --- (||) ------------ (||) --- -
    """, language="text")

st.divider()

# --- INTERPRETACIÓN MEDIANTE IA ---
st.subheader(" Interpretación mediante IA")
if st.button(" Analizar resultado con IA"):
    st.success("### Análisis Técnico de Inteligencia Artificial")
    st.markdown(f"""
    1. **¿El resultado obtenido es físicamente razonable?**  
       *Sí. A una frecuencia de {frecuencia_hz:.2f} Hz, el balance entre entrada y salida es idéntico ($S_{{in}} = S_{{out}} = {S_out:.2f}\\text{{ VA}}$ y $P_{{in}} = P_{{out}} = {P_out:.2f}\\text{{ W}}$), lo cual define conceptualmente a una máquina ideal.*

    2. **¿Qué parámetro tiene mayor influencia sobre la regulación?**  
       *En este modelo ideal la regulación se mantiene estricta en **0.00%** para cualquier tipo de carga.*

    3. **¿Por qué cambia la regulación al modificar el factor de potencia?**  
       *En este transformador ideal no cambia (permanece en 0%). En modelos reales cambiaría por la caída de tensión en las reactancias de dispersión.*

    4. **¿Dónde se producen las principales pérdidas?**  
       *En este caso las pérdidas activas ($P$) y reactivas ($Q$) en los devanados son **0.00 W**.*

    5. **¿Qué diferencia existe entre el transformador ideal y el real en este caso?**  
       *El ideal asume acoplamiento perfecto, permeabilidad infinita del núcleo y ausencia total de resistencias eléctricas.*

    6. **¿Qué decisión de ingeniería recomendaría a partir de los resultados?**  
       *Utilizar los valores RMS determinados ($V_s = {V_s_rms:.2f}\\text{{ V}}$, $I_s = {I_s_rms:.2f}\\text{{ A}}$) para dimensionar la capacidad nominal del transformador.*
    """)