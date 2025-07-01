from abc import ABC, abstractmethod
from typing import List
from .middleware import Middleware

class Bus(ABC):
    """Interfaz base para todos los buses con soporte para middlewares"""
    
    @abstractmethod
    def add_middleware(self, middleware: Middleware) -> None:
        """Agrega un middleware al bus"""
        pass
    
    @abstractmethod
    def get_middlewares(self) -> List[Middleware]:
        """Retorna la lista de middlewares configurados"""
        pass 