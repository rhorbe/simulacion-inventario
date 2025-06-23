from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class Cantidad(BaseValueObject):
    """
    Value Object que representa una cantidad en el dominio.
    Una cantidad debe ser un entero no negativo.
    """
    valor: int
    
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
            raise ValueError("No se proporcionó valor para cantidad y no hay configuración por defecto")
        
        # Como Cantidad es una clase base, no tiene una clave específica
        # Las clases que heredan de Cantidad deben implementar su propia lógica
        raise ValueError("No se proporcionó valor para cantidad y no hay configuración por defecto")
    
    @classmethod
    def from_int(cls, valor: Optional[int] = None) -> 'Cantidad':
        """
        Naming constructor que valida y crea una Cantidad.
        
        Args:
            valor: El valor de la cantidad (puede ser None para usar valor por defecto)
            
        Returns:
            Cantidad: Una instancia válida de Cantidad
            
        Raises:
            DomainError: Si la cantidad es negativa
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        # Obtener valor o usar valor por defecto
        actual_valor = cls._get_value_or_default(valor)
        
        if actual_valor < 0:
            raise DomainError("La cantidad no puede ser negativa")
        
        return cls(actual_valor)
    
    def __int__(self) -> int:
        """Convierte el ValueObject a int."""
        return self.valor
    
    def __str__(self) -> str:
        return str(self.valor) 