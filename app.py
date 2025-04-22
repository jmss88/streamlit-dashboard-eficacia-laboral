
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Visualizador de Eficacia Laboral", page_icon="📊", layout="wide")

st.title("📊 Visualizador de Eficacia Laboral por Carrera")
st.write("Explora tu base de datos con histogramas y boxplots comparativos por carrera.")

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

# Pestañas
tab1, tab2 = st.tabs(["📈 Histogramas", "📦 Boxplots"])

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
