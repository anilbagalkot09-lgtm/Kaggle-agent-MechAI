from typing import Callable, Dict, Any
import json

class A2AMessage:
    def __init__(self, type: str, correlation_id: str, from_: str, to: str = None, payload: Any = None):
        self.type = type
        self.correlation_id = correlation_id
        self.from_ = from_
        self.to = to
        self.payload = payload

    def to_dict(self):
        return {
            'type': self.type,
            'correlation_id': self.correlation_id,
            'from': self.from_,
            'to': self.to,
            'payload': self.payload
        }

class A2ARouter:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}

    def register(self, agent_id: str, handler: Callable):
        self.handlers[agent_id] = handler

    async def send(self, msg: A2AMessage):
        # naive routing: direct if 'to' set, else broadcast to all except sender
        if msg.to:
            h = self.handlers.get(msg.to)
            if h:
                await h(msg)
        else:
            for aid, h in self.handlers.items():
                if aid != msg.from_:
                    await h(msg)
