from api.src.domain.bus.event_bus import EventBus
from api.src.infra.bus.in_memory_event_bus import InMemoryEventBus

def get_event_bus() -> EventBus:
    """Proporciona una instancia vacía del bus de eventos"""
    return InMemoryEventBus() 