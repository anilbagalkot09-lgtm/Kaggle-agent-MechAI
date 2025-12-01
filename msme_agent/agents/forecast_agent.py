import asyncio
from ..core.a2a import A2AMessage
from ..core.observability import log

async def mock_llm(prompt: str):
    # predictable mock LLM for demo/testing
    return {'forecast': [1,2,3,4,5], 'note': f'mock forecast for prompt len {len(prompt)}'}

class ForecastAgent:
    def __init__(self, router, memory_bank):
        self.id = 'ForecastAgent'
        self.router = router
        self.memory = memory_bank
        router.register(self.id, self.on_message)

    async def on_message(self, msg: A2AMessage):
        if msg.type != 'RunForecast':
            return
        sku = msg.payload.get('sku')
        horizon = msg.payload.get('horizon_days', 14)
        log(self.id, 'info', f'Starting forecast for {sku} horizon {horizon}')
        # Context compaction example: if sales history is long, summarize (omitted)
        forecast = await mock_llm(f'Forecast for {sku} horizon {horizon}')
        # send ForecastReady
        await self.router.send(A2AMessage('ForecastReady', msg.correlation_id, self.id, 'ReorderAgent', {'sku': sku, 'forecast': forecast}))
