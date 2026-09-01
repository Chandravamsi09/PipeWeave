"""Event Bus Pub-Sub"""
from typing import Dict, List, Callable, Any, Set
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Event:
    event_type: str
    payload: Dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, Set[Callable]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, event_type: str, handler: Callable) -> None:
        async with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = set()
            self._subscribers[event_type].add(handler)

    async def publish(self, event_type: str, payload: Dict[str, Any]) -> Event:
        event = Event(event_type=event_type, payload=payload)
        async with self._lock:
            handlers = list(self._subscribers.get(event_type, set()))
        for h in handlers:
            try:
                if asyncio.iscoroutinefunction(h):
                    await h(event)
                else:
                    h(event)
            except Exception:
                pass
        return event

event_bus = EventBus()
