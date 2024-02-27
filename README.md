# NewsFinder-Contextual-Search-for-Personalized-News-Discovery
Revolutionizing news search: Contextual search using NLP &amp; ML for personalized, relevant news discovery. Efficient, precise, and user-friendly.

As a reader, I often struggle to find the most relevant news articles using traditional keyword-based search engines. Oftentimes, the search results are cluttered with irrelevant articles, making it challenging to discover the news that truly matters to me.

Realizing the limitations of keyword-based search, I became intrigued by the idea of contextual search, which takes into account the context and meaning of my search queries to deliver more precise results. Inspired by advancements in natural language processing and machine learning, I set out to build a contextual search system specifically tailored for news articles.

Utilizing cutting-edge technologies like Cohere's Large Language Model and a vector database, I embarked on a journey to revolutionize the way news is discovered online. My goal was to create a system that not only understands the topics I'm interested in but also identifies the most relevant news articles based on the context of my query.

## Process

The process begins by summarizing vast amounts of news articles using Cohere's Large Language Model. These summaries are then tokenized and stored in a vector database, allowing for efficient retrieval of relevant articles.

When a user enters a query, the system analyzes the context and meaning behind the query using advanced natural language processing techniques. It then compares the query against the tokenized summaries in the vector database to identify the most relevant news articles.

## Benefits

By leveraging the power of contextual search, users can now discover news articles that are tailored to their specific interests and preferences. Whether it's breaking news, in-depth analysis, or feature stories, the contextual search system ensures that users are presented with the most relevant and timely news articles, making the process of staying informed both efficient and enjoyable.

## Conclusion

Through this project, I aim to demonstrate the potential of contextual search in revolutionizing the way news is discovered and consumed online. By harnessing the capabilities of natural language processing and machine learning, we can empower readers to find the news that matters to them with greater ease and accuracy than ever before.

- Create a VirtualEnv to download libraries from the requirements.txt file provided.
- Run the `news_fetch.py file` to download and store the news in mongo database.
- Run the `python create_embed.py` file to create the embedding for the news data.
- Once that is done run the command `streamlit run app.py` to locally run the application.
- Store your news.api api key and mongo db connection string in the .env file to connect to the database and fetch news.
