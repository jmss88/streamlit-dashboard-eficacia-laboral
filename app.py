
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(page_title="Visualizador de Eficacia Laboral", page_icon="🧠", layout="wide")

st.title("🧠 Visualizador de Eficacia Laboral por Carrera")
st.write("Explora tu base de datos con múltiples vistas gráficas agrupadas por carrera.")

@st.cache_data
def load_data():
    return pd.read_csv("dataset_limpio_para_app.csv")

df = load_data()

# Filtro principal: carreras
st.sidebar.header("🎓 Filtro de Carrera")
carreras = df["CARRERA"].dropna().unique().tolist()
carreras_sel = st.sidebar.multiselect("Selecciona una o más carreras:", carreras, default=carreras)
df = df[df["CARRERA"].isin(carreras_sel)]

# Selección de variable continua
vars_continuas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
var_sel = st.sidebar.selectbox("📊 Variable continua a graficar", vars_continuas)

# Selección de variable categórica
vars_categ = df.select_dtypes(include=["object", "category"]).columns.tolist()
var_cat = st.sidebar.selectbox("📋 Variable categórica a comparar", vars_categ)

# Pestañas
tab1, tab2, tab3, tab4 = st.tabs(["📈 Histogramas", "📦 Boxplots", "🕸️ Radar (casos)", "📊 Niveles de AE"])

with tab1:
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
    st.subheader("🕸️ Radar chart por caso individual")
    radar_vars = ["Z_COE", "Z_INFO", "Z_TE", "AE_Total"]
    df_radar = df[["CARRERA"] + radar_vars].copy()
    df_radar["ID"] = df_radar.index.astype(str)

    if not df_radar.empty:
        fig = px.line_polar(
            df_radar.melt(id_vars=["CARRERA", "ID"], value_vars=radar_vars),
            r="value",
            theta="variable",
            color="CARRERA",
            line_group="ID",
            hover_name="ID",
            line_shape="linear"
        )
        fig.update_traces(opacity=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos suficientes para mostrar el radar chart.")

with tab4:
    st.subheader(f"📊 Frecuencia de {var_cat} por Carrera")
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
