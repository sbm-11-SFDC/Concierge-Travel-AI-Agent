import threading
import uuid

class InMemorySessionService:
    def __init__(self):
        self._lock = threading.Lock()
        self.sessions = {}   # session_id -> dict

    def create(self):
        sid = str(uuid.uuid4())[:8]
        with self._lock:
            self.sessions[sid] = {"state":"NEED_INTENT", "data":{}}
        return sid

    def load(self, sid):
        with self._lock:
            return self.sessions.get(sid, None)

    def save(self, sid, data):
        with self._lock:
            self.sessions.setdefault(sid, {}).update(data)

    def update_state(self, sid, state):
        with self._lock:
            if sid in self.sessions:
                self.sessions[sid]['state'] = state

    def delete(self, sid):
        with self._lock:
            if sid in self.sessions:
                del self.sessions[sid]
