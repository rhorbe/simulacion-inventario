from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class CostoFaltante(BaseValueObject):
    """
    Value Object que representa el costo de faltante en el dominio.
    Un costo de faltante no puede ser negativo.
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
            raise ValueError("No se proporcionó valor para costo_faltante y no hay configuración por defecto")
        
        costos = cls._default_config.get_costos()
        if 'faltante' in costos:
            return costos['faltante']
        
        raise ValueError("No se proporcionó valor para costo_faltante y no hay configuración por defecto")
    
    @classmethod
    def from_float(cls, valor: Optional[float] = None) -> 'CostoFaltante':
        """
        Naming constructor que valida y crea un CostoFaltante.
        
        Args:
            valor: El valor del costo de faltante (puede ser None para usar valor por defecto)
            
        Returns:
            CostoFaltante: Una instancia válida de CostoFaltante
            
        Raises:
            DomainError: Si el costo es negativo
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        # Obtener valor o usar valor por defecto
        actual_valor = cls._get_value_or_default(valor)
        
        if actual_valor < 0:
            raise DomainError("El costo de faltante no puede ser negativo")
        
        return cls(actual_valor)
    
    def __float__(self) -> float:
        """Convierte el ValueObject a float."""
        return float(self.valor)
    
    def __str__(self) -> str:
        return f"${self.valor:.2f}" 