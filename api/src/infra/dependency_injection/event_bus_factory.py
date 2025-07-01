from api.src.domain.bus.event_bus import EventBus
from api.src.infra.bus.in_memory_event_bus import InMemoryEventBus

# Instancia singleton del EventBus
_event_bus_instance = None

def get_event_bus() -> EventBus:
    """Proporciona una instancia singleton del bus de eventos"""
    global _event_bus_instance
    if _event_bus_instance is None:
        _event_bus_instance = InMemoryEventBus()
    return _event_bus_instance 