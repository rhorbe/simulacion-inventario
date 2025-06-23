from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class CostoAlmacenar(BaseValueObject):
    """
    Value Object que representa el costo de almacenamiento en el dominio.
    Un costo de almacenamiento no puede ser negativo.
    """
    valor: float
    
    @classmethod
    def _get_value_or_default(cls, value: Optional[float]) -> float:
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
            raise ValueError("No se proporcionó valor para costo_almacenar y no hay configuración por defecto")
        
        costos = cls._default_config.get_costos()
        if 'almacenar' in costos:
            return costos['almacenar']
        
        raise ValueError("No se proporcionó valor para costo_almacenar y no hay configuración por defecto")
    
    @classmethod
    def from_float(cls, valor: Optional[float] = None) -> 'CostoAlmacenar':
        """
        Naming constructor que valida y crea un CostoAlmacenar.
        
        Args:
            valor: El valor del costo de almacenamiento (puede ser None para usar valor por defecto)
            
        Returns:
            CostoAlmacenar: Una instancia válida de CostoAlmacenar
            
        Raises:
            DomainError: Si el costo es negativo
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        # Obtener valor o usar valor por defecto
        actual_valor = cls._get_value_or_default(valor)
        
        if actual_valor < 0:
            raise DomainError("El costo de almacenamiento no puede ser negativo")
        
        return cls(actual_valor)
    
    def __float__(self) -> float:
        """Convierte el ValueObject a float."""
        return float(self.valor)
    
    def __str__(self) -> str:
        return f"${self.valor:.2f}" 