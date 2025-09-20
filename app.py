import streamlit as st
import pandas as pd

# ✅ IMPORTAR FUNCIONES DE LOS ARCHIVOS DE SOPORTE
from src.data_processing import load_and_clean_vehicles_data, get_summary_statistics, filter_data
from src.visualizations import (
    create_price_distribution_plot,
    create_top_models_plot, 
    create_price_by_fuel_plot,
    create_condition_pie_chart,
    create_price_vs_mileage_scatter,
    create_correlation_heatmap
)
from src.utils import format_currency, get_insights, get_model_recommendations

# Configuración de página
st.set_page_config(
    page_title="Análisis de Vehículos US",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Análisis de Vehículos US")

# ✅ USAR FUNCIÓN DE data_processing.py
@st.cache_data
def load_data():
    return load_and_clean_vehicles_data('data/vehicles_us.csv')

# Cargar datos usando nuestra función personalizada
df = load_data()

if df is not None:
    # ✅ USAR FUNCIÓN DE data_processing.py
    stats = get_summary_statistics(df)
    
    # Mostrar métricas usando los stats calculados
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Vehículos", f"{stats['total_records']:,}")
    with col2:
        st.metric("Precio Promedio", format_currency(stats['avg_price']))  # ✅ USAR utils.py
    with col3:
        st.metric("Precio Mediano", format_currency(stats['median_price']))  # ✅ USAR utils.py
    with col4:
        st.metric("Modelos Únicos", f"{stats['unique_models']:,}")
    
    # Sidebar para filtros
    st.sidebar.header("🔧 Filtros")
    
    # Filtro de precio
    min_price, max_price = st.sidebar.select_slider(
        "Rango de Precio",
        options=[0, 5000, 10000, 15000, 25000, 50000, 75000, 100000],
        value=(5000, 50000)
    )
    
    # Filtro de combustible
    fuel_options = df['fuel'].unique()
    selected_fuels = st.sidebar.multiselect(
        "Tipo de Combustible",
        options=fuel_options,
        default=fuel_options[:4]  # Primeros 4 por defecto
    )
    
    # ✅ USAR FUNCIÓN DE data_processing.py para filtrar
    filtered_df = filter_data(
        df, 
        price_range=(min_price, max_price),
        fuel_types=selected_fuels
    )
    
    st.write(f"📊 Mostrando {len(filtered_df):,} vehículos de {len(df):,} totales")
    
    # ✅ USAR FUNCIONES DE visualizations.py
    st.header("📈 Visualizaciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribución de precios
        fig_dist = create_price_distribution_plot(filtered_df)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Gráfico de top modelos
        fig_models = create_top_models_plot(filtered_df, top_n=10)
        st.plotly_chart(fig_models, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Precio por combustible
        fig_fuel = create_price_by_fuel_plot(filtered_df)
        st.plotly_chart(fig_fuel, use_container_width=True)
    
    with col4:
        # Gráfico de pastel de condiciones
        fig_condition = create_condition_pie_chart(filtered_df)
        st.plotly_chart(fig_condition, use_container_width=True)
    
    # Gráfico de dispersión precio vs kilometraje
    st.subheader("🔍 Análisis de Correlación")
    color_option = st.selectbox("Colorear por:", ['fuel', 'condition', 'transmission'])
    fig_scatter = create_price_vs_mileage_scatter(filtered_df, color_by=color_option)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Matriz de correlación
    st.subheader("🌡️ Matriz de Correlación")
    fig_corr = create_correlation_heatmap(filtered_df)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # ✅ USAR FUNCIÓN DE utils.py para insights
    st.header("💡 Insights Automáticos")
    insights = get_insights(filtered_df)
    for i, insight in enumerate(insights, 1):
        st.info(f"{i}. {insight}")
    
    # ✅ USAR FUNCIÓN DE utils.py para recomendaciones
    st.header("🎯 Recomendador de Vehículos")
    budget = st.number_input("Presupuesto máximo ($)", min_value=1000, max_value=100000, value=25000, step=1000)
    fuel_pref = st.selectbox("Preferencia de combustible (opcional)", ['Todos'] + list(df['fuel'].unique()))
    
    if fuel_pref == 'Todos':
        fuel_pref = None
    
    recommendations = get_model_recommendations(filtered_df, budget, fuel_pref)
    
    if len(recommendations) > 0:
        st.subheader("🚗 Modelos Recomendados")
        st.dataframe(recommendations)
    else:
        st.warning("No se encontraron vehículos que cumplan con los criterios especificados.")

else:
    st.error("❌ No se pudo cargar el dataset. Verifica que vehicles_us.csv esté en la carpeta data/")