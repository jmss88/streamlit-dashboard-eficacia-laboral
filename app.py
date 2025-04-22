
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Dashboard de Eficacia Laboral", page_icon="📊", layout="wide")

st.title("📊 Dashboard de Eficacia Laboral")
st.write("Explora los datos del estudio de eficacia laboral por niveles de autoeficacia, variables y puntajes.")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("dataset_limpio_para_app.csv")

df = load_data()

# Filtros
st.sidebar.header("🔍 Filtros")

# Filtro por nivel de AE (si existe)
if "NIVEL_AE_COE" in df.columns:
    nivel_ae = st.sidebar.multiselect(
        "Nivel de AE (COE):",
        options=df["NIVEL_AE_COE"].unique().tolist(),
        default=df["NIVEL_AE_COE"].unique().tolist()
    )
    df = df[df["NIVEL_AE_COE"].isin(nivel_ae)]

# Filtro por variable para graficar
variables_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
var_grafico = st.sidebar.selectbox("Selecciona variable a graficar:", variables_numericas)

# Mostrar tabla
st.subheader("📋 Datos filtrados")
st.dataframe(df, use_container_width=True)

# Mostrar gráfica de barras promedio por grupo
if "NIVEL_AE_COE" in df.columns:
    st.subheader(f"📈 Promedio de '{var_grafico}' por Nivel de AE (COE)")
    df_bar = df.groupby("NIVEL_AE_COE")[var_grafico].mean().reset_index()
    chart = (
        alt.Chart(df_bar)
        .mark_bar()
        .encode(
            x=alt.X("NIVEL_AE_COE", title="Nivel AE"),
            y=alt.Y(var_grafico, title=f"Promedio de {var_grafico}"),
            color="NIVEL_AE_COE"
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)
