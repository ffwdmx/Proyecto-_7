import pandas as pd
import numpy as np
from datetime import datetime

def format_currency(value):
    """Formatea valores como moneda"""
    return f"${value:,.0f}"

def format_number(value):
    """Formatea números con comas"""
    return f"{value:,}"

def calculate_depreciation_rate(df):
    """Calcula la tasa de depreciación promedio"""
    current_year = datetime.now().year
    df_with_age = df.copy()
    df_with_age['age'] = current_year - df_with_age['model_year']
    
    # Filtrar vehículos con al menos 1 año
    df_aged = df_with_age[df_with_age['age'] > 0]
    
    if len(df_aged) == 0:
        return 0
    
    # Calcular depreciación por año
    depreciation_by_age = df_aged.groupby('age')['price'].mean()
    
    # Calcular tasa de depreciación promedio
    if len(depreciation_by_age) > 1:
        total_depreciation = depreciation_by_age.iloc[0] - depreciation_by_age.iloc[-1]
        years = depreciation_by_age.index[-1] - depreciation_by_age.index[0]
        return (total_depreciation / depreciation_by_age.iloc[0] / years) * 100
    
    return 0

def get_insights(df):
    """Genera insights automáticos del dataset"""
    insights = []
    
    # Insight sobre el modelo más popular
    most_popular_model = df['model'].mode()[0]
    model_count = df['model'].value_counts().iloc[0]
    insights.append(f"El modelo más popular es {most_popular_model} con {model_count:,} vehículos")
    
    # Insight sobre combustible más caro
    fuel_prices = df.groupby('fuel')['price'].mean()
    most_expensive_fuel = fuel_prices.idxmax()
    insights.append(f"Los vehículos de {most_expensive_fuel} tienen el precio promedio más alto")
    
    # Insight sobre correlación precio-kilometraje
    corr_price_mileage = df['price'].corr(df['odometer'])
    if abs(corr_price_mileage) > 0.3:
        direction = "negativa" if corr_price_mileage < 0 else "positiva"
        insights.append(f"Existe una correlación {direction} moderada entre precio y kilometraje ({corr_price_mileage:.2f})")
    
    # Insight sobre 4WD
    if 'is_4wd' in df.columns:
        pct_4wd = (df['is_4wd'].sum() / len(df)) * 100
        insights.append(f"{pct_4wd:.1f}% de los vehículos tienen tracción 4WD")
    
    return insights

def export_filtered_data(df, filename=None):
    """Exporta datos filtrados a CSV"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'vehicles_filtered_{timestamp}.csv'
    
    df.to_csv(filename, index=False)
    return filename

def get_model_recommendations(df, budget_max, fuel_preference=None):
    """Sugiere modelos basados en presupuesto y preferencias"""
    filtered_df = df[df['price'] <= budget_max]
    
    if fuel_preference:
        filtered_df = filtered_df[filtered_df['fuel'] == fuel_preference]
    
    if len(filtered_df) == 0:
        return []
    
    # Calcular valor por dinero (precio / edad)
    current_year = datetime.now().year
    filtered_df = filtered_df.copy()
    filtered_df['age'] = current_year - filtered_df['model_year']
    filtered_df['value_score'] = filtered_df['model_year'] / (filtered_df['price'] / 1000)
    
    # Top modelos por valor
    top_models = filtered_df.groupby('model').agg({
        'price': 'mean',
        'model_year': 'mean',
        'value_score': 'mean',
        'condition': lambda x: x.mode()[0] if len(x) > 0 else 'unknown'
    }).sort_values('value_score', ascending=False).head(5)
    
    return top_models.round(2)