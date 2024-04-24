import pathlib
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

def virtual_assistant(user_input):
  try:
    response = model.generate_content(user_input)
    for candidate in response.candidates:
        a = [part.text for part in candidate.content.parts]
        return {
          "message": a[0],
          "status": 200,
          "error": [] 
        }
  except Exception as e:
    return {
          "status": 500,
          "message": e 
        }