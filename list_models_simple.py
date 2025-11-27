import os, sys, traceback
from dotenv import load_dotenv
load_dotenv()
try:
    import google.generativeai as genai
except Exception as e:
    print("IMPORT_ERR:", e)
    sys.exit(1)

key = os.getenv("GEMINI_API_KEY")
if not key:
    print("NO_KEY")
    sys.exit(1)

try:
    genai.configure(api_key=key)
    models = genai.list_models()
    print("MODELS_FOUND_COUNT:", len(models) if hasattr(models, "__len__") else "unknown")
    for m in models:
        try:
            # many model objects have .name or .model
            name = getattr(m, "name", None) or getattr(m, "model", None) or str(m)
            print(" -", name)
        except Exception:
            print(" -", m)
except Exception as e:
    print("LIST_MODELS_ERROR:", e)
    traceback.print_exc()
