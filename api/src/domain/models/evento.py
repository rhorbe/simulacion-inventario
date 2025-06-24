from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

class EventoBase(ABC):
    """
    Clase base abstracta para todos los eventos de la simulación.
    Define la interfaz común que deben implementar todos los eventos.
    """
    
    @abstractmethod
    def get_dia(self) -> int:
        """Retorna el día en que ocurre el evento."""
        pass
    
    @abstractmethod
    def get_tipo(self) -> str:
        """Retorna el tipo del evento."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Representación en string del evento."""
        pass

@dataclass
class EventoDemanda(EventoBase):
    """
    Evento que representa una demanda de productos.
    """
    dia: int
    cantidad: int
    
    def get_dia(self) -> int:
        return self.dia
    
    def get_tipo(self) -> str:
        return "demanda"
    
    def get_cantidad(self) -> int:
        return self.cantidad
    
    def __str__(self) -> str:
        return f"EventoDemanda(dia={self.dia}, cantidad={self.cantidad})"

@dataclass
class EventoLlegadaPedido(EventoBase):
    """
    Evento que representa la llegada de un pedido.
    """
    dia: int
    cantidad: int
    
    def get_dia(self) -> int:
        return self.dia
    
    def get_tipo(self) -> str:
        return "llegada_pedido"
    
    def get_cantidad(self) -> int:
        return self.cantidad
    
    def __str__(self) -> str:
        return f"EventoLlegadaPedido(dia={self.dia}, cantidad={self.cantidad})"

# Clase de compatibilidad para mantener la interfaz existente
@dataclass
class Evento(EventoBase):
    """
    Clase de compatibilidad que mantiene la interfaz original.
    Se recomienda usar las clases específicas EventoDemanda y EventoLlegadaPedido.
    """
    tipo: str
    dia: int
    cantidad: int = 0
    
    def get_dia(self) -> int:
        return self.dia
    
    def get_tipo(self) -> str:
        return self.tipo
    
    def get_cantidad(self) -> int:
        return self.cantidad
    
    def __str__(self) -> str:
        return f"Evento(tipo={self.tipo}, dia={self.dia}, cantidad={self.cantidad})"
    
