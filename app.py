
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Histogramas por Carrera", page_icon="📈", layout="wide")

st.title("📈 Histogramas comparativos por Carrera")
st.write("Visualiza la distribución de una variable continua como histogramas por carrera.")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("dataset_limpio_para_app.csv")

df = load_data()

# Filtro único: Carrera
st.sidebar.header("🎓 Filtro por Carrera")
if "CARRERA" in df.columns:
    carreras = df["CARRERA"].dropna().unique().tolist()
    seleccionadas = st.sidebar.multiselect("Selecciona carrera(s):", carreras, default=carreras)
    df = df[df["CARRERA"].isin(seleccionadas)]

# Selección de variable continua para histograma
variables_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
var_grafico = st.sidebar.selectbox("Selecciona variable continua a graficar:", variables_numericas)

# Validación y gráfico
if df.empty:
    st.warning("No hay datos para las carreras seleccionadas.")
else:
    st.subheader(f"📊 Distribución de '{var_grafico}' por Carrera")
    chart = (
        alt.Chart(df)
        .transform_bin("binned", field=var_grafico, bin={"maxbins": 30})
        .mark_area(opacity=0.6, interpolate='monotone')
        .encode(
            x=alt.X("binned:Q", bin="binned", title=var_grafico),
            y=alt.Y("count()", stack=None, title="Frecuencia"),
            color=alt.Color("CARRERA:N", title="Carrera")
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(df[["CARRERA", var_grafico]], use_container_width=True)
