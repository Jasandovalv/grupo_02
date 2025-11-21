import streamlit as st

# --------------------------------------
# Configuración de la página
# --------------------------------------
st.set_page_config(page_title="Gráfico de emisiones CO₂", layout="wide)
st.title("📊 Gráfico de barras – Emisiones de CO₂ por país")
# Cargar datos
# --------------------------------------
csv_path = "/Users/jaimesandoval/Desktop/grupo21/co2/emissions_per_country/annual-co2-emissions-per-country.csv"
import pandas as pd
import altair as alt

# Cargar datos
df = pd.read_csv(csv_path)

# Interfaces de selección de país y año
paises = df['Country'].unique()
pais_seleccionado = st.selectbox('Selecciona un país', paises)

anios = df['Year'].unique()
anio_seleccionado = st.selectbox('Selecciona un año', sorted(anios))

# Filtrar datos por país y año seleccionado
df_filtrado = df[(df['Country'] == pais_seleccionado) & (df['Year'] == anio_seleccionado)]

# Gráfico de barras
if not df_filtrado.empty:
    st.subheader(f'Emisiones de CO₂ en {pais_seleccionado} - {anio_seleccionado}')
    chart = alt.Chart(df_filtrado).mark_bar().encode(
        x='Country:N',
        y='Annual CO₂ emissions:Q',
        color=alt.value("#0072B5")
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.write("No hay datos para la selección hecha.")