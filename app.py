import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN BÁSICA
# Configuramos la página para que use todo el ancho y tenga un título claro.
st.set_page_config(page_title="Dashboard de Precios de Autos", layout="wide")

# 2. CARGA DE DATOS (A prueba de errores y pantallas en blanco)
# Esta función lee el archivo y limpia los datos automáticamente.
@st.cache_data
def cargar_datos():
    # Asegúrate de que este nombre sea EXACTAMENTE el de tu archivo CSV
    df = pd.read_csv("6. Precios de Carros (2).csv", on_bad_lines='skip')
    
    # 🚨 SOLUCIÓN CLAVE: Quitamos espacios ocultos en los nombres de las columnas
    # que a veces traen los archivos CSV y causan que no se encuentren los datos.
    df.columns = df.columns.str.strip()
    
    # Forzamos que las columnas importantes sean números por si acaso.
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Borramos filas que no tengan datos esenciales en estas columnas clave.
    df = df.dropna(subset=['Brand', 'Price', 'Mileage', 'Year'])
    
    return df

df = cargar_datos()

# ==========================================
# 3. BARRA LATERAL (FILTROS)
# ==========================================
# Creamos la sección de filtros en el panel izquierdo.
st.sidebar.header("Filtros de Búsqueda 🔎")

# Filtro de Marcas
# Permite seleccionar una o varias marcas.
marcas_disponibles = df["Brand"].unique()
marcas_seleccionadas = st.sidebar.multiselect(
    "Selecciona la Marca:",
    options=marcas_disponibles,
    # Por defecto, seleccionamos las primeras 3 marcas para que empiece con datos.
    default=list(marcas_disponibles)[:3] 
)

# Filtro de Año
# Deslizador para elegir un rango de años de fabricación.
año_min = int(df['Year'].min())
año_max = int(df['Year'].max())
rango_años = st.sidebar.slider(
    "Rango de Año:",
    min_value=año_min,
    max_value=año_max,
    # Por defecto, selecciona todo el rango disponible.
    value=(año_min, año_max) 
)

# Filtro de Rango de Precio
# Deslizador para elegir un rango de precios.
precio_min = float(df["Price"].min())
precio_max = float(df["Price"].max())
rango_precios = st.sidebar.slider(
    "Rango de Precio ($)",
    min_value=precio_min,
    max_value=precio_max,
    # Por defecto, selecciona todo el rango disponible.
    value=(precio_min, precio_max) 
)

# === APLICAR LOS FILTROS ===
# Creamos un nuevo dataframe filtrado con las opciones elegidas.
df_filtrado = df[
    (df["Brand"].isin(marcas_seleccionadas)) & 
    (df["Year"].between(rango_años[0], rango_años[1])) &
    (df["Price"].between(rango_precios[0], rango_precios[1]))
]

# ==========================================
# 4. ÁREA PRINCIPAL DEL DASHBOARD
# ==========================================
st.title("🚗 Dashboard de Análisis de Vehículos")
st.markdown("Visualización directa de precios, kilometraje y años del inventario.")
st.divider()

# Comprobar si hay datos para mostrar después de aplicar los filtros.
if df_filtrado.empty:
    st.warning("⚠️ No hay vehículos que coincidan con estos filtros. Por favor, selecciona otras opciones en la barra lateral.")
else:
    # --- MÉTRICAS PRINCIPALES ---
    # Mostramos tres indicadores clave en columnas.
    col1, col2, col3 = st.columns(3)
    
    # Total de autos que cumplen los filtros
    col1.metric("Total Autos Seleccionados", len(df_filtrado))
    
    # Precio promedio formateado con dos decimales y símbolo de dólar
    col2.metric("Precio Promedio", f"${df_filtrado['Price'].mean():,.2f}")
    
    # Kilometraje promedio formateado con separadores de miles y 'km'
    col3.metric("Kilometraje Promedio", f"{df_filtrado['Mileage'].mean():,.0f} km")
    
    st.divider()

# --- GRÁFICOS INTERACTIVOS ---
    # Organizamos dos gráficos en columnas.
    grafico_izq, grafico_der = st.columns(2)
    
    with grafico_izq:
        st.subheader("Relación Precio vs Kilometraje 📉")
        # Gráfico de dispersión para ver cómo el kilometraje afecta el precio.
        # Cada punto es un auto, coloreado por marca.
        fig_scatter = px.scatter(
            df_filtrado, 
            x="Mileage", 
            y="Price", 
            color="Brand",
            # Información que aparece al pasar el ratón sobre un punto
            hover_data=["Model", "Year", "Fuel Type"],
            # Etiquetas amigables para los ejes
            labels={"Mileage": "Kilometraje (km)", "Price": "Precio ($)"},
            opacity=0.6, # Transparencia para ver puntos superpuestos
            title="Comparativa de precio y uso por marca"
        )
        # Mostramos el gráfico en la columna izquierda ocupando todo el ancho.
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with grafico_der:
        st.subheader("Distribución de Precios por Marca 💰")
        # Calculamos el promedio por marca para hacer un gráfico de barras limpio.
        promedio_marca = df_filtrado.groupby('Brand')['Price'].mean().reset_index()
        # Gráfico de barras para comparar el precio promedio entre marcas.
        fig_bar = px.bar(
            promedio_marca, 
            x="Brand", 
            y="Price", 
            color="Brand",
            # Etiquetas amigables para los ejes
            labels={"Brand": "Marca", "Price": "Precio Promedio ($)"},
            # Formato numérico para el texto sobre las barras
            text_auto='.2s', 
            title="Precio medio de venta por marca"
        )
        # Mostramos el gráfico en la columna derecha ocupando todo el ancho.
        st.plotly_chart(fig_bar, use_container_width=True)