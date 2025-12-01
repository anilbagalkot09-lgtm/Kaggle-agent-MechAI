import json, time
from prometheus_client import Counter, Gauge

LLM_CALLS = Counter('llm_calls_total', 'Total LLM calls')
LLM_FAILS = Counter('llm_failures_total', 'LLM failures')

def log(agent_id: str, level: str, message: str, extra: dict = None):
    payload = {'ts': time.time(), 'agent': agent_id, 'level': level, 'message': message}
    if extra:
        payload['extra'] = extra
    print(json.dumps(payload))
