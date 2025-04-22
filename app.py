
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Dashboard Psicoeducativo", page_icon="🧠", layout="wide")
st.title("🧠 Dashboard Psicoeducativo")
st.write("Visualiza y compara información de distintos estudios en un solo lugar.")

@st.cache_data
def load_eficacia():
    return pd.read_csv("dataset_limpio_para_app.csv")

@st.cache_data
def load_ansiedad():
    return pd.read_csv("DATOS_ANSIEDAD_C1_APP.arff.csv")

# Tabs principales
main_tab1, main_tab2 = st.tabs(["📊 Eficacia Laboral", "📚 Ansiedad Académica"])

# --------------------------
# 📊 Eficacia Laboral
# --------------------------
with main_tab1:
    st.header("📊 Visualización de Eficacia Laboral")
    df = load_eficacia()
    
    carreras = df["CARRERA"].dropna().unique().tolist()
    carreras_sel = st.multiselect("Selecciona carrera(s):", carreras, default=carreras)
    df = df[df["CARRERA"].isin(carreras_sel)]

    vars_continuas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    vars_categ = df.select_dtypes(include=["object", "category"]).columns.tolist()
    var_sel = st.selectbox("📊 Variable continua a graficar:", vars_continuas)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Histogramas",
        "📦 Boxplots",
        "📋 Variables categóricas",
        "📊 Tabla resumen categórica"
    ])

    with tab1:
        st.subheader(f"📈 Histograma de {var_sel}")
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
        var_cat = st.selectbox("📋 Variable categórica:", vars_categ)
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
        var_cat_tabla = st.selectbox("📊 Variable categórica para tabla:", vars_categ, key="tabla_eficacia")
        tabla = pd.crosstab(df["CARRERA"], df[var_cat_tabla])
        st.dataframe(tabla, use_container_width=True)

# --------------------------
# 📚 Ansiedad Académica
# --------------------------
with main_tab2:
    st.header("📚 Visualización de Ansiedad Académica")
    df2 = load_ansiedad()

    carreras2 = df2["CARRERA"].dropna().unique().tolist()
    carreras_sel2 = st.multiselect("Selecciona carrera(s):", carreras2, default=carreras2, key="carreras_ansiedad")
    df2 = df2[df2["CARRERA"].isin(carreras_sel2)]

    var_cf1 = "CF1"
    st.subheader("📊 Frecuencia de niveles de ansiedad (CF1)")
    conteo_cf1 = df2[var_cf1].value_counts().reset_index()
    conteo_cf1.columns = ["Nivel de Ansiedad", "Frecuencia"]

    bar_cf1 = (
        alt.Chart(conteo_cf1)
        .mark_bar()
        .encode(
            x=alt.X("Nivel de Ansiedad:N", sort="-y"),
            y=alt.Y("Frecuencia:Q"),
            color="Nivel de Ansiedad:N"
        )
        .properties(height=400)
    )
    st.altair_chart(bar_cf1, use_container_width=True)

    st.subheader("📈 Histograma por ítem")
    items_ansiedad = [col for col in df2.columns if col.startswith("F1")]
    if items_ansiedad:
        var_item = st.selectbox("Selecciona un ítem:", items_ansiedad)
        hist_item = (
            alt.Chart(df2)
            .mark_bar()
            .encode(
                x=alt.X(f"{var_item}:Q", bin=alt.Bin(maxbins=3)),
                y=alt.Y("count()", title="Frecuencia"),
                color="CARRERA:N"
            )
            .properties(height=400)
        )
        st.altair_chart(hist_item, use_container_width=True)

    st.subheader("📄 Tabla de respuestas por ítem")
    st.dataframe(df2, use_container_width=True)
