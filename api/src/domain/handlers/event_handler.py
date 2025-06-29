from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from api.src.domain.models.evento import Evento
from api.src.domain.models.simulation_context import SimulationContext

E = TypeVar('E', bound=Evento)

class EventHandler(ABC, Generic[E]):
    """Interfaz para handlers de eventos"""
    @abstractmethod
    def can_handle(self, evento: Evento) -> bool:
        pass

    @abstractmethod
    def handle(self, evento: E, context: SimulationContext) -> None:
        pass 