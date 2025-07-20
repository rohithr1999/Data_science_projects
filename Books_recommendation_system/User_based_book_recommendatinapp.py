import streamlit as st
import pandas as pd
import pickle

# Load data
user_item_matrix = pickle.load(open('user_item_matrix.pkl', 'rb'))
user_similarity_df = pickle.load(open('user_similarity.pkl', 'rb'))
book_images = pickle.load(open('book_images.pkl', 'rb'))  # Book title → image URL

# Recommendation function
def recommend_books(user_id, user_item_matrix, user_similarity_df, top_n=10):
    if user_id not in user_item_matrix.index:
        return "User not found.", [], [], []

    # Find top 5 similar users
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).drop(user_id)
    top_users = similar_users.head(5).index

    # Get their ratings
    similar_ratings = user_item_matrix.loc[top_users]

    # Average ratings across similar users
    mean_ratings = similar_ratings.mean(axis=0)

    # Remove books already rated by the user
    books_rated_by_user = user_item_matrix.loc[user_id]
    rated_books = books_rated_by_user[books_rated_by_user > 0].index
    recommendations = mean_ratings.drop(index=rated_books)

    # Get top N recommendations
    top_books = recommendations.sort_values(ascending=False).head(top_n)
    titles = top_books.index.tolist()
    scores = top_books.values.tolist()
    images = [book_images.get(title, "") for title in titles]

    return "Success", titles, scores, images


# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Book Recommender", layout="centered")
st.title("📚 User-Based Book Recommendation System")

# User ID input
user_ids = user_item_matrix.index.tolist()
selected_user = st.selectbox("Select User ID:", user_ids)

# Radio button for top N books (5 to 20)
top_n = st.radio("Select number of books to recommend", [5, 10, 15, 20], index=0)

# Show recommendations
if st.button("📖 Recommend Books"):
    status, book_titles, scores, images = recommend_books(
        user_id=selected_user,
        user_item_matrix=user_item_matrix,
        user_similarity_df=user_similarity_df,
        top_n=top_n
    )

    if status == "User not found.":
        st.error("❌ User ID not found.")
    else:
        st.subheader(f"📖 Top {top_n} Book Recommendations:")

        for i, (title, score, img) in enumerate(zip(book_titles, scores, images), start=1):
            col1, col2 = st.columns([1, 4])
            with col1:
                if img:
                    st.image(img, width=100)
                else:
                    st.markdown("📕 No image")
            with col2:
                st.markdown(f"**{i}. {title}**")
                st.markdown(f"⭐ **Predicted Score**: {round(score, 2)}")