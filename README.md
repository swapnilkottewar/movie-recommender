Movie Recommendation System

A personalized Movie Recommendation Web Application built using Machine Learning and Streamlit.
This system recommends movies based on user preferences, favorite movies, and selected genres.

Features:
- User Authentication (Login & Signup)
- Personalized Movie Recommendations
- Favorite Movies Selection (Optional)
- Genre-Based Filtering (Dynamic)
- IMDb Ratings, Posters & Year (OMDb API)
- Attractive Netflix-style UI
- Optimized for Fast Performance
- Adaptive Recommendation

How It Works:
Uses Item-Based Collaborative Filtering:
1. User-Item Matrix
2. Cosine Similarity
3. Recommendations based on favorites, genres, and similarity

Tech Stack:
- Frontend: Streamlit
- Backend: Python
- Database: SQLite
- ML: Collaborative Filtering
- API: OMDb API

Project Structure:
- app.py
- database.py
- recommender.py
- rating_small.csv
- movie.csv
- requirements.txt

Installation:
1. Clone repo
2. pip install -r requirements.txt
3. Add OMDb API key
4. Run: streamlit run app.py

Deployment:
- Use Streamlit Cloud
- Connect GitHub repo
- Add API key in secrets

Dataset:
- MovieLens (Reduced)
- Contains users, movies, ratings

Future Enhancements:
- Trailer integration
- Like/Dislike system
- Search feature
- Deep learning model

Author:
Swapnil Kottewar
B.Tech AI Engineering

