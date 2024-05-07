from celery import shared_task
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from newsapi.newsapi_client import NewsApiClient

load_dotenv()

# Initialize MongoDB connection
connection_string = os.environ.get('connection_string')
client = MongoClient(connection_string) 
db = client['ContextualSearch']  
news_collection = db['news']

@shared_task(bind=True)
def add_data(self):
    """
    Task to fetch news articles from News API and store them in MongoDB.
    """
    # Initialize News API client with your API key
    api_key = os.environ.get('api_key')
    newsapi = NewsApiClient(api_key=api_key)

    topics = ["machinelearning", "technology", "science", "business", "health", "startups"]

    structured_data = []

    for topic in topics:
        articles_for_topic = newsapi.get_everything(q=topic, page=2).get("articles", [])
        topic_data = {"Topic": topic, "Data": []}

        for article in articles_for_topic:  
            title = article.get("title", "")    
            description = article.get("description", "")
            content = article.get("content", "")
            author = article.get("author", "")
            url = article.get("url", "")
            url_to_image = article.get("urlToImage", "")
            published_at = article.get("publishedAt", "")

            # Add data to the 'Data' list
            news_entry = {"title": title, "description": description, "content": content}
            topic_data["Data"].append(news_entry)

            # Add metadata to the 'MetaData' section
            metadata = {
                "author": author,
                "url": url,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
            }
            news_entry["MetaData"] = {title: metadata}

        # Append the structured data to the list
        structured_data.append(topic_data)

    # Insert data into the MongoDB collection
    news_collection.insert_many(structured_data)

@shared_task(bind=True)
def embedding_create(self):
    """
    Task to create embeddings for news articles and store them in MongoDB.
    """
    # Load SentenceTransformer model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Iterate over each document in the "news" collection
    for topic_document in news_collection.find():
        topic = topic_document['Topic']
        data = topic_document['Data']
        for news_item in data:
            if 'vector' not in news_item:
                content = news_item['content']
                
                # Generate embedding for the content
                embedding = model.encode(content)
                
                # Add the embedding to the news item
                news_item['vector'] = embedding.tolist()

        # Update the news document with the embeddings
        news_collection.update_one({'_id': topic_document['_id']}, {'$set': {'Data': data}})

    print("Embeddings stored within each news document.")

