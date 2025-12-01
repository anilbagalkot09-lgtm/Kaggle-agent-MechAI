import asyncio
from msme_agent.core.a2a import A2AMessage, A2ARouter
from msme_agent.core.session_service import InMemorySessionService
from msme_agent.tools.supplier_openapi_tool import SupplierOpenAPITool
from msme_agent.agents.order_agent import OrderAgent

class MockSupplier(SupplierOpenAPITool):
    def __init__(self):
        pass
    def place_order(self, supplier_id, payload):
        return {'order_id': 'mock-123', 'status': 'placed'}

def test_order_place():
    router = A2ARouter()
    session = InMemorySessionService()
    supplier = MockSupplier()
    OrderAgent(router, supplier, session)
    async def send():
        await router.send(A2AMessage('ReorderDecision', 'c2', 'test', to='OrderAgent', payload={'sku':'S1','order_qty':10}))
    import asyncio; asyncio.run(send())
    assert session.get('c2')['status'] == 'placed'
