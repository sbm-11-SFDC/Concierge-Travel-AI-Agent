from fastapi import FastAPI, Request
import uvicorn
import os
from sessions.in_memory_session import InMemorySessionService
from tools.gemini_websearch import search_with_gemini

app = FastAPI(title="Travel Agent")
# CORS — allow local web UI (localhost:8080) to call this API during development
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_store = InMemorySessionService()

TRAVEL_PORT = int(os.getenv('TRAVEL_PORT', 8005))

def synthesize_plan(user_text, raw_search_text):
    # Build a single prompt safely by concatenation
    prompt = "You are TripConcierge. User request: " + user_text + "\n\n"
    prompt += "Use the following raw search results as sources and create a compact trip plan:\n"
    prompt += "- 3-day itinerary (morning/afternoon/evening)\n"
    prompt += "- 3 recommended hotels with short notes and approximate price if available\n"
    prompt += "- Top 6 attractions with one-line reasons\n"
    prompt += "- Approximate budget summary\n"
    prompt += "- Provide source citations (list URLs or mention source names)\n\n"
    prompt += "Raw search results:\n" + raw_search_text
    # Ask Gemini (via search_with_gemini) to synthesize using the provided raw search text
    plan_text = search_with_gemini(prompt, max_results=5)
    return plan_text

@app.post('/agent/task')
async def handle_task(req: Request):
    payload = await req.json()
    task_id = payload.get('task_id')
    user_query = payload.get('payload', {}).get('query') or payload.get('payload', {}).get('text')
    if not user_query:
        return {'error':'no query provided', 'task_id':task_id}
    # 1) Live search via Gemini
    raw_search = search_with_gemini(user_query, max_results=6)
    # 2) Synthesize a formatted plan
    plan = synthesize_plan(user_query, raw_search)
    session_store.save(task_id, {'raw_search': raw_search, 'plan': plan})
    return {'task_id': task_id, 'plan': plan}

if __name__ == '__main__':
    uvicorn.run('agents.travel_agent:app', host='0.0.0.0', port=TRAVEL_PORT)
