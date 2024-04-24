import json
from dotenv import load_dotenv
import os
import google.generativeai as genai
from channels.generic.websocket import AsyncWebsocketConsumer
from .chatbot import virtual_assistant

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"status": "WebSocket connected"}))

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            response = await self.process_message(message['text'])
            await self.send(text_data=json.dumps({"Reply": response['message']}))
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def process_message(self, message):
        try:
            load_dotenv()
            api_key = os.getenv('GOOGLE_API_KEY')


            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')

            return virtual_assistant(message)
        except Exception as e:
            return str(e) 