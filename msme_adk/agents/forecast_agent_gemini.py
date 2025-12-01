"""Gemini-enabled ForecastAgent with context compaction, hybrid ML+LLM, guardrails, and memory writes."""
import asyncio, json, time
from typing import List, Dict, Any, Optional
import pydantic as _pydantic
from pydantic import BaseModel, ValidationError, Field

# compatibility: support both pydantic v1 (conlist) and v2 (Field with min_items)
_pyd_ver = tuple(int(x) for x in _pydantic.__version__.split('+')[0].split('.'))
if _pyd_ver[0] < 2:
    from pydantic import conlist
    ForecastList = conlist(float, min_items=1)
    _forecast_field_default = ...
else:
    ForecastList = List[float]
    _forecast_field_default = Field(..., min_items=1)

try:
    from ..core.a2a import A2AMessage
    from ..core.llm_client import LLMClient
    from ..core.observability import log, LLM_CALLS, LLM_FAILS
    from ..core.memory_bank import MemoryBank
except (ImportError, ValueError):
    from msme_adk.core.a2a import A2AMessage
    from msme_adk.core.llm_client import LLMClient
    from msme_adk.core.observability import log, LLM_CALLS, LLM_FAILS
    from msme_adk.core.memory_bank import MemoryBank


class ForecastSchema(BaseModel):
    forecast: ForecastList = _forecast_field_default
    analysis: str
    seasonality: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

FORECAST_PROMPT = """You are a supply-chain forecasting assistant for a small retail MSME.
Inputs:
- SKU: {sku}
- HorizonDays: {horizon}
- RecentSales (most recent last): {recent_sales}
- ContextSummary: {context_summary}

Produce ONLY valid JSON with keys: forecast, analysis, seasonality, metadata.
"""

COMPACTION_PROMPT = """Summarize daily sales into a short summary and weekly aggregates (7-day means).
Return JSON: {"summary": "...", "weekly_aggregates": [...]}
"""

def simple_exp_smoothing(history: List[float], horizon: int, alpha: float = 0.25):
    if not history:
        return [0.0] * horizon
    s = history[0]
    for x in history:
        s = alpha * x + (1 - alpha) * s
    return [round(s,2) for _ in range(horizon)]

async def with_retries(fn, *args, retries=3, base_delay=0.5, **kwargs):
    attempt = 0
    while attempt < retries:
        try:
            return fn(*args, **kwargs) if not asyncio.iscoroutinefunction(fn) else await fn(*args, **kwargs)
        except Exception as e:
            attempt += 1
            delay = base_delay * (2 ** (attempt-1))
            log('ForecastAgent', 'error', f'LLM attempt {attempt} failed: {e}. Backoff {delay}s')
            await asyncio.sleep(delay)
    raise RuntimeError('Max retries exceeded')

class ForecastAgent:
    def __init__(self, router, memory: MemoryBank, use_llm_compaction: bool = True):
        self.id = 'ForecastAgentGemini'
        self.router = router
        self.memory = memory
        self.use_llm_compaction = use_llm_compaction
        try:
            self.llm = LLMClient()
        except Exception as e:
            log(self.id, 'error', f'LLMClient init error: {e}')
            self.llm = None
        router.register(self.id, self.on_message)

    async def compact_context(self, sku: str, sales_history: List[float]):
        if not sales_history:
            return {'summary':'No sales history', 'weekly_aggregates': []}
        if len(sales_history) < 60 or not self.use_llm_compaction or not self.llm:
            weekly = []
            window = 7
            for i in range(max(0, len(sales_history)-28), len(sales_history), window):
                chunk = sales_history[i:i+window]
                if chunk:
                    weekly.append(round(sum(chunk)/len(chunk),2))
            summary = f'Weekly aggregates (last {len(weekly)}): {weekly[-4:]}'
            return {'summary': summary, 'weekly_aggregates': weekly}
        # call LLM for compaction
        prompt = COMPACTION_PROMPT.replace('{sales_list}', json.dumps(sales_history[-180:]))
        try:
            LLM_CALLS.inc()
            raw = await with_retries(self.llm.complete, prompt, retries=2)
            parsed = json.loads(raw)
            return {'summary': parsed.get('summary',''), 'weekly_aggregates': parsed.get('weekly_aggregates',[])}
        except Exception as e:
            LLM_FAILS.inc()
            log(self.id, 'error', f'Compaction failed: {e}, falling back deterministic.')
            return await self.compact_context(sku, sales_history[:60])

    async def call_llm_forecast(self, sku: str, horizon: int, recent_sales: List[float], context_summary: str):
        prompt = FORECAST_PROMPT.format(sku=sku, horizon=horizon, recent_sales=json.dumps(recent_sales), context_summary=context_summary)
        LLM_CALLS.inc()
        raw = await with_retries(self.llm.complete, prompt, retries=3)
        # extract JSON object
        start = raw.find('{')
        end = raw.rfind('}') + 1
        json_text = raw[start:end] if start != -1 and end != -1 else raw
        parsed = json.loads(json_text)
        return ForecastSchema(**parsed)

    async def on_message(self, msg: A2AMessage):
        if msg.type != 'RunForecast':
            return
        sku = msg.payload.get('sku')
        horizon = int(msg.payload.get('horizon_days', 14))
        sales_history = msg.payload.get('sales_history', [])
        log(self.id, 'info', f'Received RunForecast for {sku} horizon {horizon}, history len {len(sales_history)}')
        compacted = await self.compact_context(sku, sales_history)
        await self.memory.add(f'sales_summary:{sku}', compacted)
        ml_forecast = simple_exp_smoothing(sales_history[-60:], horizon)
        llm_schema = None
        if self.llm:
            try:
                llm_schema = await self.call_llm_forecast(sku, horizon, sales_history[-30:], compacted.get('summary',''))
                log(self.id, 'info', f'LLM forecast OK for {sku}')
            except Exception as e:
                log(self.id, 'error', f'LLM forecast failed for {sku}: {e}')
        if llm_schema:
            llm_conf = llm_schema.metadata.get('confidence') if llm_schema.metadata else 0.6
            w_llm = max(0.05, min(0.95, float(llm_conf)))
            w_ml = 1.0 - w_llm
            llm_list = list(llm_schema.forecast)[:horizon] + [llm_schema.forecast[-1]]*(max(0, horizon - len(llm_schema.forecast)))
            final = [round(w_llm*float(llm_list[i]) + w_ml*float(ml_forecast[i]),2) for i in range(horizon)]
            chosen = 'hybrid'
            analysis = llm_schema.analysis
        else:
            final = ml_forecast
            chosen = 'ml'
            analysis = 'ML fallback (exp smoothing)'
        payload = {'forecast': final, 'analysis': analysis, 'seasonality': llm_schema.seasonality if llm_schema else None, 'metadata': {'model': chosen, 'timestamp': time.time()}}
        await self.memory.add(f'forecast:{sku}:{int(time.time())}', payload)
        await self.router.send(A2AMessage('ForecastReady', msg.correlation_id, self.id, 'ReorderAgent', {'sku': sku, 'forecast': payload}))
        log(self.id, 'info', f'Emitted ForecastReady for {sku} using {chosen}')
