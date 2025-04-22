
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Comparativa por Carrera", page_icon="🎓", layout="wide")

st.title("🎓 Comparativa por Carrera en Eficacia Laboral")
st.write("Selecciona una o más carreras para comparar variables de eficacia laboral de manera visual.")

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

# Selección de variable numérica
variables_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
var_grafico = st.sidebar.selectbox("Selecciona variable a graficar:", variables_numericas)

# Validación y gráfica
if df.empty:
    st.warning("No hay datos para las carreras seleccionadas.")
else:
    st.subheader(f"📊 Comparativa de '{var_grafico}' entre carreras")
    df_bar = df.groupby("CARRERA")[var_grafico].mean().reset_index()
    chart = (
        alt.Chart(df_bar)
        .mark_bar()
        .encode(
            x=alt.X("CARRERA:N", title="Carrera"),
            y=alt.Y(var_grafico, title=f"Promedio de {var_grafico}"),
            color="CARRERA:N"
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(df_bar, use_container_width=True)
