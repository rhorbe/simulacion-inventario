from api.src.domain.bus.command_bus import CommandBus
from api.src.infra.bus.in_memory_command_bus import InMemoryCommandBus

# Instancia singleton del CommandBus
_command_bus_instance = None

def get_command_bus() -> CommandBus:
    """Proporciona una instancia singleton del bus de comandos"""
    global _command_bus_instance
    if _command_bus_instance is None:
        _command_bus_instance = InMemoryCommandBus()
    return _command_bus_instance 