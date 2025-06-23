from dataclasses import dataclass
from api.src.domain.value_objects.precio import Precio
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class PrecioVenta(Precio):
    """
    Value Object que representa el precio de venta en el dominio.
    Hereda de Precio y encapsula la lógica para obtener el valor por defecto.
    """
    
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
            raise ValueError("No se proporcionó valor para precio_venta y no hay configuración por defecto")
        
        precios = cls._default_config.get_precios()
        if 'venta' in precios:
            return precios['venta']
        
        raise ValueError("No se proporcionó valor para precio_venta y no hay configuración por defecto")
    
    @classmethod
    def from_float(cls, valor: Optional[float] = None) -> 'PrecioVenta':
        """
        Naming constructor que valida y crea un PrecioVenta.
        
        Args:
            valor: El valor del precio de venta (puede ser None para usar valor por defecto)
            
        Returns:
            PrecioVenta: Una instancia válida de PrecioVenta
            
        Raises:
            DomainError: Si el precio es negativo
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        actual_valor = cls._get_value_or_default(valor)
        if actual_valor < 0:
            from api.src.domain.exceptions.domain_error import DomainError
            raise DomainError("El precio no puede ser negativo")
        return cls(actual_valor) 