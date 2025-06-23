from dataclasses import dataclass
from api.src.domain.value_objects.cantidad import Cantidad

@dataclass(frozen=True)
class PoliticaInventario:
    """
    Value Object que representa una política de inventario (r, Q).
    Encapsula el punto de reorden (r) y la cantidad de pedido (Q).
    Ambos valores deben ser no negativos.
    """
    punto_reorden: Cantidad
    cantidad_pedido: Cantidad
    
    @classmethod
    def from_valores(cls, punto_reorden: int, cantidad_pedido: int) -> 'PoliticaInventario':
        """
        Naming constructor que valida y crea una PoliticaInventario.
        
        Args:
            punto_reorden: El punto de reorden (r)
            cantidad_pedido: La cantidad de pedido (Q)
            
        Returns:
            PoliticaInventario: Una instancia válida de PoliticaInventario
            
        Raises:
            DomainError: Si los valores son inválidos
        """
        punto_reorden_vo = Cantidad.from_int(punto_reorden)
        cantidad_pedido_vo = Cantidad.from_int(cantidad_pedido)
        
        return cls(punto_reorden_vo, cantidad_pedido_vo)
    
    def get_punto_reorden(self) -> int:
        """Obtiene el punto de reorden."""
        return int(self.punto_reorden)
    
    def get_cantidad_pedido(self) -> int:
        """Obtiene la cantidad de pedido."""
        return int(self.cantidad_pedido)
    
    def __str__(self) -> str:
        return f"Política (r={self.punto_reorden}, Q={self.cantidad_pedido})" 