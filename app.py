
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

    vars_continuas2 = df2.select_dtypes(include=["float64", "int64"]).columns.tolist()
    vars_categ2 = ["CF1", "CARRERA"]
    var_sel2 = st.selectbox("📊 Variable continua a graficar:", vars_continuas2, key="var_ansiedad")

    tab5, tab6, tab7, tab8 = st.tabs([
        "📈 Histogramas",
        "📦 Boxplots",
        "📋 Variables categóricas",
        "📊 Tabla resumen categórica"
    ])

    with tab5:
        st.subheader(f"📈 Histograma de {var_sel2}")
        hist2 = (
            alt.Chart(df2)
            .transform_bin("binned", field=var_sel2, bin={"maxbins": 30})
            .mark_area(opacity=0.6, interpolate="monotone")
            .encode(
                x=alt.X("binned:Q", title=var_sel2),
                y=alt.Y("count()", stack=None, title="Frecuencia"),
                color="CARRERA:N"
            )
            .properties(height=400)
        )
        st.altair_chart(hist2, use_container_width=True)

    with tab6:
        st.subheader(f"📦 Boxplot de {var_sel2} por Carrera")
        box2 = (
            alt.Chart(df2)
            .mark_boxplot()
            .encode(
                x=alt.X("CARRERA:N", title="Carrera"),
                y=alt.Y(f"{var_sel2}:Q", title=var_sel2),
                color="CARRERA:N"
            )
            .properties(height=400)
        )
        st.altair_chart(box2, use_container_width=True)

    with tab7:
        var_cat2 = st.selectbox("📋 Variable categórica:", vars_categ2, key="cat_ansiedad")
        df_bar2 = df2.groupby(["CARRERA", var_cat2]).size().reset_index(name="conteo")
        bar2 = (
            alt.Chart(df_bar2)
            .mark_bar()
            .encode(
                x=alt.X("CARRERA:N", title="Carrera"),
                y=alt.Y("conteo:Q", title="Frecuencia"),
                color=alt.Color(var_cat2, title=var_cat2),
                tooltip=["CARRERA", var_cat2, "conteo"]
            )
            .properties(height=400)
        )
        st.altair_chart(bar2, use_container_width=True)

    with tab8:
        var_cat_tabla2 = st.selectbox("📊 Variable categórica para tabla:", vars_categ2, key="tabla_ansiedad")
        tabla2 = pd.crosstab(df2["CARRERA"], df2[var_cat_tabla2])
        st.dataframe(tabla2, use_container_width=True)
