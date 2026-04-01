import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def build_model(data):
    matrix = data.pivot_table(
        index="userId",
        columns="title",
        values="rating"
    ).fillna(0).astype("float32")

    similarity = cosine_similarity(matrix.T)

    similarity_df = pd.DataFrame(
        similarity,
        index=matrix.columns,
        columns=matrix.columns
    )

    return matrix, similarity_df


def recommend_from_preferences(fav_movies, selected_genres, similarity_df, movies, n=10):

    scores = pd.Series(dtype=float)

    # 🔥 PRIORITY: GENRES
    if selected_genres:
        genre_movies = movies[
            movies["genres"].apply(lambda x: any(g in x for g in selected_genres))
        ]

        # Combine with favorites if available
        if fav_movies:
            for movie in fav_movies:
                if movie in similarity_df.columns:
                    scores = scores.add(similarity_df[movie], fill_value=0)

            if not scores.empty:
                rec_df = pd.DataFrame(scores, columns=["score"]).reset_index()
                rec_df.rename(columns={"index": "title"}, inplace=True)
                rec_df = rec_df.merge(movies, on="title", how="left")

                rec_df = rec_df[
                    rec_df["genres"].apply(lambda x: any(g in x for g in selected_genres))
                ]

                if not rec_df.empty:
                    return rec_df.head(n)

        return genre_movies.drop_duplicates("title").head(n)

    # 🔥 FAVORITES ONLY
    if fav_movies:
        for movie in fav_movies:
            if movie in similarity_df.columns:
                scores = scores.add(similarity_df[movie], fill_value=0)

        if not scores.empty:
            scores = scores.sort_values(ascending=False)

            rec_df = pd.DataFrame(scores, columns=["score"]).reset_index()
            rec_df.rename(columns={"index": "title"}, inplace=True)
            rec_df = rec_df.merge(movies, on="title", how="left")

            return rec_df.head(n)

    # 🔥 FALLBACK
    popular = movies.copy()
    popular["count"] = popular.groupby("title")["title"].transform("count")

    return popular.sort_values("count", ascending=False).drop_duplicates("title").head(n)