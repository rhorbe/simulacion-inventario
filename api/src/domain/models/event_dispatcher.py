from typing import List
from .evento import Evento
from .event_handler import EventHandler
from .simulation_context import SimulationContext

class EventDispatcher:
    """Dispatcher que maneja la ejecución de handlers de eventos"""
    
    def __init__(self, handlers: List[EventHandler]):
        self.handlers = handlers
    
    def dispatch(self, evento: Evento, context: SimulationContext) -> None:
        """Ejecuta el handler apropiado para el evento"""
        for handler in self.handlers:
            if handler.can_handle(evento):
                handler.handle(evento, context)
                return
        
        raise ValueError(f"No se encontró handler para el evento: {type(evento).__name__}") 