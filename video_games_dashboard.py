import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from collections import Counter

# Configurar la página
st.set_page_config(layout="wide")

# Cargar y preparar datos
@st.cache(allow_output_mutation=True)
def load_data():
    with open('games.json', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    df['Genres'] = df['Genres'].apply(eval)  # Convertir strings de listas a listas reales
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    df['Release Year'] = df['Release Date'].dt.year
    return df

data = load_data()

# Título del Dashboard
st.title('Dashboard de Videojuegos')

# Crear 2 columnas con más espacio
col1, col2 = st.columns((2, 3))

# Columna 1: Slider para seleccionar el año y mostrar juegos de ese año
with col1:
    st.subheader('Cantidad de Juegos por Año')
    year = st.slider('Seleccione el año', int(data['Release Year'].min()), int(data['Release Year'].max()), int(data['Release Year'].min()))
    games_in_year = data[data['Release Year'] == year]
    st.write(f"Juegos lanzados en el año {year}:")
    st.write(games_in_year[['Title', 'Release Date']])

    # Gráfico de la cantidad de juegos por año
    games_per_year = data.groupby('Release Year')['Title'].count().reset_index()
    games_per_year.columns = ['Año de Lanzamiento', 'Cantidad de Juegos']
    fig, ax = plt.subplots()
    ax.plot(games_per_year['Año de Lanzamiento'], games_per_year['Cantidad de Juegos'], marker='o')
    ax.set_title('Cantidad de Juegos por Año')
    ax.set_xlabel('Año de Lanzamiento')
    ax.set_ylabel('Cantidad de Juegos')
    st.pyplot(fig)

# Columna 2: Mostrar detalles del juego seleccionado
with col2:
    option = st.selectbox('Por nombre', data['Title'].unique())
    selected_game = data[data['Title'] == option]

    st.subheader('Detalles del Videojuego')
    st.write('Fecha de lanzamiento:', selected_game.iloc[0]['Release Date'].strftime('%b %d, %Y') if not pd.isna(selected_game.iloc[0]['Release Date']) else 'Desconocido')
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
