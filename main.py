import pandas as pd
from fastapi import FastAPI
from typing import Dict

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# DESARROLLO DE FUNCIONES

## FUNCION 1. CANTIDAD DE PELICULAS ESTRENADAS EN UN MES ESPECIFICO

# Voy a usar el data frame que limpié y creé.
df_movies = pd.read_csv(r'movies.csv', low_memory=False)

df_movies['release_date'] = pd.to_datetime(df_movies['release_date'], format='%Y-%m-%d', errors='coerce') #Para confirmar el formato

@app.get('/cantidad_filmaciones_mes/{mes}', response_model=Dict[str, str])
def cantidad_filmaciones_mes(mes: str):
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes_lower = mes.lower() 
    if mes_lower not in meses:
        
        return {"error": "Mes inválido"}
    
    mes_num = meses[mes_lower]
    cantidad = df_movies[df_movies['release_date'].dt.month == mes_num].shape[0]
    
    return {"cantidad": f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"}

## FUNCIÓN 2. CANTIDAD DE PELICULAS ESTRENADAS EN UN DÍA

@app.get('/cantidad_filmaciones_dia/{dia}', response_model=Dict[str, str])
def cantidad_filmaciones_dia(dia: str):
    dia = dia.lower()
    dias_validos = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    if dia not in dias_validos:
       
        return {"error": f"Día inválido. Debe ser uno de los siguientes: {', '.join(dias_validos)}"}
    cantidad = df_movies[df_movies['release_day'] == dia].shape[0]

    return {"mensaje": f"{cantidad} películas fueron estrenadas un {dia}"}


## FUNCIÓN 3. SCORE DE UNA FILMACIÓN POR TITULO
 
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    titulo_limpio = titulo.strip().lower() #minusculas
    filmacion = df_movies[df_movies['title'].str.lower().str.strip() == titulo_limpio]
    if filmacion.empty:
        return {"error": "Película no encontrada"}
    score = filmacion['popularity'].values[0]
    año_estreno = filmacion['release_year'].values[0]
    
    return {
        "mensaje": f"La película '{titulo}' fue estrenada en el año {año_estreno} con un score de {score}"
    }

## FUNCIÓN 4. VOTOS POR TITULO

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    filmacion = df_movies[df_movies['title'].str.lower() == titulo.lower()]
    if filmacion.empty:
        return {"error": "Película no encontrada"}
    votos = filmacion['vote_count'].values[0]
    promedio_votos = filmacion['vote_average'].values[0]
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
    actor_data = df_movies[df_movies['Lead actor'].str.lower() == nombre_actor.lower()]
    
    if actor_data.empty:
        return {"error": "Actor no encontrado"}
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
    peliculas_info = df_movies[df_movies['Director'].str.lower() == nombre_director.lower()]
    if peliculas_info.empty:
        return {"error": "Director no encontrado"}

    info_peliculas = [] #nueva lista

    for _, row in peliculas_info.iterrows():
        info_peliculas.append({
            "título": row['title'],
            "fecha de lanzamiento": row['release_date'].strftime('%Y-%m-%d'),  # Formatear la fecha
            "retorno": row['return'],
            "costo": row['budget'],
            "ganancia": row['revenue']
        })

    return {
        "director": nombre_director,
        "películas dirigidas": info_peliculas
    }

## FUNCION DE RECOMENDACIÓN.



@app.get('/get_recommendation/{titulo}', response_model=List[str])
def recomendacion(titulo: str):
    try:
        titulo = re.sub(r'[^a-z\s]', '', titulo.lower())

        titulo_vector = tfidf_vectorizer.transform([titulo])

        cosine_similarities = cosine_similarity(titulo_vector, tfidf_matrix).flatten()

        similar_indices = cosine_similarities.argsort()[-6:-1][::-1]

        similar_titles = df_movies['original_title'].iloc[similar_indices].tolist()

        return similar_titles
    except Exception as e:
        return {"error": str(e)}