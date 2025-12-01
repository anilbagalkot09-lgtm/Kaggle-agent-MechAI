import math
from ..core.a2a import A2AMessage
from ..core.observability import log

def avg_daily(forecast_payload):
    arr = forecast_payload.get('forecast', [])
    return sum(arr)/len(arr) if arr else 0

class ReorderAgent:
    def __init__(self, router, inventory_tool):
        self.id = 'ReorderAgent'
        self.router = router
        self.inventory = inventory_tool
        router.register(self.id, self.on_message)

    async def on_message(self, msg: A2AMessage):
        if msg.type != 'ForecastReady':
            return
        sku = msg.payload.get('sku')
        forecast = msg.payload.get('forecast', {})
        sku_rec = await self.inventory.read_sku(sku) or {'qty':0, 'lead_time_days':7, 'reorder_point':10}
        ad = avg_daily(forecast)
        reorder_point = math.ceil((sku_rec.get('lead_time_days',7) * ad) + 2)
        order_qty = max(reorder_point - sku_rec.get('qty',0), 0)
        log(self.id, 'info', f'Computed reorder for {sku}: rp={reorder_point} qty={order_qty}')
        await self.router.send(A2AMessage('ReorderDecision', msg.correlation_id, self.id, 'OrderAgent', {'sku': sku, 'reorder_point': reorder_point, 'order_qty': order_qty}))
