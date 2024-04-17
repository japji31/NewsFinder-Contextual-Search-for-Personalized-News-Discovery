import numpy as np
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

def retrieve_top_similar_news(user_query,connection_string):
    # Connect to MongoDB
    connection_string = connection_string
    client = MongoClient(connection_string)

    # Access your database
    db = client.get_database("ContextualSearch")

    # Access your collection
    collection = db.get_collection("news")

    # Load the SentenceTransformer model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Function to generate embedding for user input
    def generate_embedding(text):
        return model.encode(text).reshape(1, -1)

    # Function to calculate cosine similarity between two vectors
    def calculate_similarity(vector1, vector2):
        return cosine_similarity(vector1, vector2)[0][0]

    # Function to retrieve top 3 news items with highest similarity scores
    def retrieve_top_news(user_embedding):
        top_news = []
        for document in collection.find({}):
            topic = document['Topic']
            data = document['Data']
            for news_item in data:
                title_embedding = np.array(news_item.get('vector', [])).reshape(1, -1)
                similarity_score = calculate_similarity(user_embedding, title_embedding)
                top_news.append((news_item['title'], similarity_score))
        
        top_news.sort(key=lambda x: x[1], reverse=True)
        return top_news[:3]

    # Generate embedding for user query
    user_embedding = generate_embedding(user_query)

    # Retrieve top 3 similar news items
    top_news = retrieve_top_news(user_embedding)

    return top_news

if __name__ == "__main__":
    load_dotenv()
    connection_string = os.environ.get('connection_string')
    query = input("Enter your query: ")
    similar_news = retrieve_top_similar_news(query,connection_string)
    print("Top 3 most similar news items:")
    for i, (title, similarity_score) in enumerate(similar_news, 1):
        print(f"{i}. Title: {title}")
        print(f"   Similarity Score: {similarity_score}")
        print()
