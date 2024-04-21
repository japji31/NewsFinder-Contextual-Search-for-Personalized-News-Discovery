import json
from dotenv import load_dotenv
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from chatbot import virtual_assistant

class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()
        print("WebSocket connected.")

    async def receive(self, text_data):
        response = await self.process_message(text_data)

        # Send the response back to the client
        await self.send(text_data=json.dumps({
            'message': response['message']
        }))

    async def process_message(self, message):
        try:
            # Load environment variables
            load_dotenv()
            api_key = os.getenv('GOOGLE_API_KEY')

            # Initialize ML service
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')

            # Process message using virtual assistant
            return virtual_assistant.process_message(message)
        except Exception as e:
            return str(e)  # Handle errors gracefully