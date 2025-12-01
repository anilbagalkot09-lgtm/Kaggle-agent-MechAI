from typing import List, Dict, Any
import time

class MemoryBank:
    def __init__(self):
        self._records: List[Dict[str, Any]] = []

    async def add(self, key: str, value: Any, vector: List[float] = None):
        self._records.append({'key': key, 'value': value, 'vector': vector, 'ts': time.time()})

    async def query_by_key(self, key: str):
        return [r for r in self._records if r['key'] == key]

    async def recent(self, k=5):
        return self._records[-k:]
