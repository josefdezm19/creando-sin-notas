import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="FutbolTracker AI", layout="wide")
st.title("⚽ FutbolTracker: Análisis Táctico en Tiempo Real")

# 2. Conexión API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ Falta la API Key en los 'Secrets'.")
    st.stop()

# 3. Inicializar memoria de partido (Si no existe, creamos una lista vacía)
if "eventos" not in st.session_state:
    st.session_state.eventos = []

# --- INTERFAZ DE REGISTRO DE DATOS ---
st.subheader("📍 Registrar Acción")

col1, col2, col3 = st.columns(3)

with col1:
    # Simulación de las 12 zonas
    zona = st.selectbox("Zona del Campo (1-12)", 
                        options=[f"Zona {i}" for i in range(1, 13)],
                        help="Zona 1-4: Defensa | 5-8: Medio | 9-12: Ataque")

with col2:
    accion = st.selectbox("Acción Técnica", 
                          ["Pase Correcto", "Pase Fallado", "Recuperación", "Pérdida", "Tiro a Puerta", "Gol"])

with col3:
    jugador = st.text_input("Dorsal / Nombre", "General")

# Botón grande para guardar
if st.button("➕ Registrar Jugada", use_container_width=True):
    # Guardamos el evento en la memoria
    nuevo_evento = {"Minuto": "En curso", "Zona": zona, "Acción": accion, "Jugador": jugador}
    st.session_state.eventos.append(nuevo_evento)
    st.success(f"Registrado: {accion} en {zona}")

# --- VISUALIZACIÓN DE DATOS ---
st.divider()
col_datos, col_ia = st.columns([1, 1])

with col_datos:
    st.subheader("📋 Registro del Partido")
    if st.session_state.eventos:
        df = pd.DataFrame(st.session_state.eventos)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay datos registrados.")

# --- CEREBRO IA (GEMINI) ---
with col_ia:
    st.subheader("🤖 Analista Táctico AI")
    st.write("Cuando tengas suficientes datos, pide el análisis.")
    
    if st.button("Generar Análisis Táctico", type="primary"):
        if not st.session_state.eventos:
            st.warning("Registra al menos 3 jugadas antes de analizar.")
        else:
            with st.spinner("Gemini está analizando el partido..."):
                # Convertimos los datos a texto para que la IA los lea
                datos_texto = str(st.session_state.eventos)
                
                # Prompt específico mezclando tus instrucciones + los datos reales
                PROMPT_FINAL = f"""
                Actúa como un analista táctico de fútbol profesional.
                
                Aquí tienes el registro de eventos del partido en tiempo real:
                {datos_texto}
                
                Basándote EXCLUSIVAMENTE en estos datos:
                1. Identifica patrones (¿Por qué zona atacan más? ¿Dónde pierden el balón?).
                2. Da 3 consejos tácticos urgentes para el entrenador.
                3. Sé breve y directo.
                """
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(PROMPT_FINAL)
                
                st.markdown("### 📝 Informe del Entrenador")
                st.markdown(response.text)
