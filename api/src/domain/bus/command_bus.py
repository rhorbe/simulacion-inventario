from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any, List
from .middleware import Middleware

T = TypeVar('T')

class CommandHandler(ABC, Generic[T]):
    """Interfaz para handlers de comandos"""
    
    @abstractmethod
    def handle(self, command: T) -> Any:
        """Maneja el comando y retorna el resultado"""
        pass

class CommandBus(ABC):
    """Interfaz para el bus de comandos con soporte para middlewares"""
    
    @abstractmethod
    def register_handler(self, command_type: Type[T], handler: CommandHandler[T]) -> None:
        """Registra un handler para un tipo de comando específico"""
        pass
    
    @abstractmethod
    def execute(self, command: T) -> Any:
        """Ejecuta un comando a través de la cadena de middlewares"""
        pass
    
    @abstractmethod
    def add_middleware(self, middleware: Middleware) -> None:
        """Agrega un middleware al bus"""
        pass
    
    @abstractmethod
    def get_middlewares(self) -> List[Middleware]:
        """Retorna la lista de middlewares configurados"""
        pass 