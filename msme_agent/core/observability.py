import json, time
from prometheus_client import Counter, Gauge

REQUESTS = Counter('agent_requests_total', 'Total agent requests')
ORDER_SUCCESS = Gauge('agent_order_success_rate', 'Order success rate (0-1)')

def log(agent_id: str, level: str, message: str, extra: dict = None):
    payload = {'ts': time.time(), 'agent': agent_id, 'level': level, 'message': message}
    if extra:
        payload['extra'] = extra
    print(json.dumps(payload))
