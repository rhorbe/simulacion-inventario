from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class CostoPedido(BaseValueObject):
    """
    Value Object que representa los costos de pedido en el dominio.
    Encapsula el costo para pedidos pequeños y grandes.
    El costo de pedido pequeño debe ser mayor al costo de pedido grande.
    Ambos costos deben ser no negativos.
    """
    costo_pedido_pequeno: float
    costo_pedido_grande: float
    
    @classmethod
    def _get_value_or_default(cls, value: Optional[float]) -> float:
        """
        Este método no se usa directamente en CostoPedido.
        Se implementa para cumplir con la interfaz abstracta.
        """
        raise NotImplementedError("Este método no se usa en CostoPedido")
    
    @classmethod
    def from_costos(cls, costo_pedido_pequeno: Optional[float] = None, costo_pedido_grande: Optional[float] = None) -> 'CostoPedido':
        """
        Naming constructor que valida y crea un CostoPedido.
        
        Args:
            costo_pedido_pequeno: El costo por unidad para pedidos pequeños (puede ser None para usar valor por defecto)
            costo_pedido_grande: El costo por unidad para pedidos grandes (puede ser None para usar valor por defecto)
            
        Returns:
            CostoPedido: Una instancia válida de CostoPedido
            
        Raises:
            DomainError: Si los costos son inválidos
            ValueError: Si algún valor es None y no hay configuración por defecto
        """
        # Obtener valores o usar valores por defecto
        if costo_pedido_pequeno is not None:
            actual_costo_pequeno = costo_pedido_pequeno
        elif cls._default_config is not None:
            costos = cls._default_config.get_costos()
            if 'pedido_pequeno' in costos:
                actual_costo_pequeno = costos['pedido_pequeno']
            else:
                raise ValueError("No se proporcionó valor para costo_pedido_pequeno y no hay configuración por defecto")
        else:
            raise ValueError("No se proporcionó valor para costo_pedido_pequeno y no hay configuración por defecto")
        
        if costo_pedido_grande is not None:
            actual_costo_grande = costo_pedido_grande
        elif cls._default_config is not None:
            costos = cls._default_config.get_costos()
            if 'pedido_grande' in costos:
                actual_costo_grande = costos['pedido_grande']
            else:
                raise ValueError("No se proporcionó valor para costo_pedido_grande y no hay configuración por defecto")
        else:
            raise ValueError("No se proporcionó valor para costo_pedido_grande y no hay configuración por defecto")
        
        if actual_costo_pequeno < 0:
            raise DomainError("El costo de pedido pequeño no puede ser negativo")
        
        if actual_costo_grande < 0:
            raise DomainError("El costo de pedido grande no puede ser negativo")
        
        if actual_costo_pequeno <= actual_costo_grande:
            raise DomainError("El costo de pedido pequeño debe ser mayor al costo de pedido grande")
        
        return cls(actual_costo_pequeno, actual_costo_grande)
    
    def get_costo_pedido_pequeno(self) -> float:
        """Obtiene el costo de pedido pequeño."""
        return self.costo_pedido_pequeno
    
    def get_costo_pedido_grande(self) -> float:
        """Obtiene el costo de pedido grande."""
        return self.costo_pedido_grande
    
    def calcular_costo_unitario(self, cantidad: int) -> float:
        """
        Calcula el costo unitario según la cantidad del pedido.
        
        Args:
            cantidad: La cantidad del pedido
            
        Returns:
            float: El costo unitario correspondiente
        """
        return self.costo_pedido_pequeno if cantidad < 300 else self.costo_pedido_grande
    
    def __str__(self) -> str:
        return f"Costos de pedido: pequeño=${self.costo_pedido_pequeno:.2f}, grande=${self.costo_pedido_grande:.2f}" 