from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError

@dataclass(frozen=True)
class PlazoDeEntrega:
    """
    Value Object que representa un plazo de entrega en el dominio.
    Encapsula el plazo mínimo y máximo de entrega.
    El plazo máximo no puede ser menor al mínimo.
    Ambos plazos deben ser no negativos.
    """
    plazo_minimo: int
    plazo_maximo: int
    
    @classmethod
    def from_plazos(cls, plazo_minimo: int, plazo_maximo: int) -> 'PlazoDeEntrega':
        """
        Naming constructor que valida y crea un PlazoDeEntrega.
        
        Args:
            plazo_minimo: El plazo mínimo de entrega en días
            plazo_maximo: El plazo máximo de entrega en días
            
        Returns:
            PlazoDeEntrega: Una instancia válida de PlazoDeEntrega
            
        Raises:
            DomainError: Si los plazos son inválidos
        """
        if plazo_minimo < 0:
            raise DomainError("El plazo mínimo de entrega no puede ser negativo")
        
        if plazo_maximo < 0:
            raise DomainError("El plazo máximo de entrega no puede ser negativo")
        
        if plazo_maximo < plazo_minimo:
            raise DomainError("El plazo máximo de entrega no puede ser menor al plazo mínimo")
        
        return cls(plazo_minimo, plazo_maximo)
    
    def get_plazo_minimo(self) -> int:
        """Obtiene el plazo mínimo de entrega."""
        return self.plazo_minimo
    
    def get_plazo_maximo(self) -> int:
        """Obtiene el plazo máximo de entrega."""
        return self.plazo_maximo
    
    def __str__(self) -> str:
        return f"Plazo de entrega: {self.plazo_minimo}-{self.plazo_maximo} días" 