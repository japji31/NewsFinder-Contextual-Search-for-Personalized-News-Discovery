import numpy as np
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class SearchNews:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database("ContextualSearch")
        self.collection = self.db.get_collection("news")
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def generate_embedding(self, text):
        return self.model.encode(text).reshape(1, -1)

    def calculate_similarity(self, vector1, vector2):
        return cosine_similarity(vector1, vector2)[0][0]

    def retrieve_top_news(self, user_embedding):
        top_news = []
        for document in self.collection.find({}):
            data = document['Data']
            for news_item in data:
                title_embedding = np.array(news_item.get('vector', [])).reshape(1, -1)
                similarity_score = self.calculate_similarity(user_embedding, title_embedding)
                news_dict = {
                    "news": news_item['title'],
                    "score": similarity_score
                }
                top_news.append(news_dict)
        
        top_news.sort(key=lambda x: x["score"], reverse=True)
        return top_news[:3]
