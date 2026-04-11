import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Precios de Autos", layout="wide")

st.markdown("""
    <style>
    /* Fondo negro absoluto para la página principal */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    /* Fondo de la barra superior */
    [data-testid="stHeader"] {
        background-color: #000000;
    }
    /* Fondo ligeramente distinto para la barra lateral para que contraste */
    [data-testid="stSidebar"] {
        background-color: #111111;
    }
    /* Color de texto base */
    p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #EDEDED !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    df = pd.read_csv("6. Precios de Carros (2).csv", on_bad_lines='skip')
    
    df.columns = df.columns.str.strip()
    
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    df = df.dropna(subset=['Brand', 'Price', 'Mileage', 'Year'])
    
    return df

df = cargar_datos()

st.sidebar.header("Filtros de Búsqueda 🔎")

marcas_disponibles = df["Brand"].unique()
marcas_seleccionadas = st.sidebar.multiselect(
    "Selecciona la Marca:",
    options=marcas_disponibles,
    default=list(marcas_disponibles)[:3] 
)

año_min = int(df['Year'].min())
año_max = int(df['Year'].max())
rango_años = st.sidebar.slider(
    "Rango de Año:",
    min_value=año_min,
    max_value=año_max,
    value=(año_min, año_max) 
)

precio_min = float(df["Price"].min())
precio_max = float(df["Price"].max())
rango_precios = st.sidebar.slider(
    "Rango de Precio ($)",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max) 
)

df_filtrado = df[
    (df["Brand"].isin(marcas_seleccionadas)) & 
    (df["Year"].between(rango_años[0], rango_años[1])) &
    (df["Price"].between(rango_precios[0], rango_precios[1]))
]

st.title("🚗 Dashboard de Análisis de Vehículos")
st.markdown("Visualización directa de precios, kilometraje y años del inventario.")
st.write("---")

if df_filtrado.empty:
    st.warning("⚠️ No hay vehículos que coincidan con estos filtros. Cambia la selección.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Autos Seleccionados", len(df_filtrado))
    col2.metric("Precio Promedio", f"${df_filtrado['Price'].mean():,.2f}")
    col3.metric("Kilometraje Promedio", f"{df_filtrado['Mileage'].mean():,.0f} km")
    
    st.write("---")
    grafico_izq, grafico_der = st.columns(2)
    
    with grafico_izq:
        st.subheader("Relación Precio vs Kilometraje 📉")
        fig_scatter = px.scatter(
            df_filtrado, 
            x="Mileage", 
            y="Price", 
            color="Brand",
            hover_data=["Model", "Year", "Fuel Type"],
            labels={"Mileage": "Kilometraje (km)", "Price": "Precio ($)"}, opacity=0.7,
            template="plotly_dark" # Activa el modo oscuro nativo de Plotly
        )
        fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with grafico_der:
        st.subheader("Distribución de Precios por Marca 💰")
        promedio_marca = df_filtrado.groupby('Brand')['Price'].mean().reset_index()
        fig_bar = px.bar(
            promedio_marca, 
            x="Brand", 
            y="Price", 
            color="Brand",
            labels={"Brand": "Marca", "Price": "Precio Promedio ($)"},
            text_auto='.2s',
            template="plotly_dark" # Activa el modo oscuro nativo de Plotly
        )
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)
   
    
