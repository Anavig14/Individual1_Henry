import pandas as pd
from fastapi import FastAPI
from typing import Dict

app = FastAPI()

# DESARROLLO DE FUNCIONES

## FUNCION 1. CANTIDAD DE PELICULAS ESTRENADAS EN UN MES ESPECIFICO

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

## FUNCIÓN 2. CANTIDAD DE PELICULAS ESTRENADAS EN UN DÍA

@app.get('/cantidad_filmaciones_dia/{dia}', response_model=Dict[str, str])
def cantidad_filmaciones_dia(dia: int):
    if dia < 1 or dia > 31:
        return {"error": "Día inválido. Debe estar entre 1 y 31."}
    
    cantidad = df_movies[df_movies['release_date'].dt.day == dia].shape[0]
    
    return {"mensaje": f"{cantidad} películas fueron estrenadas en el día {dia}"}


## FUNCIÓN 3. SCORE DE UNA FILMACIÓN POR TITULO
 
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    # Limpiar el título de espacios adicionales y convertirlo a minúsculas
    titulo_limpio = titulo.strip().lower()
    
    # Buscar la película por título en el DataFrame, ignorando mayúsculas/minúsculas y espacios adicionales
    filmacion = df_movies[df_movies['title'].str.lower().str.strip() == titulo_limpio]
    
    # Verificar si se encontró la película
    if filmacion.empty:
        return {"error": "Película no encontrada"}
    
    # Extraer la popularidad y el año de estreno
    score = filmacion['popularity'].values[0]
    año_estreno = filmacion['release_year'].values[0]
    
    return {
        "mensaje": f"La película '{titulo}' fue estrenada en el año {año_estreno} con un score de {score}"
    }

## FUNCIÓN 4. VOTOS POR TITULO

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    # Buscar la película por título
    filmacion = df_movies[df_movies['title'].str.lower() == titulo.lower()]

    # Verificar si la película existe
    if filmacion.empty:
        return {"error": "Película no encontrada"}
    
    # Extraer la cantidad de votos y el promedio de votos
    votos = filmacion['vote_count'].values[0]
    promedio_votos = filmacion['vote_average'].values[0]
    
    # Verificar si la película tiene suficientes valoraciones
    if votos < 2000:
        return {"mensaje": "La película no cuenta con suficientes valoraciones (mínimo 2000)"}
    
    return {
        "titulo": titulo,
        "total_votos": votos,
        "promedio_votos": promedio_votos
    }


## FUNCIÓN 5.  DATOS DEL ACTOR

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    # Filtrar películas en las que el actor está en la columna 'Lead actor'
    actor_data = df_movies[df_movies['Lead actor'].str.lower() == nombre_actor.lower()]
    
    if actor_data.empty:
        return {"error": "Actor no encontrado"}
    
    # Calcular la cantidad de películas, retorno total y retorno promedio
    cantidad_peliculas = actor_data.shape[0]
    retorno_total = actor_data['return'].sum()
    retorno_promedio = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    
    return {
        "actor": nombre_actor,
        "cantidad de películas": cantidad_peliculas,
        "retorno total": retorno_total,
        "retorno promedio por filmación": retorno_promedio
    }


## FUNCIÓN 6.  DATOS DEL DIRECTOR

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    # Filtrar películas basadas en el nombre del director en df_movies
    peliculas_info = df_movies[df_movies['Director'].str.lower() == nombre_director.lower()]

    # Verificar si se encontraron películas
    if peliculas_info.empty:
        return {"error": "Director no encontrado"}
    
    # Lista para almacenar la información de las películas
    info_peliculas = []

    # Iterar sobre las películas encontradas
    for _, row in peliculas_info.iterrows():
        info_peliculas.append({
            "título": row['title'],
            "fecha de lanzamiento": row['release_date'].strftime('%Y-%m-%d'),  # Formatear la fecha
            "retorno": row['return'],
            "costo": row['budget'],
            "ganancia": row['revenue']
        })
    
    # Retornar la información del director y sus películas
    return {
        "director": nombre_director,
        "películas dirigidas": info_peliculas
    }
