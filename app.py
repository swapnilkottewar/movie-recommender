import streamlit as st
import pandas as pd
import requests
from database import *
from recommender import build_model, recommend_from_preferences

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Movie Recommender 🎬", layout="wide")

import os
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# -------------------------------
# COLORFUL UI CSS
# -------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #141414, #1f1f2e);
}

h1 {
    text-align:center;
    color:#FF4B2B;
}

.card {
    background: linear-gradient(145deg, #1e1e2f, #252540);
    padding: 12px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.6);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px rgba(255,75,43,0.6);
}

img {
    border-radius: 12px;
    margin-bottom: 10px;
}

div[data-testid="column"] {
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# OMDb FUNCTION
# -------------------------------
@st.cache_data
def fetch_movie(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        data = requests.get(url).json()

        poster = data.get("Poster", "")
        rating = data.get("imdbRating", "N/A")
        year = data.get("Year", "N/A")

        if poster == "N/A":
            poster = "https://via.placeholder.com/300x450?text=No+Image"

        return poster, rating, year
    except:
        return "https://via.placeholder.com/300x450", "N/A", "N/A"

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    ratings = pd.read_csv("rating.csv")
    movies = pd.read_csv("movie.csv")

    ratings = ratings[ratings['userId'].isin(ratings['userId'].value_counts().head(500).index)]
    ratings = ratings[ratings['movieId'].isin(ratings['movieId'].value_counts().head(500).index)]

    return pd.merge(ratings, movies, on="movieId"), movies

data, movies = load_data()
_, similarity_df = build_model(data)

# -------------------------------
# SESSION STATE
# -------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "popup" not in st.session_state:
    st.session_state.popup = True

if "page" not in st.session_state:
    st.session_state.page = "home"

# -------------------------------
# LOGIN PAGE
# -------------------------------
if not st.session_state.user:

    st.title("🎬 Movie Recommender Login")

    mode = st.radio("Choose", ["Login", "Signup"])
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if mode == "Signup":
        if st.button("Create Account"):
            if register_user(u, p):
                st.success("Account created!")
            else:
                st.error("User exists")

    if mode == "Login":
        if st.button("Login"):
            if login_user(u, p):
                st.session_state.user = u
                st.session_state.popup = True
                st.rerun()
            else:
                st.error("Invalid credentials")

# -------------------------------
# POPUP (PREFERENCES)
# -------------------------------
elif st.session_state.popup:

    st.title("🎯 Choose Your Preferences")

    fav_movies = st.multiselect("Favorite Movies", movies["title"].unique())
    fav_genres = st.multiselect(
        "Favorite Genres",
        sorted(set("|".join(movies["genres"]).split("|")))
    )

    if st.button("Save"):
        save_preferences(st.session_state.user, fav_movies, fav_genres)
        st.session_state.popup = False
        st.rerun()

    if st.button("Skip"):
        st.session_state.popup = False
        st.rerun()

    st.stop()

# -------------------------------
# MAIN APP
# -------------------------------
else:

    # 🔥 TOP NAVIGATION
    nav = st.columns([6,1,1,1])

    with nav[1]:
        if st.button("🏠 Home"):
            st.session_state.page = "home"

    with nav[2]:
        if st.button("ℹ️ About"):
            st.session_state.page = "about"

    with nav[3]:
        if st.button("📞 Contact"):
            st.session_state.page = "contact"

    # 🔹 HOME PAGE
    if st.session_state.page == "home":

        st.sidebar.write(f"👤 {st.session_state.user}")

        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()

        st.title("🎬 Smart Movie Recommender")

        favs, genres = get_preferences(st.session_state.user)

        selected_genres = st.sidebar.multiselect(
            "🎛 Filter Genres",
            sorted(set("|".join(movies["genres"]).split("|"))),
            default=genres
        )

        if st.button("🚀 Recommend Movies"):

            results = recommend_from_preferences(
                favs,
                selected_genres,
                similarity_df,
                movies
            )

            # 🔥 UPDATE PREFERENCES
            if selected_genres:
                save_preferences(st.session_state.user, favs, selected_genres)

            st.subheader("✨ Recommended For You")

            # 🔥 FIXED GRID (NO OVERLAP)
            rows = [results[i:i+5] for i in range(0, len(results), 5)]

            for row in rows:
                cols = st.columns(5)

                for col, (_, movie) in zip(cols, row.iterrows()):
                    with col:
                        poster, rating, year = fetch_movie(movie['title'])

                        st.markdown(f"""
                        <div class="card">
                            <img src="{poster}" width="100%">
                            <h4>{movie['title']}</h4>
                            <p>{year} | ⭐ {rating}</p>
                            <p style="color:lightgray;">{movie['genres']}</p>
                        </div>
                        """, unsafe_allow_html=True)

    # 🔹 ABOUT PAGE
    elif st.session_state.page == "about":

        st.title("ℹ️ About")

        st.write("""
        🎬 Movie Recommendation System
        
        - Uses Collaborative Filtering  
        - Personalized recommendations  
        - Genre-based filtering  
        - OMDb API integration  
        
        Built using:
        Python | Streamlit | Machine Learning
        """)

    # 🔹 CONTACT PAGE
    elif st.session_state.page == "contact":

        st.title("📞 Contact")

        st.write("""
        👤 Swapnil Kottewar  
        🎓 AI Engineering Student  

        📧 swanilkottewar323@gmail.com  
        🔗 www.linkedin.com/in/swapnil-kottewar  
        
        Feel free to connect!
        """)