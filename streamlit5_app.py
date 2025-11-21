import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------
# Configuración
# --------------------------------------
st.set_page_config(page_title="Emisiones de CO₂", layout="wide")
st.title("📊 Gráfico de barras – Emisiones de CO₂ por país")

# --------------------------------------
# URL RAW de GitHub
# --------------------------------------
csv_url = "https://github.com/Jasandovalv/grupo_02/blob/main/co2/emissions_per_country/annual-co2-emissions-per-country.csv"

# --------------------------------------
# Cargar datos con caché
# --------------------------------------
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# --------------------------------------
# Procesar CSV
# --------------------------------------
df = df.rename(columns={"Entity": "country", "Code": "code", "Year": "year"})
df["code"] = df["code"].astype(str).str.upper()
df = df[df["code"].str.len() == 3]

value_cols = [c for c in df.columns if c not in ["country", "code", "year"]]
df = df.rename(columns={value_cols[0]: "co2"})
df["co2"] = pd.to_numeric(df["co2"], errors="coerce")

# --------------------------------------
# Selector de año
# --------------------------------------
years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Selecciona un año:", years)

df_year = df[df["year"] == selected_year].sort_values("co2", ascending=False)

# --------------------------------------
# Gráfico de barras
# --------------------------------------
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
st.dataframe(df_year, use_container_width=True)
