# Proyecto-_7
## Prueba Proyecto_7
Codigo para sprint de proyecto en Tripleten
liga de render.com https://proyecto-7-njp7.onrender.com

Estructura de archivos:
    data En esta carpeta se guarda el dataset vehicles_us.csv

    notebooks
        Notebook de análisis completo: 
            Analisis exploratorio paso a paso con el dataset real
            Estadisticas descriptivas especificas
            Insights automaticos para compradores / vendedores
    src
        data processing. py -> Funciones para cargar, kimpiar y filtrar datos
        visualizations.py -> Funciones para crear graficos especificos
        utils.py -> Funciones auxiliares  ( formateo, insights, recomendaciones)
    app.py
        Aplicacion con Streamlit
        Carga y procesa las 51,525 filas del dataset
        Filtros interactivos basados en 13 columnas especificas
        Visualizaciones diseñadas para el mercado automotriz de US
        Analisis de depreciacion, correlaciones y tendencias

    README
    requirements.txt