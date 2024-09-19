import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df_movies = pd.read_csv('Exitosas_1990.csv')

df_movies['original_title'] = df_movies['original_title'].str.lower().str.replace('[^a-z\s]', '')

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df_movies['original_title'])

def recomendacion(titulo):
    titulo = titulo.lower().replace('[^a-z\s]', '')
    titulo_vector = tfidf_vectorizer.transform([titulo]) # Para vectorizar el titulo ingresado
    cosine_similarities = cosine_similarity(titulo_vector, tfidf_matrix).flatten() #Calcula similitud
    similar_indices = cosine_similarities.argsort()[-6:-1][::-1]  # Obtener los 5 titulos más similares
    similar_titles = df_movies['original_title'].iloc[similar_indices].tolist()
    return similar_titles