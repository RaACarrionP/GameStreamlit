import streamlit as st
import pandas as pd
import json

# Cargar datos desde JSON con la codificación correcta
@st.cache
def load_data():
    with open('games.json', encoding='utf-8') as f:  # Añade encoding='utf-8'
        data = json.load(f)
    return pd.json_normalize(data)

data = load_data()

# Título del Dashboard
st.title('Dashboard de Videojuegos')

# Selección de un videojuego para mostrar detalles
option = st.selectbox('Selecciona un videojuego', data['Title'].unique())
selected_game = data[data['Title'] == option]

# Mostrar detalles del videojuego seleccionado
st.subheader('Detalles del Videojuego')
st.write('Fecha de lanzamiento:', selected_game.iloc[0]['Release Date'])
st.write('Equipo:', selected_game.iloc[0]['Team'])
st.write('Rating:', selected_game.iloc[0]['Rating'])
st.write('Número de reseñas:', selected_game.iloc[0]['Number of Reviews'])
st.write('Géneros:', selected_game.iloc[0]['Genres'])
st.write('Resumen:', selected_game.iloc[0]['Summary'])

# Mostrar críticas
st.subheader('Críticas')
reviews = selected_game.iloc[0]['Reviews'].strip('[]').replace('\'', '').split(',')
for review in reviews:
    st.info(review)