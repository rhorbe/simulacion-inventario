from dataclasses import dataclass
from api.src.domain.value_objects.cantidad import Cantidad
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class InventarioInicial(Cantidad):
    """
    Value Object que representa el inventario inicial en el dominio.
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
            raise ValueError("No se proporcionó valor para inventario_inicial y no hay configuración por defecto")
        
        simulacion = cls._default_config.get_simulacion()
        if 'inventario_inicial' in simulacion:
            return simulacion['inventario_inicial']
        
        raise ValueError("No se proporcionó valor para inventario_inicial y no hay configuración por defecto")
    
    @classmethod
    def from_int(cls, valor: Optional[int] = None) -> 'InventarioInicial':
        """
        Naming constructor que valida y crea un InventarioInicial.
        
        Args:
            valor: El valor del inventario inicial (puede ser None para usar valor por defecto)
            
        Returns:
            InventarioInicial: Una instancia válida de InventarioInicial
            
        Raises:
            DomainError: Si la cantidad es negativa
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        actual_valor = cls._get_value_or_default(valor)
        return cls(actual_valor) 