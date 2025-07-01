from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Dict, Any, Type, TypeVar

T = TypeVar('T', bound='BaseMessage')

class Message(ABC):
    """Interfaz base para todos los mensajes (comandos y eventos)"""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el mensaje a diccionario para serialización"""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Crea una instancia del mensaje desde un diccionario"""
        pass

class BaseMessage(Message):
    """Implementación base que proporciona serialización automática"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialización automática basada en dataclass"""
        result = asdict(self)
        result['_tipo'] = type(self).__name__
        result['_categoria'] = self._get_categoria()
        return result
    
    def _get_categoria(self) -> str:
        """Retorna la categoría del mensaje (comando o evento)"""
        if hasattr(self, 'get_tipo_evento'):
            return "evento"
        else:
            return "comando"
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Deserialización automática basada en dataclass"""
        # Remover metadatos antes de crear la instancia
        clean_data = {k: v for k, v in data.items() 
                     if not k.startswith('_')}
        return cls(**clean_data) 