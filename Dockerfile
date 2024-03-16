# Use the official Python 3.10.5 image as the base image
FROM python:3.10.5-slim 

# Set the working directory in the container
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git

# Clone your Git repository
RUN git clone https://github.com/japji31/NewsFinder-Contextual-Search-for-Personalized-News-Discovery.git .

# Copy the .env file into the container
COPY .env /app/.env

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory for the runtime environment
WORKDIR /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the streamlit command when the container launches
CMD ["streamlit", "run", "app.py"]
