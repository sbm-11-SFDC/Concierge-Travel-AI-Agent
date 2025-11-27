from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, uuid, os, httpx
from sessions.in_memory_session import InMemorySessionService

app = FastAPI(title="Coordinator")
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


# Allow local web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:9000', 'http://127.0.0.1:9000', 'http://localhost', 'http://127.0.0.1'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

session_store = InMemorySessionService()
COORD_PORT = int(os.getenv('COORD_PORT', 8000))

# Build TRAVEL_AGENT with safe concatenation to avoid nested-quote issues
travel_port_env = os.getenv('TRAVEL_PORT', '8005')
TRAVEL_AGENT = os.getenv('TRAVEL_AGENT') or ("http://localhost:" + travel_port_env + "/agent/task")

def need_more_info(session):
    s = session.get('data', {})
    return 'intent' not in s or not s['intent']

@app.post('/start_convo')
async def start_convo(req: Request):
    sid = session_store.create()
    # Ask the user for the trip intent
    prompt = 'Hello — where would you like to travel? Provide destination, rough dates, and any preferences (e.g., beaches, nightlife, budget).'
    return {'session_id': sid, 'prompt': prompt}

@app.post('/reply')
async def reply(req: Request):
    body = await req.json()
    sid = body.get('session_id')
    text = body.get('text')
    if not sid or not text:
        return {'error':'need session_id and text'}

    session = session_store.load(sid)
    if session is None:
        return {'error':'invalid session_id'}

    # Save the latest user text into session
    session_store.save(sid, {'last_user': text})
    # If we still need intent (first user input), store it as intent and call travel agent
    if need_more_info(session):
        session_store.save(sid, {'data': {'intent': text}})
        # Move to searching
        session_store.update_state(sid, 'SEARCHING')
        # Call travel agent
        task_id = 'T-' + str(uuid.uuid4())[:8]
        payload = {'task_id': task_id, 'payload': {'query': text}}
        async with httpx.AsyncClient() as client:
            resp = await client.post(TRAVEL_AGENT, json=payload, timeout=120.0)
            if resp.status_code != 200:
                session_store.update_state(sid, 'ERROR')
                return {'error':'travel agent failed', 'details': resp.text}
            plan = resp.json().get('plan')
        session_store.save(sid, {'last_plan': plan})
        session_store.update_state(sid, 'DELIVERED')
        return {'session_id': sid, 'plan': plan}
    else:
        return {'session_id': sid, 'prompt': 'I have your earlier intent. Do you want to refine it, or shall I prepare a plan?'}

if __name__ == '__main__':
    uvicorn.run('agents.coordinator_agent:app', host='0.0.0.0', port=COORD_PORT)
