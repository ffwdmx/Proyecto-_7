import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_price_distribution_plot(df):
    """Crea un histograma de distribución de precios"""
    fig = px.histogram(
        df,
        x='price',
        nbins=50,
        title="Distribución de Precios de Vehículos",
        labels={'price': 'Precio ($)', 'count': 'Frecuencia'},
        color_discrete_sequence=['#636EFA']
    )
    fig.update_layout(
        xaxis_title="Precio ($)",
        yaxis_title="Frecuencia",
        showlegend=False
    )
    return fig

def create_top_models_plot(df, top_n=15):
    """Crea un gráfico de barras horizontales con los modelos más populares"""
    top_models = df['model'].value_counts().head(top_n)
    
    fig = px.bar(
        x=top_models.values,
        y=top_models.index,
        orientation='h',
        title=f"Top {top_n} Modelos Más Populares",
        labels={'x': 'Cantidad de Vehículos', 'y': 'Modelo'},
        color=top_models.values,
        color_continuous_scale='viridis'
    )
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    return fig

def create_price_by_fuel_plot(df):
    """Crea un gráfico de barras del precio promedio por tipo de combustible"""
    fuel_price = df.groupby('fuel')['price'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=fuel_price.index,
        y=fuel_price.values,
        title="Precio Promedio por Tipo de Combustible",
        labels={'x': 'Tipo de Combustible', 'y': 'Precio Promedio ($)'},
        color=fuel_price.values,
        color_continuous_scale='plasma'
    )
    fig.update_layout(showlegend=False)
    return fig

def create_condition_pie_chart(df):
    """Crea un gráfico de pastel para la distribución por condición"""
    condition_counts = df['condition'].value_counts()
    
    fig = px.pie(
        values=condition_counts.values,
        names=condition_counts.index,
        title="Distribución por Condición del Vehículo"
    )
    return fig

def create_price_vs_mileage_scatter(df, color_by='fuel', sample_size=5000):
    """Crea un gráfico de dispersión precio vs kilometraje"""
    if len(df) > sample_size:
        plot_df = df.sample(n=sample_size)
    else:
        plot_df = df
    
    fig = px.scatter(
        plot_df,
        x='odometer',
        y='price',
        color=color_by,
        title=f"Precio vs Kilometraje (coloreado por {color_by})",
        labels={'odometer': 'Kilometraje', 'price': 'Precio ($)'},
        opacity=0.6
    )
    return fig

def create_correlation_heatmap(df):
    """Crea una matriz de correlación para variables numéricas"""
    numeric_columns = ['price', 'model_year', 'odometer', 'cylinders', 'days_listed']
    corr_data = df[numeric_columns].corr()
    
    fig = px.imshow(
        corr_data,
        text_auto=True,
        aspect="auto",
        title="Matriz de Correlación entre Variables Numéricas",
        color_continuous_scale='RdBu',
        color_continuous_midpoint=0
    )
    return fig

def create_temporal_analysis_plot(df):
    """Crea un análisis temporal de precios"""
    if 'date_posted' in df.columns and df['date_posted'].notna().any():
        monthly_data = df.copy()
        monthly_data['year_month'] = monthly_data['date_posted'].dt.to_period('M')
        monthly_stats = monthly_data.groupby('year_month').agg({
            'price': ['mean', 'count']
        }).round(2)
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Precio Promedio por Mes", "Cantidad de Publicaciones por Mes"),
            vertical_spacing=0.1
        )
        
        # Precio promedio
        fig.add_trace(
            go.Scatter(
                x=[str(x) for x in monthly_stats.index],
                y=monthly_stats[('price', 'mean')],
                mode='lines+markers',
                name='Precio Promedio'
            ),
            row=1, col=1
        )
        
        # Cantidad de publicaciones
        fig.add_trace(
            go.Bar(
                x=[str(x) for x in monthly_stats.index],
                y=monthly_stats[('price', 'count')],
                name='Cantidad'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title="Análisis Temporal del Mercado",
            height=600,
            showlegend=False
        )
        
        return fig
    else:
        return None

def create_age_vs_price_analysis(df):
    """Análisis de depreciación por edad del vehículo"""
    age_price = df.groupby('age').agg({
        'price': ['mean', 'median', 'count']
    }).round(2)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Precio vs Edad del Vehículo", "Cantidad de Vehículos por Edad")
    )
    
    # Precio vs edad
    fig.add_trace(
        go.Scatter(
            x=age_price.index,
            y=age_price[('price', 'mean')],
            mode='lines+markers',
            name='Precio Promedio',
            line=dict(color='blue')
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=age_price.index,
            y=age_price[('price', 'median')],
            mode='lines+markers',
            name='Precio Mediano',
            line=dict(color='red', dash='dash')
        ),
        row=1, col=1
    )
    
    # Cantidad por edad
    fig.add_trace(
        go.Bar(
            x=age_price.index,
            y=age_price[('price', 'count')],
            name='Cantidad',
            marker_color='lightblue'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title="Análisis de Depreciación por Edad",
        height=400
    )
    
    return fig