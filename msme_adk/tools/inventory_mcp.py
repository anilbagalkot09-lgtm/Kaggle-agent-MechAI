class InventoryMCP:
    def __init__(self):
        self._store = {}

    def read_sku(self, sku: str):
        return self._store.get(sku)

    def upsert(self, sku: str, record: dict):
        existing = self._store.get(sku, {})
        existing.update(record)
        self._store[sku] = existing
        return self._store[sku]

    def list_low(self):
        return [{'sku': k, **v} for k, v in self._store.items() if v.get('qty',0) <= v.get('reorder_point',0)]
