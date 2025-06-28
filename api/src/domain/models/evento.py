from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Evento(ABC):
    """
    Clase base abstracta para todos los eventos de la simulación.
    Define la interfaz común que deben implementar todos los eventos.
    """
    dia: int
    cantidad: int

    def get_dia(self) -> int:
        """Retorna el día en que ocurre el evento."""
        return self.dia
    
    @abstractmethod
    def get_tipo(self) -> str:
        """Retorna el tipo del evento."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Representación en string del evento."""
        pass

    def get_cantidad(self) -> int:
        return self.cantidad


@dataclass
class EventoDemanda(Evento):
    """
    Evento que representa una demanda de productos.
    """

    def get_tipo(self) -> str:
        return "demanda"
    
    def __str__(self) -> str:
        return f"EventoDemanda(dia={self.dia}, cantidad={self.cantidad})"

@dataclass
class EventoLlegadaPedido(Evento):
    """
    Evento que representa la llegada de un pedido.
    """
    
    def get_tipo(self) -> str:
        return "llegada_pedido"

    def __str__(self) -> str:
        return f"EventoLlegadaPedido(dia={self.dia}, cantidad={self.cantidad})"