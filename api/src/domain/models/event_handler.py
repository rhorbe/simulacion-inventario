from typing import Protocol
from .evento import Evento
from .simulation_context import SimulationContext

class EventHandler(Protocol):
    """Protocolo para handlers de eventos"""
    
    def can_handle(self, evento: Evento) -> bool:
        """Determina si este handler puede procesar el evento"""
        ...
    
    def handle(self, evento: Evento, context: SimulationContext) -> None:
        """Procesa el evento usando el contexto de simulación"""
        ... 