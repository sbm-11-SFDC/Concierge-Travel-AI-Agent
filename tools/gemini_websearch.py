import os, time, concurrent.futures
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GENAI_MODEL = os.getenv("GENAI_MODEL", "models/gemini-2.5-pro")
GENAI_TIMEOUT_SEC = int(os.getenv("GENAI_TIMEOUT_SEC", "60"))
GENAI_RETRIES = int(os.getenv("GENAI_RETRIES", "1"))

try:
    from google import genai
except Exception as e:
    genai = None
    _IMPORT_ERR = str(e)

def _extract_text_from_response(resp):
    if resp is None:
        return None
    text = getattr(resp, "text", None)
    if text:
        return text
    cand = getattr(resp, "candidates", None) or getattr(resp, "output", None)
    if cand:
        first = cand[0]
        for attr in ("content", "text"):
            v = getattr(first, attr, None)
            if v:
                return v if isinstance(v, str) else str(v)
        try:
            if isinstance(first, dict):
                return first.get("text") or first.get("content") or str(first)
        except Exception:
            pass
    return str(resp)

def _call_generate(client, prompt):
    # Note: call generate_content WITHOUT passing a 'timeout' kwarg
    return client.models.generate_content(model=GENAI_MODEL, contents=prompt)

def search_with_gemini(query: str, max_results: int = 5):
    if genai is None:
        raise RuntimeError("google.genai import failed: " + _IMPORT_ERR)

    client_kwargs = {}
    if GEMINI_API_KEY:
        client_kwargs["api_key"] = GEMINI_API_KEY

    client = genai.Client(**client_kwargs)
    prompt = f"Search the web for: {query}. Summarize the top results in short bullets and include citations (URLs or source names)."

    last_err = None
    for attempt in range(GENAI_RETRIES + 1):
        try:
            # run generate_content in a thread and enforce timeout at Python level
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
                fut = ex.submit(_call_generate, client, prompt)
                try:
                    resp = fut.result(timeout=GENAI_TIMEOUT_SEC)
                except concurrent.futures.TimeoutError:
                    # attempt cancellation, then raise a clear error
                    fut.cancel()
                    raise RuntimeError(f"Gemini timed out after {GENAI_TIMEOUT_SEC} seconds.")
            text = _extract_text_from_response(resp)
            if text and text.strip():
                return text
            return str(resp)
        except Exception as e:
            last_err = e
            if attempt < GENAI_RETRIES:
                time.sleep(1 + attempt * 2)
            else:
                break

    raise RuntimeError(f"Gemini call failed after {GENAI_RETRIES+1} attempts. Last error: {last_err}")
