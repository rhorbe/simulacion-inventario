from api.src.domain.bus.command_bus import CommandBus
from api.src.infra.bus.in_memory_command_bus import InMemoryCommandBus

def get_command_bus() -> CommandBus:
    """Proporciona una instancia vacía del bus de comandos"""
    return InMemoryCommandBus() 