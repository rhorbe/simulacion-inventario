from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional, Any
from api.src.domain.repository.config import Config

T = TypeVar('T', bound='BaseValueObject')

class BaseValueObject(ABC):
    """
    Clase base para todos los Value Objects.
    Proporciona funcionalidad para usar valores por defecto desde la configuración.
    """
    
    _default_config: Optional[Config] = None
    
    @classmethod
    def with_config(cls: Type[T], config: Config) -> Type[T]:
        """
        Configura los valores por defecto para este tipo de Value Object.
        
        Args:
            config: Configuración que contiene los valores por defecto
            
        Returns:
            La clase con la configuración establecida
        """
        cls._default_config = config
        return cls
    
    @classmethod
    def get_default_config(cls) -> Optional[Config]:
        """
        Obtiene la configuración por defecto establecida.
        
        Returns:
            Configuración por defecto o None si no está establecida
        """
        return cls._default_config
    
    @classmethod
    def clear_default_config(cls) -> None:
        """
        Limpia la configuración por defecto establecida.
        """
        cls._default_config = None
    
    @classmethod
    @abstractmethod
    def _get_value_or_default(cls, value: Optional[Any]) -> Any:
        """
        Obtiene el valor proporcionado o el valor por defecto de la configuración.
        Cada clase concreta implementa su propia lógica para obtener el valor por defecto.
        
        Args:
            value: Valor proporcionado (puede ser None)
            
        Returns:
            El valor proporcionado o el valor por defecto
            
        Raises:
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        pass 