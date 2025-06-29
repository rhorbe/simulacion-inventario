from abc import ABC, abstractmethod
from typing import TypeVar, Type, Any

T = TypeVar('T')


class CommandBus(ABC):
    """Interfaz para el bus de comandos"""
    
    @abstractmethod
    def register_handler(self, command_type: Type[T], handler: Any) -> None:
        """
        Registra un handler para un tipo de comando específico
        
        Args:
            command_type: Tipo de comando
            handler: Handler que procesará el comando
        """
        pass
    
    @abstractmethod
    def execute(self, command: T) -> Any:
        """
        Ejecuta un comando usando el handler registrado
        
        Args:
            command: Comando a ejecutar
            
        Returns:
            Resultado de la ejecución del comando
            
        Raises:
            ValueError: Si no hay handler registrado para el tipo de comando
        """
        pass 