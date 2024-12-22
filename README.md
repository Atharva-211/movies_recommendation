Movie Recommender System

Welcome to the Movie Recommender System – an application built to enhance your movie-watching experience by recommending films based on your preferences. Whether you're into action-packed thrillers or heartwarming dramas, this system will find the perfect movies for you.

Overview
--------
The Movie Recommender System is powered by a robust algorithm that takes in your movie choice and recommends similar movies using Content-Based Filtering. It leverages a similarity matrix calculated from various features like genres, keywords, cast, and crew to suggest movies you’ll likely enjoy.

How It Works
-------------
The heart of the recommendation engine lies in how we transform movie data into meaningful features and calculate similarities between them. Here’s the breakdown:

1. Data Collection:
   - Movie data is sourced from TMDB (The Movie Database), which includes essential information such as the movie's title, overview, genres, keywords, cast, and crew.
   - The raw data is cleaned and transformed into usable formats, removing unnecessary spaces, and converting certain fields (like genres and cast) into lists.

2. Feature Engineering:
   - The text from the overview, genres, keywords, cast, and crew is combined into a single tags field for each movie. This gives us a rich set of descriptive features that capture the essence of the movie.
   - The tags are then preprocessed using stemming to reduce words to their root form (e.g., "dancing" becomes "danc").

3. Vectorization:
   - A Count Vectorizer is applied to convert the textual data into numerical form. It creates a matrix of features representing the frequency of each word in the movie descriptions.

4. Similarity Calculation:
   - With the vectorized data, the algorithm calculates the Cosine Similarity between movies. This measures how similar two movies are, based on the features we extracted.

5. Recommendations:
   - Once the similarity matrix is ready, the system can recommend movies by finding the top 5 most similar movies to the one you selected.

Technologies Used
-----------------
- Python: For processing the movie data and implementing the recommendation algorithm.
- Streamlit: To deploy the web app and create a beautiful user interface.
- Pandas: To manage and clean the dataset.
- Scikit-learn: For creating the vectorizer and calculating cosine similarity.
- TMDB API: To fetch movie details like posters and metadata.
- NLTK: To preprocess and stem the movie descriptions.

Recommendation Algorithm
-------------------------
The recommendation system works on Content-Based Filtering, where the goal is to recommend items that are similar to those a user has already shown interest in. Here's how it works in this project:

1. Movie Features Extraction:
   - We extract and combine multiple features (genres, cast, crew, etc.) into a comprehensive tags list for each movie. These tags are what define the essence of a movie.

2. Cosine Similarity:
   - Once we have the tags, we apply a Count Vectorizer to convert the text into numerical data. Then, we calculate the cosine similarity between the movies based on these features. Cosine similarity measures the angle between two vectors, and the closer the angle, the more similar the items are.

3. Final Recommendations:
   - For each movie, the system identifies the top 5 movies that have the highest similarity score and recommends them to you. It’s like having your personal movie expert that knows exactly what you like.

How to Use
-----------
1. Open the app at [Movie Recommender](https://atharva-211-movies-recommendation-movies-feapp-zxdti5.streamlit.app/).
2. Select a movie from the dropdown list.
3. Hit the Recommend button to see a list of movies that are similar to the one you picked.
4. Enjoy your personalized movie recommendations!

Setup & Installation
---------------------
If you want to run this on your local machine, here’s how to set it up:

1. Clone the repository:
   git clone https://github.com/atharv-gaikwad/movie-recommender.git
   cd movie-recommender

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   streamlit run app.py

4. Visit http://localhost:8501 to start using the recommender.

Files in the Repository
------------------------
- app.py: The main Streamlit application that runs the UI.
- movies.pkl: The serialized movie dataset used for recommendations.
- movie_dict.pkl: A dictionary representation of the movie dataset for easy access.
- similarity.pkl: The precomputed similarity matrix for efficient recommendation.

Algorithm Insights
------------------
- Cosine Similarity: By measuring the cosine of the angle between two vectors in a multi-dimensional space, we calculate how similar the two movies are. The closer the value is to 1, the more similar the movies are.
- Stemming: The Porter Stemmer is used to reduce words to their base form, making it easier to match similar terms across movies (e.g., "dancing", "danced" becomes "danc").
- Count Vectorizer: The CountVectorizer takes care of converting the tags into a bag of words representation, capturing how often each word appears across the movie descriptions.

Contributors
------------
- Atharva Gaikwad: Creator, Developer, and Lead Engineer.

License
-------
This project is open source and available under the MIT License. Feel free to fork, modify, and contribute back to the project!

Let the movie marathon begin. If you find this system more accurate than a Hollywood agent, I’ll be impressed. Enjoy the movies!
