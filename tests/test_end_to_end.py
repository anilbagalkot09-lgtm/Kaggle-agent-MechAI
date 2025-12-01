import asyncio
from msme_adk.core.a2a import A2AMessage, A2ARouter
from msme_adk.core.memory_bank import MemoryBank
from msme_adk.agents.forecast_agent_gemini import ForecastAgent

def test_smoke():
    router = A2ARouter()
    memory = MemoryBank()
    ForecastAgent(router, memory)
    async def send():
        await router.send(A2AMessage('RunForecast', 't1', 'test', to='ForecastAgent', payload={'sku':'S1','horizon_days':7,'sales_history':[1,2,3,4,5,6,7]}))
    asyncio.run(send())
    assert True
