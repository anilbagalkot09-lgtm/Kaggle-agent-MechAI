import time
class MemoryBank:
    def __init__(self):
        self._records = []

    async def add(self, key, value):
        self._records.append({'key': key, 'value': value, 'ts': time.time()})

    async def query_by_key(self, key):
        return [r for r in self._records if r['key'] == key]
