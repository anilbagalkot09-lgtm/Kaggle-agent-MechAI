import asyncio
from msme_agent.core.a2a import A2AMessage, A2ARouter
from msme_agent.core.session_service import InMemorySessionService
from msme_agent.core.memory_bank import MemoryBank
from msme_agent.tools.inventory_db_tool import InventoryDBTool
from msme_agent.tools.supplier_openapi_tool import SupplierOpenAPITool
from msme_agent.agents.forecast_agent import ForecastAgent
from msme_agent.agents.reorder_agent import ReorderAgent
from msme_agent.agents.order_agent import OrderAgent
from msme_agent.agents.ops_agent import OpsAgent
from msme_agent.core.observability import log

async def run_demo():
    router = A2ARouter()
    session = InMemorySessionService()
    memory = MemoryBank()
    inventory = InventoryDBTool()
    supplier = SupplierOpenAPITool()  # assumes mock supplier running locally
    # seed inventory
    await inventory.upsert_sku('SAMPLE-001', {'qty': 5, 'reorder_point': 10, 'lead_time_days': 7})

    # create agents
    ForecastAgent(router, memory)
    ReorderAgent(router, inventory)
    OrderAgent(router, supplier, session)
    OpsAgent(router, inventory)

    # start demo workflow
    corr = 'wf-1'
    await router.send(A2AMessage('RunForecast', corr, 'system', to='ForecastAgent', payload={'sku': 'SAMPLE-001', 'horizon_days': 14}))

    # wait a short time for async handlers to run in this demo
    await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(run_demo())
