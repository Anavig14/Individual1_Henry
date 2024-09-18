import pandas as pd
from fastapi import FastAPI
from typing import Dict


app = FastAPI()

# Cargar el DataFrame (asegúrate de ajustar la ruta a tu archivo)
df_movies = pd.read_csv(r'C:\Users\anavi\OneDrive\Escritorio\Individual1 _ Henry\movies.csv')

# Asegúrate de que 'release_date' esté en formato de fecha
df_movies['release_date'] = pd.to_datetime(df_movies['release_date'], format='%Y-%m-%d', errors='coerce')

@app.get('/cantidad_filmaciones_mes/{mes}', response_model=Dict[str, str])
def cantidad_filmaciones_mes(mes: str):
    # Mapeo de meses en español
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    mes_lower = mes.lower()
    
    if mes_lower not in meses:
        return {"error": "Mes inválido"}
    
    mes_num = meses[mes_lower]
    
    # Filtrar películas que fueron estrenadas en el mes dado
    cantidad = df_movies[df_movies['release_date'].dt.month == mes_num].shape[0]
    
    return {"cantidad": f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"}