import os, sys, json, traceback
from dotenv import load_dotenv
load_dotenv()
try:
    import google.generativeai as genai
except Exception as e:
    print("IMPORT_ERR:", e)
    sys.exit(1)

# configure
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Calling list_models with 60s timeout... (this may take a few seconds)")
try:
    models = genai.list_models(timeout=60)
    out = []
    for m in models:
        try:
            # try to get name/desc safely
            name = getattr(m, "name", None) or getattr(m, "model", None) or str(m)
            out.append(str(name))
        except Exception:
            out.append(str(m))
    print("MODELS_FOUND:")
    for x in out:
        print(" -", x)
except Exception as e:
    print("LIST_MODELS_FAILED:", e)
    traceback.print_exc()