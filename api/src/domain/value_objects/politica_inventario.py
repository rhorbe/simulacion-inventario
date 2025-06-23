from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError
from api.src.domain.value_objects.cantidad import Cantidad
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class PoliticaInventario(BaseValueObject):
    """
    Value Object que representa una política de inventario (r, Q).
    Encapsula el punto de reorden (r) y la cantidad de pedido (Q).
    Ambos valores deben ser no negativos.
    """
    punto_reorden: Cantidad
    cantidad_pedido: Cantidad
    
    @classmethod
    def _get_value_or_default(cls, value: Optional[int]) -> int:
        """
        Este método no se usa directamente en PoliticaInventario.
        Se implementa para cumplir con la interfaz abstracta.
        """
        raise NotImplementedError("Este método no se usa en PoliticaInventario")
    
    @classmethod
    def from_valores(cls, punto_reorden: Optional[int] = None, cantidad_pedido: Optional[int] = None) -> 'PoliticaInventario':
        """
        Naming constructor que valida y crea una PoliticaInventario.
        
        Args:
            punto_reorden: El punto de reorden (r) (puede ser None para usar valor por defecto)
            cantidad_pedido: La cantidad de pedido (Q) (puede ser None para usar valor por defecto)
            
        Returns:
            PoliticaInventario: Una instancia válida de PoliticaInventario
            
        Raises:
            DomainError: Si los valores son inválidos
            ValueError: Si algún valor es None y no hay configuración por defecto
        """
        # Obtener valores o usar valores por defecto
        if punto_reorden is not None:
            actual_punto_reorden = punto_reorden
        elif cls._default_config is not None:
            politicas = cls._default_config.get_politicas_abastecimiento()
            if politicas and 'punto_reorden' in politicas[0]:
                actual_punto_reorden = politicas[0]['punto_reorden']
            else:
                raise ValueError("No se proporcionó valor para punto_reorden y no hay configuración por defecto")
        else:
            raise ValueError("No se proporcionó valor para punto_reorden y no hay configuración por defecto")
        
        if cantidad_pedido is not None:
            actual_cantidad_pedido = cantidad_pedido
        elif cls._default_config is not None:
            politicas = cls._default_config.get_politicas_abastecimiento()
            if politicas and 'cantidad_pedido' in politicas[0]:
                actual_cantidad_pedido = politicas[0]['cantidad_pedido']
            else:
                raise ValueError("No se proporcionó valor para cantidad_pedido y no hay configuración por defecto")
        else:
            raise ValueError("No se proporcionó valor para cantidad_pedido y no hay configuración por defecto")
        
        punto_reorden_vo = Cantidad.from_int(actual_punto_reorden)
        cantidad_pedido_vo = Cantidad.from_int(actual_cantidad_pedido)
        
        return cls(punto_reorden_vo, cantidad_pedido_vo)
    
    def get_punto_reorden(self) -> int:
        """Obtiene el punto de reorden."""
        return int(self.punto_reorden)
    
    def get_cantidad_pedido(self) -> int:
        """Obtiene la cantidad de pedido."""
        return int(self.cantidad_pedido)
    
    def __str__(self) -> str:
        return f"Política (r={self.punto_reorden}, Q={self.cantidad_pedido})" 