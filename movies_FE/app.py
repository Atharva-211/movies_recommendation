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
    recommended_movies_ratings = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_ratings.append(round(i[1] * 100, 1))
    return recommended_movies, recommended_movies_posters, recommended_movies_ratings


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity_file_parts = ['movies_FE/similarity.pkl_part0', 'movies_FE/similarity.pkl_part1']
similarity = load_split_pickle(similarity_file_parts)

# Page config
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with improved text visibility
st.markdown("""
    <style>
        /* Global Styles */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
        }

        /* Reduce overall page padding */
        .stApp {
            background-color: #1a1a1a;
            color: #ffffff;
        }

        .element-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
        }

        /* Header Styles with reduced padding */
        .main-header {
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
            padding: 1rem;  /* Reduced from 2rem */
            border-radius: 15px;
            margin-bottom: 1rem;  /* Reduced from 2rem */
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .title {
            font-size: 2.5rem;  /* Reduced from 3.5rem */
            font-weight: 700;
            background: linear-gradient(135deg, #FFF 0%, #F0F0F0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;  /* Reduced from 1rem */
        }

        .subtitle {
            color: #FFF;
            font-size: 1rem;  /* Reduced from 1.2rem */
            opacity: 0.9;
            margin: 0.3rem 0;  /* Added small margin */
        }

        /* Search Container with reduced padding */
        .search-container {
            background: #2d2d2d;
            padding: 1rem;  /* Reduced from 2rem */
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            margin-bottom: 1rem;  /* Reduced from 2rem */
        }

        .search-title {
            color: #ffffff;
            margin-bottom: 0.5rem;  /* Reduced from 1rem */
            font-size: 1.2rem;  /* Added smaller font size */
        }

        /* Movie Card Styles with reduced padding */
        .movie-card {
            background: #2d2d2d;
            border-radius: 15px;
            padding: 0.5rem;  /* Reduced from 1rem */
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 0.5rem;  /* Reduced from 1rem */
        }

        .movie-title {
            font-size: 0.9rem;  /* Reduced from 1rem */
            font-weight: 600;
            color: #ffffff;
            margin-top: 0.4rem;  /* Reduced from 0.8rem */
            text-align: center;
        }

        /* Footer with reduced padding */
        .footer {
            background: #2d2d2d;
            color: #ffffff;
            padding: 0.5rem;  /* Reduced from 1rem */
            border-radius: 10px;
            text-align: center;
            margin-top: 1rem;  /* Reduced from 2rem */
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        /* Adjust button padding */
        .stButton > button {
            padding: 0.5rem 1.5rem;  /* Reduced from 0.8rem 2rem */
        }

        /* Remove default streamlit paddings */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* Previous CSS styles remain the same */
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1 class="title">CineMatch 🎬</h1>
        <p class="subtitle">Find similar movies using content-based filtering and cosine similarity</p>
        <p style="color: #FFF; font-size: 0.9rem; opacity: 0.8; max-width: 800px; margin: 1rem auto;">
            Our system analyzes movie features like plot, genres, cast, and keywords to find the most similar films to your selection using advanced text processing and cosine similarity calculations.
        </p>
    </div>
""", unsafe_allow_html=True)

# Search section with dark theme
st.markdown("""
    <div class="search-container">
        <h3 class="search-title">🎥 Start Your Movie Journey</h3>
    </div>
""", unsafe_allow_html=True)

# Create three columns for layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    selected_movie_name = st.selectbox(
        "Select a movie you love:",
        movies['title'].values,
        index=None,
        placeholder="Search for a movie..."
    )

    # Create sub-columns for the button to center it
    button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
    with button_col2:
        recommend_button = st.button("Get Recommendations 🚀")

# Recommendations section
if recommend_button and selected_movie_name:
    with st.spinner("🎬 Finding perfect matches for you..."):
        names, posters, ratings = recommend(selected_movie_name)

    st.markdown("""
        <h2 style='color: #ffffff; text-align: center; margin: 2rem 0;'>
            🌟 Movies You'll Love 🌟
        </h2>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    for col, name, poster, rating in zip(cols, names, posters, ratings):
        with col:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{poster}" class="movie-poster" alt="{name}">
                    <h3 class="movie-title">{name}</h3>
                    <div style="text-align: center;">
                        <span class="match-score">{rating}% Match</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>Created with ❤️ by Atharva Gaikwad</p>
        <p>Powered by TMDB API | © 2024 CineMatch</p>
        <p style="font-size: 0.8rem; opacity: 0.8;">
            Movie data and posters provided by 
            <a href="https://www.themoviedb.org" target="_blank">The Movie Database</a>
        </p>
    </div>
""", unsafe_allow_html=True)