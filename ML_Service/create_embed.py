import os
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
load_dotenv()

connection_string = os.environ.get('connection_string')

client = MongoClient(connection_string)

# Access your database
db = client.get_database("ContextualSearch")

# Access the "news" collection
news_collection = db['news']

# Load the SentenceTransformer model
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
