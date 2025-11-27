from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# Client reads GEMINI_API_KEY automatically from environment
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",      # or models/gemini-2.5-pro
    contents="Explain how AI works in a few words"
)

print("TEXT:", getattr(response, "text", None) or str(response))
