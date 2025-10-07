import streamlit as st
import pickle


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]


movies_df = pickle.load(open('movies.pkl', 'rb'))
movies_titles = movies_df['title'].values
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select the Movie you like.",
    movies_titles
)

if st.button("Recommend"):
    recommend(selected_movie_name)
    st.write(selected_movie_name)
