from ..core.a2a import A2AMessage
from ..core.observability import log

class OpsAgent:
    def __init__(self, router, inventory_tool):
        self.id = 'OpsAgent'
        self.router = router
        self.inventory = inventory_tool
        router.register(self.id, self.on_message)

    async def on_message(self, msg: A2AMessage):
        if msg.type == 'OrderPlaced':
            log(self.id, 'info', f'Order placed: {msg.payload}')
        elif msg.type == 'OrderUpdated':
            log(self.id, 'info', f'Order updated: {msg.payload}')
