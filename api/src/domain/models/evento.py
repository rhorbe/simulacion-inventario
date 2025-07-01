from abc import ABC, abstractmethod
from dataclasses import dataclass
from .message import BaseMessage


class Evento(BaseMessage):
    """
    Clase base abstracta para todos los eventos de la simulación.
    Define la interfaz común que deben implementar todos los eventos.
    """
    
    @abstractmethod
    def get_dia(self) -> int:
        """Retorna el día en que ocurre el evento."""
        pass
    
    @abstractmethod
    def get_tipo_evento(self) -> str:
        """Retorna el tipo específico del evento (demanda, llegada_pedido, etc.)"""
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
    dia: int
    cantidad: int
    
    def get_dia(self) -> int:
        return self.dia
    
    def get_tipo_evento(self) -> str:
        return "demanda"
    
    def __str__(self) -> str:
        return f"EventoDemanda(dia={self.dia}, cantidad={self.cantidad})"

@dataclass
class EventoLlegadaPedido(Evento):
    """
    Evento que representa la llegada de un pedido.
    """
    dia: int
    cantidad: int
    
    def get_dia(self) -> int:
        return self.dia
    
    def get_tipo_evento(self) -> str:
        return "llegada_pedido"

    def __str__(self) -> str:
        return f"EventoLlegadaPedido(dia={self.dia}, cantidad={self.cantidad})"