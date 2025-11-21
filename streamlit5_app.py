import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------
# Configuración
# --------------------------------------
st.set_page_config(page_title="Emisiones de CO₂", layout="wide")
st.title("📊 Gráfico de barras – Emisiones de CO₂ por país")

# --------------------------------------
# URL CSV de Our World in Data
# --------------------------------------
csv_url = "https://ourworldindata.org/grapher/annual-co2-emissions-per-country.csv"

# --------------------------------------
# Cargar datos con caché
# --------------------------------------
@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)

    # Renombrar columnas estándar
    df = df.rename(columns={
        "Entity": "country",
        "Code": "code",
        "Year": "year"
    })

    df["code"] = df["code"].astype(str).str.upper()
    df = df[df["code"].str.len() == 3]

    # identificar columna de CO₂ automáticamente
    value_cols = [c for c in df.columns if c not in ["country", "code", "year"]]
    df = df.rename(columns={value_cols[0]: "co2"})
    df["co2"] = pd.to_numeric(df["co2"], errors="coerce")

    return df

# Cargar el dataframe
df = load_data(csv_url)

# --------------------------------------
# Selector de año
# --------------------------------------
years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Selecciona un año:", years)

df_year = df[df["year"] == selected_year].sort_values("co2", ascending=False)

# --------------------------------------
# Gráfico de barras
# --------------------------------------
st.subheader(f"Top 20 países emisores en {selected_year}")

fig = px.bar(
    df_year.head(20),
    x="country",
    y="co2",
    title=f"Top 20 países emisores en {selected_year}",
    labels={"country": "País", "co2": "Ton CO₂"}
)
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------
# Tabla
# --------------------------------------
st.subheader("📄 Tabla del año seleccionado")
st.dataframe(df_year[["country", "code", "year", "co2"]], use_container_width=True)

