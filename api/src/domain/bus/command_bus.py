from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any
from .bus import Bus

T = TypeVar('T')

class CommandHandler(ABC, Generic[T]):
    """Interfaz para handlers de comandos"""
    
    @abstractmethod
    def handle(self, command: T) -> Any:
        """Maneja el comando y retorna el resultado"""
        pass

class CommandBus(Bus):
    """Interfaz para el bus de comandos con soporte para middlewares"""
    
    @abstractmethod
    def register_handler(self, command_type: Type[T], handler: CommandHandler[T]) -> None:
        """Registra un handler para un tipo de comando específico"""
        pass
    
    @abstractmethod
    async def execute(self, command: T) -> Any:
        """Ejecuta un comando a través de la cadena de middlewares"""
        pass 