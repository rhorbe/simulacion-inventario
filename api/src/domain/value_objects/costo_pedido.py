from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError

@dataclass(frozen=True)
class CostoPedido:
    """
    Value Object que representa los costos de pedido en el dominio.
    Encapsula el costo para pedidos pequeños y grandes.
    El costo de pedido pequeño debe ser mayor al costo de pedido grande.
    Ambos costos deben ser no negativos.
    """
    costo_pedido_pequeno: float
    costo_pedido_grande: float
    
    @classmethod
    def from_costos(cls, costo_pedido_pequeno: float, costo_pedido_grande: float) -> 'CostoPedido':
        """
        Naming constructor que valida y crea un CostoPedido.
        
        Args:
            costo_pedido_pequeno: El costo por unidad para pedidos pequeños
            costo_pedido_grande: El costo por unidad para pedidos grandes
            
        Returns:
            CostoPedido: Una instancia válida de CostoPedido
            
        Raises:
            DomainError: Si los costos son inválidos
        """
        if costo_pedido_pequeno < 0:
            raise DomainError("El costo de pedido pequeño no puede ser negativo")
        
        if costo_pedido_grande < 0:
            raise DomainError("El costo de pedido grande no puede ser negativo")
        
        if costo_pedido_pequeno <= costo_pedido_grande:
            raise DomainError("El costo de pedido pequeño debe ser mayor al costo de pedido grande")
        
        return cls(costo_pedido_pequeno, costo_pedido_grande)
    
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