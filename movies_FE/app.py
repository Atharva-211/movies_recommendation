import streamlit as st
import pandas as pd
import pickle
import requests
import os

# Function to load and merge split pickle files
def load_split_pickle(file_parts):
    data = b""
    for part in file_parts:
        with open(part, 'rb') as f:
            data += f.read()
    return pickle.loads(data)

# Fetch movie poster from API
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=99361ee55cf8bdd0e5d4a5197223425a&language=en-US'
        )
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Specify file paths for the split similarity matrix
similarity_file_parts = [
    'similarity.pkl_part0',
    'similarity.pkl_part1'
]

# Load similarity matrix from split files
similarity = load_split_pickle(similarity_file_parts)

# Streamlit App
st.set_page_config(page_title="Movies Recommender", layout="wide")

# App title with styling
st.markdown("""
    <style>
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #FF6347;
            text-align: center;
        }
        .instructions {
            font-size: 18px;
            color: #444;
            text-align: center;
        }
        /* Animation for the movie posters */
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .movie-poster {
            animation: fadeIn 0.5s ease-out;
        }
    </style>
    <h1 class="title">🎥 Movie Recommender System 🎬</h1>
    <p class="instructions">Select a movie from the dropdown below to get personalized recommendations.</p>
""", unsafe_allow_html=True)

# Movie selection
selected_movie_name = st.selectbox(
    "Choose a movie to get recommendations:", movies['title'].values
)

# Recommend button
if st.button("Recommend"):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie_name)

    # Display recommendations in a grid with animation
    st.markdown("## Recommended Movies:")
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f"""
                <div class="movie-poster">
                    <img src="{poster}" style="width: 100%; border-radius: 8px;" />
                    <p style="text-align: center; font-size: 14px; font-weight: bold;">{name}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align: center; font-size: 16px;'>Click the button to get started!</p>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr>
    <footer style="text-align: center; font-size: 14px;">
        Created with ❤️ using Streamlit. <br>
        Powered by TMDB API. <br>
        © 2024 Atharva Gaikwad
    </footer>
""", unsafe_allow_html=True)
