from typing import Callable, Dict, Any
import asyncio

class A2AMessage:
    def __init__(self, type: str, correlation_id: str, from_: str, to: str = None, payload: Any = None):
        self.type = type
        self.correlation_id = correlation_id
        self.from_ = from_
        self.to = to
        self.payload = payload

class A2ARouter:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}

    def register(self, agent_id: str, handler: Callable):
        self.handlers[agent_id] = handler

    async def send(self, msg: A2AMessage):
        # direct routing if 'to' set
        if msg.to and msg.to in self.handlers:
            h = self.handlers[msg.to]
            res = h(msg)
            if asyncio.iscoroutine(res):
                await res
            return
        # broadcast
        for aid, h in self.handlers.items():
            if aid == msg.from_:
                continue
            res = h(msg)
            if asyncio.iscoroutine(res):
                await res
