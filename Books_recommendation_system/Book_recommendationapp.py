import streamlit as st
import pandas as pd
import pickle

# Load the data
user_item_matrix = pickle.load(open('user_item_matrix.pkl', 'rb'))
user_similarity_df = pickle.load(open('user_similarity.pkl', 'rb'))

# Define the recommend function
def recommend_books(user_id, user_item_matrix, user_similarity_df, top_n=10):
    if user_id not in user_item_matrix.index:
        return "User not found.", []
    
    # Find top 5 similar users
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).drop(user_id)
    top_users = similar_users.head(5).index

    # Get their ratings
    similar_ratings = user_item_matrix.loc[top_users]

    # Average the ratings of similar users
    mean_ratings = similar_ratings.mean(axis=0)

    # Remove books already rated by this user
    books_rated_by_user = user_item_matrix.loc[user_id]
    rated_books = books_rated_by_user[books_rated_by_user > 0].index
    recommendations = mean_ratings.drop(index=rated_books)

    # Return top N recommended books
    return "Success", recommendations.sort_values(ascending=False).head(top_n).index.tolist()

# Streamlit UI
st.title("📚 User-Based Book Recommendation System")

# Ask for User ID
user_ids = user_item_matrix.index.tolist()
selected_user = st.selectbox("Select User ID:", user_ids)

if st.button("Recommend Books"):
    status, recommendations = recommend_books(
        user_id=selected_user,
        user_item_matrix=user_item_matrix,
        user_similarity_df=user_similarity_df,
        top_n=5
    )
    
    if status == "User not found.":
        st.error("User ID not found in the system.")
    else:
        st.subheader("📖 Top 5 Book Recommendations:")
        for i, book in enumerate(recommendations):
            st.markdown(f"**{i+1}. {book}**")
