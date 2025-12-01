class InventoryDBTool:
    def __init__(self):
        # sku -> {qty, reorder_point, lead_time_days}
        self._inventory = {}

    async def read_sku(self, sku: str):
        return self._inventory.get(sku)

    async def upsert_sku(self, sku: str, record: dict):
        existing = self._inventory.get(sku, {})
        existing.update(record)
        self._inventory[sku] = existing

    async def list_low_stock(self):
        return [{'sku': k, **v} for k, v in self._inventory.items() if v.get('qty',0) <= v.get('reorder_point',0)]
