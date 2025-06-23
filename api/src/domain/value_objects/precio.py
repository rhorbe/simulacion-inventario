from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError

@dataclass(frozen=True)
class Precio:
    """
    Value Object que representa un precio en el dominio.
    Un precio no puede ser negativo.
    """
    valor: float
    
    @classmethod
    def from_float(cls, valor: float) -> 'Precio':
        """
        Naming constructor que valida y crea un Precio.
        
        Args:
            valor: El valor del precio
            
        Returns:
            Precio: Una instancia válida de Precio
            
        Raises:
            DomainError: Si el precio es negativo
        """
        if valor < 0:
            raise DomainError("El precio no puede ser negativo")
        
        return cls(valor)
    
    def __float__(self) -> float:
        """Convierte el ValueObject a float."""
        return self.valor
    
    def __str__(self) -> str:
        return f"${self.valor:.2f}" 