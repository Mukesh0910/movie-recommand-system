import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key=855c5de57c7fa0650d26bf1933f4230b&language=en-US'
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .movie-container {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        .movie-card {
            text-align: center;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }
        .movie-card:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
            background-color: #f9f9f9;
        }
        img {
            border-radius: 10px;
        }
        .movie-title {
            font-weight: bold;
            font-size: 1rem;
            margin-top: 10px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# App header
st.title('🎬 Movie Recommender System')
st.markdown("#### Discover your next favorite movie! Just pick one you love, and we'll do the rest.")

# Dropdown for movie selection
selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown:',
    movies['title'].values
)

# Button to get recommendations
if st.button('Get Recommendations 🎥'):
    names, posters, ids = recommend(selected_movie_name)

    # Display the recommended movies
    st.markdown("### Recommended Movies:")
    movie_cols = st.columns(5)  # Create 5 equal columns for movie cards

    for col, name, poster, movie_id in zip(movie_cols, names, posters, ids):
        with col:
            # Create interactive movie card
            movie_link = f"https://www.themoviedb.org/movie/{movie_id}"
            col.markdown(
                f"""
                <div class="movie-card">
                    <a href="{movie_link}" target="_blank">
                        <img src="{poster}" alt="{name}" width="100%" />
                        <div class="movie-title">{name}</div>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

# Footer
st.markdown("---")
st.markdown("💡 Developed with ❤️ using [Streamlit](https://streamlit.io/).")
