import pandas as pd
import numpy as np
from datetime import datetime

def load_and_clean_vehicles_data(file_path='data/vehicles_us.csv'):
    """
    Carga y limpia el dataset de vehículos
    
    Returns:
        pd.DataFrame: Dataset limpio
    """
    try:
        df = pd.read_csv(file_path)
        
        # Limpieza básica
        df = df.dropna(subset=['price', 'model_year'])
        df = df[df['price'] > 0]
        df = df[df['price'] < 100000]
        df = df[df['model_year'] >= 1990]
        
        # Conversiones de tipos
        df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
        df['model_year'] = df['model_year'].astype(int)
        
        # Llenar valores faltantes
        categorical_columns = ['condition', 'fuel', 'transmission', 'type', 'paint_color']
        for col in categorical_columns:
            df[col] = df[col].fillna('unknown')
        
        # Crear variables derivadas
        df = create_derived_variables(df)
        
        return df
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
        return None

def create_derived_variables(df):
    """
    Crea variables derivadas útiles para el análisis
    """
    current_year = datetime.now().year
    
    # Categorías de precio
    df['price_category'] = pd.cut(df['price'], 
                                bins=[0, 5000, 15000, 30000, 50000, float('inf')],
                                labels=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'])
    
    # Edad del vehículo
    df['age'] = current_year - df['model_year']
    df['age_category'] = pd.cut(df['age'],
                              bins=[0, 3, 7, 15, float('inf')],
                              labels=['Nuevo', 'Semi-nuevo', 'Usado', 'Clásico'])
    
    # Categoría de kilometraje
    df['mileage_category'] = pd.cut(df['odometer'],
                                  bins=[0, 30000, 75000, 150000, float('inf')],
                                  labels=['Bajo', 'Medio', 'Alto', 'Muy Alto'])
    
    # Precio por año (depreciación)
    df['price_per_year'] = df['price'] / (current_year - df['model_year'] + 1)
    
    return df

def get_summary_statistics(df):
    """
    Genera estadísticas resumidas del dataset
    """
    stats = {
        'total_records': len(df),
        'avg_price': df['price'].mean(),
        'median_price': df['price'].median(),
        'avg_year': df['model_year'].mean(),
        'unique_models': df['model'].nunique(),
        'price_range': (df['price'].min(), df['price'].max()),
        'year_range': (df['model_year'].min(), df['model_year'].max())
    }
    
    return stats

def filter_data(df, price_range=None, fuel_types=None, transmissions=None, year_range=None):
    """
    Aplica filtros al dataset
    """
    filtered_df = df.copy()
    
    if price_range:
        filtered_df = filtered_df[
            (filtered_df['price'] >= price_range[0]) & 
            (filtered_df['price'] <= price_range[1])
        ]
    
    if fuel_types:
        filtered_df = filtered_df[filtered_df['fuel'].isin(fuel_types)]
    
    if transmissions:
        filtered_df = filtered_df[filtered_df['transmission'].isin(transmissions)]
    
    if year_range:
        filtered_df = filtered_df[
            (filtered_df['model_year'] >= year_range[0]) & 
            (filtered_df['model_year'] <= year_range[1])
        ]
    
    return filtered_df