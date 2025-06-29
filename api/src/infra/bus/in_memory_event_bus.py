from typing import Dict, Type, Any
from api.src.domain.bus.event_bus import EventBus
from api.src.domain.models.evento import Evento
from api.src.domain.models.simulation_context import SimulationContext


class InMemoryEventBus(EventBus):
    """Implementación en memoria del bus de eventos"""
    
    def __init__(self):
        self._handlers: Dict[Type[Evento], Any] = {}
    
    def register_handler(self, event_type: Type[Evento], handler: Any) -> None:
        """Registra un handler para un tipo de evento específico"""
        self._handlers[event_type] = handler
    
    def dispatch(self, evento: Evento, context: SimulationContext) -> None:
        """
        Ejecuta el handler apropiado para el evento
        
        Args:
            evento: Evento a procesar
            context: Contexto de simulación
            
        Raises:
            ValueError: Si no hay handler registrado para el tipo de evento
        """
        event_type = type(evento)
        if event_type not in self._handlers:
            raise ValueError(f"No se encontró handler para el evento: {event_type.__name__}")
        
        handler = self._handlers[event_type]
        handler.handle(evento, context) 