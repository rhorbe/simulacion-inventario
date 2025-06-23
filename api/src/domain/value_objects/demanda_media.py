from dataclasses import dataclass
from api.src.domain.value_objects.cantidad import Cantidad
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class DemandaMedia(Cantidad):
    """
    Value Object que representa la demanda media en el dominio.
    Hereda de Cantidad y encapsula la lógica para obtener el valor por defecto.
    """
    
    @classmethod
    def _get_value_or_default(cls, value: Optional[int]) -> int:
        """
        Obtiene el valor proporcionado o el valor por defecto de la configuración.
        
        Args:
            value: Valor proporcionado (puede ser None)
            
        Returns:
            El valor proporcionado o el valor por defecto
            
        Raises:
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        if value is not None:
            return value
        
        if cls._default_config is None:
            raise ValueError("No se proporcionó valor para demanda_media y no hay configuración por defecto")
        
        simulacion = cls._default_config.get_simulacion()
        if 'demanda_media' in simulacion:
            return simulacion['demanda_media']
        
        raise ValueError("No se proporcionó valor para demanda_media y no hay configuración por defecto")
    
    @classmethod
    def from_int(cls, valor: Optional[int] = None) -> 'DemandaMedia':
        """
        Naming constructor que valida y crea una DemandaMedia.
        
        Args:
            valor: El valor de la demanda media (puede ser None para usar valor por defecto)
            
        Returns:
            DemandaMedia: Una instancia válida de DemandaMedia
            
        Raises:
            DomainError: Si la cantidad es negativa
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        actual_valor = cls._get_value_or_default(valor)
        return cls(actual_valor) 