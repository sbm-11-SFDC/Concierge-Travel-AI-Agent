import os, json
from dotenv import load_dotenv
load_dotenv()
try:
    import google.generativeai as genai
except Exception as e:
    print("google.generativeai import failed:", e); raise

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    models = genai.list_models()
    # Try to print a readable list
    for m in models:
        try:
            print("NAME:", getattr(m, "name", m))
        except Exception:
            print("MODEL:", m)
except Exception as e:
    print("list_models failed:", e)
