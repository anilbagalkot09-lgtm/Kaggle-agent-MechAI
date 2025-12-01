import time

class InMemorySessionService:
    def __init__(self):
        self._store = {}

    def create(self, session_id: str, initial_state: dict):
        self._store[session_id] = {'state': initial_state, 'created_at': time.time()}

    def get(self, session_id: str):
        return self._store.get(session_id, {}).get('state')

    def update(self, session_id: str, delta: dict):
        if session_id not in self._store:
            raise KeyError('session not found')
        self._store[session_id]['state'].update(delta)

    def delete(self, session_id: str):
        if session_id in self._store:
            del self._store[session_id]
