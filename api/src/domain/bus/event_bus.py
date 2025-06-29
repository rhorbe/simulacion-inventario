from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any, List
from ..models.evento import Evento
from ..models.simulation_context import SimulationContext
from .middleware import Middleware

T = TypeVar('T', bound=Evento)

class EventHandler(ABC, Generic[T]):
    """Interfaz para handlers de eventos"""
    
    @abstractmethod
    def can_handle(self, evento: Evento) -> bool:
        """Determina si este handler puede manejar el evento"""
        pass
    
    @abstractmethod
    def handle(self, evento: T, context: SimulationContext) -> None:
        """Maneja el evento con el contexto dado"""
        pass

class EventBus(ABC):
    """Interfaz para el bus de eventos con soporte para middlewares"""
    
    @abstractmethod
    def register_handler(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """Registra un handler para un tipo de evento específico"""
        pass
    
    @abstractmethod
    def dispatch(self, evento: Evento, context: SimulationContext) -> None:
        """Despacha un evento a través de la cadena de middlewares"""
        pass
    
    @abstractmethod
    def add_middleware(self, middleware: Middleware) -> None:
        """Agrega un middleware al bus"""
        pass
    
    @abstractmethod
    def get_middlewares(self) -> List[Middleware]:
        """Retorna la lista de middlewares configurados"""
        pass 