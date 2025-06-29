from abc import ABC, abstractmethod
from typing import Type, Any
from ..models.evento import Evento
from ..models.simulation_context import SimulationContext


class EventBus(ABC):
    """Interfaz para el bus de eventos"""
    
    @abstractmethod
    def register_handler(self, event_type: Type[Evento], handler: Any) -> None:
        """
        Registra un handler para un tipo de evento específico
        
        Args:
            event_type: Tipo de evento
            handler: Handler que procesará el evento
        """
        pass
    
    @abstractmethod
    def dispatch(self, evento: Evento, context: SimulationContext) -> None:
        """
        Ejecuta el handler apropiado para el evento
        
        Args:
            evento: Evento a procesar
            context: Contexto de simulación
            
        Raises:
            ValueError: Si no hay handler registrado para el tipo de evento
        """
        pass 