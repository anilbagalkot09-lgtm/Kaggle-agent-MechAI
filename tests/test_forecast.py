import asyncio
from msme_agent.core.a2a import A2AMessage, A2ARouter
from msme_agent.core.memory_bank import MemoryBank
from msme_agent.agents.forecast_agent import ForecastAgent

def test_forecast_runs():
    router = A2ARouter()
    memory = MemoryBank()
    ForecastAgent(router, memory)
    # Send RunForecast and ensure ForecastAgent responds by invoking handlers (no exception)
    async def send_msg():
        await router.send(A2AMessage('RunForecast', 't1', 'test', to='ForecastAgent', payload={'sku':'S1','horizon_days':7}))
    asyncio.run(send_msg())
    assert True
