import asyncio
from msme_adk.core.a2a import A2AMessage, A2ARouter
from msme_adk.core.session_service import InMemorySessionService
from msme_adk.core.memory_bank import MemoryBank
from msme_adk.tools.inventory_mcp import InventoryMCP
from msme_adk.tools.supplier_openapi_tool import SupplierOpenAPITool
from msme_adk.agents.forecast_agent_gemini import ForecastAgent
from msme_adk.agents.reorder_agent import ReorderAgent
from msme_adk.agents.order_agent import OrderAgent
from msme_adk.agents.ops_agent import OpsAgent
from msme_adk.core.observability import log

async def run_demo():
    router = A2ARouter()
    session = InMemorySessionService()
    memory = MemoryBank()
    inventory = InventoryMCP()
    supplier = SupplierOpenAPITool()
    # seed inventory
    inventory.upsert('SAMPLE-001', {'qty': 5, 'reorder_point': 10, 'lead_time_days': 7})
    # create agents
    ForecastAgent(router, memory)
    ReorderAgent(router, inventory)
    OrderAgent(router, supplier, session)
    OpsAgent(router, inventory)
    # trigger a workflow
    corr = 'wf-gemini-1'
    await router.send(A2AMessage('RunForecast', corr, 'system', to='ForecastAgent', payload={'sku':'SAMPLE-001','horizon_days':14,'sales_history':[2,3,4,5,6,3,4,5,6,7,8,9,5,4,3,6,7,8,9,10,9,8,7,6,5,4]}))
    await asyncio.sleep(2)

if __name__ == '__main__':
    asyncio.run(run_demo())
