import os
import time
import streamlit as st
from dotenv import load_dotenv
from searching import retrieve_top_similar_news


def main(connection_string):
    st.title("News Search")

    # Input field for user query
    user_query = st.text_input("Enter your query:")

    if st.button("Search"):
        # Retrieve top similar news
        start = time.time()
        similar_news = retrieve_top_similar_news(user_query,connection_string)
        end = time.time()
        st.subheader("Top 3 most similar news items:")
        for i, (title, similarity_score) in enumerate(similar_news, 1):
            st.write(f"{i}. Title: {title}")
            st.write(f"   Similarity Score: {similarity_score}")
            st.write("---")

        st.write(f"Time consumed {end-start} seconds")
if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get('api_key')
    connection_string = os.environ.get('connection_string')
    main(connection_string)
