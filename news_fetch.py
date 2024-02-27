import os
import json
from dotenv import load_dotenv
from newsapi import NewsApiClient
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()
 
api_key = os.environ.get('api_key')
connection_string = os.environ.get('connection_string')

# Initialize News API client with your API key
newsapi = NewsApiClient(api_key=api_key)

# Connect to MongoDB
client = MongoClient(connection_string) 
db = client['ContextualSearch']  
news_collection = db['news']

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

# Close the MongoDB connection
client.close()
