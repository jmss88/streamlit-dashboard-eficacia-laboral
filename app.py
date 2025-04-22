
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Visualizador de Eficacia Laboral", page_icon="📊", layout="wide")

st.title("📊 Visualizador de Eficacia Laboral por Carrera")
st.write("Explora tu base de datos con histogramas, boxplots y análisis de variables categóricas.")

@st.cache_data
def load_data():
    return pd.read_csv("dataset_limpio_para_app.csv")

df = load_data()

# Filtro principal: carreras
st.sidebar.header("🎓 Filtro de Carrera")
carreras = df["CARRERA"].dropna().unique().tolist()
carreras_sel = st.sidebar.multiselect("Selecciona una o más carreras:", carreras, default=carreras)
df = df[df["CARRERA"].isin(carreras_sel)]

# Variables continuas y categóricas
vars_continuas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
vars_categ = df.select_dtypes(include=["object", "category"]).columns.tolist()

# Pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Histogramas",
    "📦 Boxplots",
    "📋 Comparar variable categórica",
    "📊 Tabla resumen de variables categóricas"
])

with tab1:
    var_sel = st.sidebar.selectbox("📊 Variable continua para histograma/boxplot", vars_continuas)
    st.subheader(f"📈 Distribución de {var_sel} por Carrera")
    hist = (
        alt.Chart(df)
        .transform_bin("binned", field=var_sel, bin={"maxbins": 30})
        .mark_area(opacity=0.6, interpolate="monotone")
        .encode(
            x=alt.X("binned:Q", title=var_sel),
            y=alt.Y("count()", stack=None, title="Frecuencia"),
            color="CARRERA:N"
        )
        .properties(height=400)
    )
    st.altair_chart(hist, use_container_width=True)

with tab2:
    st.subheader(f"📦 Boxplot de {var_sel} por Carrera")
    box = (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            x=alt.X("CARRERA:N", title="Carrera"),
            y=alt.Y(f"{var_sel}:Q", title=var_sel),
            color="CARRERA:N"
        )
        .properties(height=400)
    )
    st.altair_chart(box, use_container_width=True)

with tab3:
    st.subheader("📋 Comparación de variables categóricas por Carrera")
    var_cat = st.selectbox("Selecciona variable categórica", vars_categ)
    df_bar = df.groupby(["CARRERA", var_cat]).size().reset_index(name="conteo")
    bar = (
        alt.Chart(df_bar)
        .mark_bar()
        .encode(
            x=alt.X("CARRERA:N", title="Carrera"),
            y=alt.Y("conteo:Q", title="Frecuencia"),
            color=alt.Color(var_cat, title=var_cat),
            tooltip=["CARRERA", var_cat, "conteo"]
        )
        .properties(height=400)
    )
    st.altair_chart(bar, use_container_width=True)

with tab4:
    st.subheader("📊 Tabla resumen de variables categóricas por Carrera")
    var_cat_resumen = st.selectbox("Selecciona variable categórica para tabla resumen", vars_categ, key="tabla")
    tabla = pd.crosstab(df["CARRERA"], df[var_cat_resumen])
    st.dataframe(tabla, use_container_width=True)
