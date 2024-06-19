import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from collections import Counter

# Cargar y preparar datos
@st.cache(allow_output_mutation=True)
def load_data():
    with open('games.json', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    df['Genres'] = df['Genres'].apply(eval)  # Convertir strings de listas a listas reales
    return df

data = load_data()

# Título del Dashboard
st.title('Dashboard de Videojuegos')

# Seleccionar un videojuego para mostrar detalles
option = st.selectbox('Selecciona un videojuego', data['Title'].unique())
selected_game = data[data['Title'] == option]

# Mostrar detalles del juego seleccionado
st.subheader('Detalles del Videojuego')
st.write('Fecha de lanzamiento:', selected_game.iloc[0]['Release Date'])
st.write('Equipo:', selected_game.iloc[0]['Team'])
st.write('Rating:', selected_game.iloc[0]['Rating'])
st.write('Número de reseñas:', selected_game.iloc[0]['Number of Reviews'])
st.write('Géneros:', ', '.join(selected_game.iloc[0]['Genres']))
st.write('Resumen:', selected_game.iloc[0]['Summary'])

# Visualización: Distribución de Géneros en el Dataset
st.subheader('Distribución de Géneros en el Dataset')
genre_counts = Counter([genre for sublist in data['Genres'] for genre in sublist])
fig, ax = plt.subplots()
pd.Series(genre_counts).sort_values(ascending=False).plot(kind='bar', ax=ax, color='skyblue')
ax.set_title('Frecuencia de Géneros de Videojuegos')
ax.set_xlabel('Género')
ax.set_ylabel('Cantidad')
st.pyplot(fig)

# Encontrar y mostrar juegos similares basados en género
st.subheader(f'Juegos similares a "{option}" basados en género')
similar_genres = set(selected_game.iloc[0]['Genres'])
similar_games = data[data['Genres'].apply(lambda genres: any(genre in similar_genres for genre in genres))]
st.write(similar_games[['Title', 'Release Date', 'Rating']])
