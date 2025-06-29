from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

C = TypeVar('C')

class CommandHandler(ABC, Generic[C]):
    """Interfaz para handlers de comandos"""
    @abstractmethod
    def handle(self, command: C) -> Any:
        pass 