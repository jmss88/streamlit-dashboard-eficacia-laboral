
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

# Lista de columnas categóricas a incluir como filtros
filtros_categoricos = [
    "NIVEL_AE_COE",
    "NIVEL_AE_INFO",
    "NIVEL_AE_TE",
    "Nivel_AE_TOTAL"
]

# Aplicar filtros dinámicos por cada columna categórica
for columna in filtros_categoricos:
    if columna in df.columns:
        opciones = df[columna].dropna().unique().tolist()
        seleccionadas = st.sidebar.multiselect(f"Filtrar por {columna}:", opciones, default=opciones)
        df = df[df[columna].isin(seleccionadas)]

# Filtro por variable numérica para graficar
variables_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
var_grafico = st.sidebar.selectbox("Selecciona variable a graficar:", variables_numericas)

# Mostrar tabla
st.subheader("📋 Datos filtrados")
st.dataframe(df, use_container_width=True)

# Mostrar gráfica de barras promedio por grupo
grupo_base = "Nivel_AE_TOTAL" if "Nivel_AE_TOTAL" in df.columns else "NIVEL_AE_COE"

st.subheader(f"📈 Promedio de '{var_grafico}' por {grupo_base}")
df_bar = df.groupby(grupo_base)[var_grafico].mean().reset_index()
chart = (
    alt.Chart(df_bar)
    .mark_bar()
    .encode(
        x=alt.X(grupo_base, title=grupo_base),
        y=alt.Y(var_grafico, title=f"Promedio de {var_grafico}"),
        color=grupo_base
    )
    .properties(height=400)
)
st.altair_chart(chart, use_container_width=True)
