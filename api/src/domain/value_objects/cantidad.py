from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError

@dataclass(frozen=True)
class Cantidad:
    """
    Value Object que representa una cantidad en el dominio.
    Una cantidad debe ser un entero no negativo.
    """
    valor: int
    
    @classmethod
    def from_int(cls, valor: int) -> 'Cantidad':
        """
        Naming constructor que valida y crea una Cantidad.
        
        Args:
            valor: El valor de la cantidad
            
        Returns:
            Cantidad: Una instancia válida de Cantidad
            
        Raises:
            DomainError: Si la cantidad es negativa
        """
        if valor < 0:
            raise DomainError("La cantidad no puede ser negativa")
        
        return cls(valor)
    
    def __int__(self) -> int:
        """Convierte el ValueObject a int."""
        return self.valor
    
    def __str__(self) -> str:
        return str(self.valor) 