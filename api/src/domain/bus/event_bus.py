from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any
from ..models.evento import Evento
from ..models.simulation_context import SimulationContext
from .bus import Bus

T = TypeVar('T')

class EventHandler(ABC, Generic[T]):
    """Interfaz para handlers de eventos"""
    
    @abstractmethod
    def can_handle(self, evento: Evento) -> bool:
        """Determina si este handler puede manejar el evento"""
        pass
    
    @abstractmethod
    def handle(self, event: T, context: Any = None) -> Any:
        """Maneja el evento con el contexto dado"""
        pass

class EventBus(Bus):
    """Interfaz para el bus de eventos con soporte para middlewares"""
    
    @abstractmethod
    def register_handler(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """Registra un handler para un tipo de evento específico"""
        pass
    
    @abstractmethod
    async def dispatch(self, event: T, context: Any = None) -> None:
        """Despacha un evento a través de la cadena de middlewares"""
        pass 