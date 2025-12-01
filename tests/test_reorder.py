import asyncio
from msme_agent.core.a2a import A2AMessage, A2ARouter
from msme_agent.tools.inventory_db_tool import InventoryDBTool
from msme_agent.agents.reorder_agent import ReorderAgent

def test_reorder_runs():
    router = A2ARouter()
    inventory = InventoryDBTool()
    async def setup():
        await inventory.upsert_sku('S1', {'qty':2, 'reorder_point':5, 'lead_time_days':7})
        ReorderAgent(router, inventory)
        await router.send(A2AMessage('ForecastReady', 'c1', 'test', to='ReorderAgent', payload={'sku':'S1','forecast':{'forecast':[2,3,4]}}))
    import asyncio; asyncio.run(setup())
    assert True
