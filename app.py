import streamlit as st
import pickle
import requests
import requests, certifi
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import time

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5b3ba3a43d1c424a51014c165767ae07&language=en-US"
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
            else:
                return None
        except requests.exceptions.RequestException as e:
            st.warning(f"Retry {attempt+1}/3 failed: {e}")
            time.sleep(2)
    st.error(f"Failed to fetch poster for movie_id {movie_id}")
    return None


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movies_df.iloc[i[0]].movie_id))
    return recommended_movies, recommended_movies_posters


similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_df = pickle.load(open('movies.pkl', 'rb'))
movies_titles = movies_df['title'].values
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select the Movie you like.",
    movies_titles
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
