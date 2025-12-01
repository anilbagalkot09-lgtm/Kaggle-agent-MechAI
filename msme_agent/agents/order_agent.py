from ..core.a2a import A2AMessage
from ..core.observability import log

class OrderAgent:
    def __init__(self, router, supplier_tool, session_service):
        self.id = 'OrderAgent'
        self.router = router
        self.supplier = supplier_tool
        self.session = session_service
        router.register(self.id, self.on_message)

    async def on_message(self, msg: A2AMessage):
        if msg.type == 'ReorderDecision':
            sku = msg.payload.get('sku')
            qty = msg.payload.get('order_qty', 0)
            corr = msg.correlation_id
            log(self.id, 'info', f'Placing order for {sku} qty {qty}')
            resp = self.supplier.place_order('SUPPLIER-1', {'sku': sku, 'qty': qty})
            # persist session for pause/resume
            self.session.create(corr, {'order_id': resp.get('order_id', 'mock'), 'status': 'placed', 'sku': sku, 'qty': qty})
            await self.router.send(A2AMessage('OrderPlaced', corr, self.id, 'OpsAgent', {'order_id': resp.get('order_id', 'mock')}))
        elif msg.type == 'SupplierWebhook':
            corr = msg.correlation_id
            status = msg.payload.get('status')
            log(self.id, 'info', f'Webhook for {corr} status {status}')
            state = self.session.get(corr) or {}
            state['status'] = status
            self.session.update(corr, state)
            await self.router.send(A2AMessage('OrderUpdated', corr, self.id, 'OpsAgent', {'status': status}))
