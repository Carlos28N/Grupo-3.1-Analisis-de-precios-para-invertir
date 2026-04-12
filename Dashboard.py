import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Dashboard de Inventario", layout="wide")

st.markdown("""
    <style>
    /* FONDO NOCTURNO */
    .stApp { 
        background-color: #0B0E14; 
    }
    
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    /* TÍTULOS */
    h1, h2, h3 {
        color: #FFC0CB !important; /* Rosa Pastel */
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }
    
    p, label, span {
        color: #F0F6FC !important; /* Blanco Perla */
    }

    /* FILTROS (DISEÑO CLEAN TECH)*/
    div[data-baseweb="select"] > div {
        background-color: #0B0E14 !important;
        border: 1px solid #FFC0CB !important; /* Borde rosa neón finito */
        border-radius: 12px !important;
    }

    /* Etiquetas de marcas (Rosa Pastel) */
    span[data-baseweb="tag"] {
        background-color: #FFC0CB !important;
        border-radius: 8px !important;
        border: 1px solid #B39DDB !important; /* Borde lavanda sutil */
    }
    
    /* Texto dentro de los cuadros (Negro puro para máximo contraste) */
    span[data-baseweb="tag"] span {
        color: #0B0E14 !important; 
        font-weight: 800 !important;
    }

    /* MÉTRICAS (KPIs)*/
    div[data-testid="metric-container"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-top: 3px solid #FFC0CB; /* rosa pastel */
        border-radius: 12px;
        padding: 20px;
    }

    /* LÍNEA DE AÑOS EN ROSA */
    div[data-baseweb="slider"] > div > div > div {
        background-color: #FFB6C1 !important;
    }
    
    div[role="slider"] {
        background-color: #FFC0CB !important;
        box-shadow: 0 0 10px #FFC0CB; /* Efecto de brillo rosa */
    }
            div[role="slider"] {
        background-color: #FFC0CB !important;
        box-shadow: 0 0 10px #FFC0CB;
    }
    div[data-baseweb="slider"] > div + div {
        display: none !important;
    }
    div[data-testid="stThumbValue"] {
        color: #FFC0CB !important;
        font-weight: bold !important;
    }
            /* TABS */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #F0F6FC !important; /* Texto blanco perla */
        font-size: 16px !important;
        font-weight: bold !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFC0CB !important; /* Rosa Pastel */
        color: #0B0E14 !important; /* Texto oscuro para que resalte */
        border-radius: 5px 5px 0px 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    df = pd.read_csv("dataset_limpio.csv")
    return df

df = cargar_datos()

st.sidebar.title("⚙️ Panel de Control")
st.sidebar.markdown("Filtra el inventario aquí:")

condiciones = st.sidebar.multiselect(
    "Condición del Vehículo:",
    options=df["Condicion"].unique(),
    default=df["Condicion"].unique()
)


marcas = st.sidebar.multiselect(
    "Selecciona Marcas:",
    options=sorted(df["Marca"].unique()),
    default=sorted(df["Marca"].unique())[:5] 
)


rango_años = st.sidebar.slider(
    "Rango de Año:",
    min_value=int(df['Año'].min()),
    max_value=int(df['Año'].max()),
    value=(int(df['Año'].min()), int(df['Año'].max()))
)


df_filtrado = df[
    (df["Condicion"].isin(condiciones)) &
    (df["Marca"].isin(marcas)) & 
    (df["Año"].between(rango_años[0], rango_años[1]))
]


st.title("Dashboard de Análisis de Mercado e Inversión Vehicular")
st.markdown("Grupo 3. Análisis de precios para invertir.")
st.write("") 

if df_filtrado.empty:
    st.warning("No hay datos con los filtros seleccionados.")
else:
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric("Total Vehículos", f"{len(df_filtrado)}")
    kpi2.metric("Precio Promedio", f"${df_filtrado['Precio'].mean():,.0f}")
    kpi3.metric("Kilometraje Promedio", f"{df_filtrado['Kilometraje'].mean():,.0f} km")
    
    total_nuevos = len(df_filtrado[df_filtrado['Condicion'] == 'Nuevo'])
    porcentaje_nuevos = (total_nuevos / len(df_filtrado)) * 100 if len(df_filtrado) > 0 else 0
    kpi4.metric("Inventario Nuevo", f"{porcentaje_nuevos:.1f}%")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Visión General", "📈 Análisis por Año", "🎯 Ofertas Atípicas", "🌀 Frecuencia de Stock",  "🔔 Distribución de Precios", "👑 Líderes de Ventas", "🎯 Análisis de Pareto" ])
   
with tab1:
        c_izq, c_der = st.columns(2)

        with c_izq:
            st.write("### Evolución del Precio Promedio por Año")
            fig_area = px.area(df_filtrado.groupby('Año')['Precio'].mean().reset_index(), 
                              x="Año", y="Precio",
                              color_discrete_sequence=['#FFB6C1'])
            fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_area, use_container_width=True)

        with c_der:
            st.write("### Distribución por Combustible")
            fig_donut = px.pie(df_filtrado, names='Combustible', hole=0.6,
                               color_discrete_sequence=px.colors.sequential.RdPu)
            fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=30, b=0))
            fig_donut.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)

        st.divider() 
        st.markdown("""
            <style>
            table {
                border: 1px solid rgba(255, 255, 255, 0.1) !important; /* Bordes muy finos y sutiles */
                border-collapse: collapse;
                width: 100%;
                background-color: transparent !important;
            }
            th, td {
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                padding: 12px !important;
                text-align: left !important;
                color: #FFFFFF;
            }
            /* ENCABEZADO CON TRANSPARENCIA */
            thead th {
                background-color: rgba(255, 183, 197, 0.2) !important; /* Rosa con 20% de opacidad */
                color: #FFC0CB !important;                            /* Letras rosa claro brillante */
                font-weight: bold !important;
                text-transform: uppercase;
                font-size: 13px;
                border-bottom: 2px solid rgba(255, 192, 203, 0.5) !important;
            }
            /* Efecto al pasar el mouse (opcional, se ve muy pro) */
            tbody tr:hover {
                background-color: rgba(255, 255, 255, 0.05) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        col_tabla1, col_tabla2 = st.columns(2)

        with col_tabla1:
            st.write("### ✨ Top 5: Vehículos Más Caros")
            top_caros = df_filtrado.nlargest(5, 'Precio')[['Marca', 'Modelo', 'Año', 'Precio']].reset_index(drop=True)
            top_caros['Precio'] = top_caros['Precio'].apply(lambda x: f"${x:,.2f}")
            st.table(top_caros) 

        with col_tabla2:
            st.write("### 🏷️ Top 5: Vehículos Más Baratos")
            top_baratos = df_filtrado.nsmallest(5, 'Precio')[['Marca', 'Modelo', 'Año', 'Precio']].reset_index(drop=True)
            top_baratos['Precio'] = top_baratos['Precio'].apply(lambda x: f"${x:,.2f}")
            st.table(top_baratos)

        

with tab2:
        st.write("### Relación Año vs Precio por condición")
        st.caption("¿Existen clásicos con precio de nuevo?")
        
        df_tendencia = df_filtrado.groupby(['Año', 'Condicion'])['Precio'].mean().reset_index()
        
        fig_line = px.line(
            df_tendencia, 
            x='Año', 
            y='Precio', 
            color='Condicion',
            color_discrete_map={'Nuevo': '#FFC0CB', 'Usado': '#B39DDB'},
            markers=True
        )
        
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_line, use_container_width=True)

with tab3:
        st.write("### Detección de Ofertas Atípicas por Modelo")
        
        st.caption("¿De qué manera el comportamiento de los precios permite detectar ofertas atípicas que se desvíen de la tendencia central del mercado?")
        
        fig_box = px.box(
            df_filtrado, 
            x='Modelo', 
            y='Precio', 
            color='Condicion', 
            color_discrete_map={'Nuevo': '#FFC0CB', 'Usado': '#B39DDB'}
        )
        
        fig_box.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Modelos de Vehículos",
            yaxis_title="Precio ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        fig_box.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#161B22')
        
        st.plotly_chart(fig_box, use_container_width=True)

with tab4:
        st.write("### Frecuencia de Stock por Marca y Año")
        
        st.caption("¿Cuál es la frecuencia de las combinaciones marca-año dentro del inventario actual?")
        
        df_df = df_filtrado.copy()
        df_df['Marca_Año'] = df_df['Marca'] + " (" + df_df['Año'].astype(str) + ")"
        
        top_combinaciones = df_df['Marca_Año'].value_counts().nlargest(10).reset_index()
        top_combinaciones.columns = ['Combinación', 'Cantidad']
        
        fig_radial = px.bar_polar(
            top_combinaciones, 
            r='Cantidad',        
            theta='Combinación',  
            color='Cantidad',      
            color_continuous_scale='RdPu', 
            template="plotly_dark", 
        )

        fig_radial.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor="rgba(0,0,0,0)", 
                angularaxis=dict(linewidth=1, showline=True, linecolor='#FFFFFF'), 
                radialaxis=dict(linewidth=1, showline=True, linecolor='#FFFFFF', showgrid=True, gridcolor='#FFFFFF')
                ),
            coloraxis_showscale=False 
        )
        
        st.plotly_chart(fig_radial, use_container_width=True)

with tab5:
        st.write("### Análisis de Densidad y Distribución")
        st.caption("¿Cómo se distribuyen los precios y qué tan sesgado está el mercado?")
        
        fig_violin = px.violin(
            df_filtrado, 
            y="Precio",       
            color="Condicion", 
            box=True,         
            points="outliers", 
            color_discrete_map={'Nuevo': '#FFC0CB', 'Usado': '#B39DDB'} 
        )
        
        fig_violin.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Precio del Vehículo ($)",
            xaxis_title="Condición",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        fig_violin.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#161B22')
        fig_violin.update_xaxes(showgrid=False) 
        
        fig_violin.update_traces(meanline_visible=True) 
        st.plotly_chart(fig_violin, use_container_width=True)

with tab6:
        st.write("### Marcas mas vendidas")
        st.caption("Ranking de marcas por volumen total en inventario (ordenadas de mayor a menor)")

        df_ranking = df_filtrado['Marca'].value_counts().reset_index()
        df_ranking.columns = ['Marca', 'Cantidad']
        df_ranking = df_ranking.sort_values(by='Cantidad', ascending=True) 

        fig_ranking = px.bar(
            df_ranking, 
            x='Cantidad', 
            y='Marca', 
            orientation='h',
            text='Cantidad', 
            color='Cantidad',
            color_continuous_scale='RdPu' 
        )

        fig_ranking.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Total de Vehículos",
            yaxis_title=None,
            coloraxis_showscale=False 
        )
        fig_ranking.update_traces(
            textfont_size=12, 
            textangle=0, 
            textposition="outside", 
            cliponaxis=False,
            marker_line_color='#FFFFFF',
            marker_line_width=0.5
        )
        
        fig_ranking.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#161B22')

        st.plotly_chart(fig_ranking, use_container_width=True)

with tab7:
        st.write("### Análisis de Pareto: Valor del Inventario")
        st.caption("Identificación de las marcas 'Clase A' que concentran el 80% del valor del capital.")

        df_pareto = df_filtrado.groupby('Marca')['Precio'].sum().sort_values(ascending=False).reset_index()
        df_pareto['Porcentaje'] = (df_pareto['Precio'] / df_pareto['Precio'].sum()) * 100
        df_pareto['Acumulado'] = df_pareto['Porcentaje'].cumsum()

        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])

        fig_pareto.add_trace(
            go.Bar(x=df_pareto['Marca'], y=df_pareto['Precio'], name="Valor Total ($)", marker_color='#B39DDB'),
            secondary_y=False,
        )
        fig_pareto.add_trace(
            go.Scatter(x=df_pareto['Marca'], y=df_pareto['Acumulado'], name="% Acumulado", line=dict(color='#FFC0CB', width=3)),
            secondary_y=True,
        )
        fig_pareto.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_pareto.add_shape(
            type="line", x0=0, x1=len(df_pareto)-1, y0=80, y1=80,
            line=dict(color="white", dash="dash"), secondary_y=True
        )

        st.plotly_chart(fig_pareto, use_container_width=True)
