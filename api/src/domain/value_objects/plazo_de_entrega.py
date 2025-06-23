from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class PlazoDeEntrega(BaseValueObject):
    """
    Value Object que representa un plazo de entrega en el dominio.
    Encapsula el plazo mínimo y máximo de entrega.
    El plazo máximo no puede ser menor al mínimo.
    Ambos plazos deben ser no negativos.
    """
    plazo_minimo: int
    plazo_maximo: int
    
    @classmethod
    def _get_value_or_default(cls, value: Optional[int]) -> int:
        """
        Este método no se usa directamente en PlazoDeEntrega.
        Se implementa para cumplir con la interfaz abstracta.
        """
        raise NotImplementedError("Este método no se usa en PlazoDeEntrega")
    
    @classmethod
    def from_plazos(cls, plazo_minimo: Optional[int] = None, plazo_maximo: Optional[int] = None) -> 'PlazoDeEntrega':
        """
        Naming constructor que valida y crea un PlazoDeEntrega.
        
        Args:
            plazo_minimo: El plazo mínimo de entrega en días (puede ser None para usar valor por defecto)
            plazo_maximo: El plazo máximo de entrega en días (puede ser None para usar valor por defecto)
            
        Returns:
            PlazoDeEntrega: Una instancia válida de PlazoDeEntrega
            
        Raises:
            DomainError: Si los plazos son inválidos
            ValueError: Si algún valor es None y no hay configuración por defecto
        """
        # Obtener valores o usar valores por defecto
        if plazo_minimo is not None:
            actual_plazo_minimo = plazo_minimo
        elif cls._default_config is not None:
            entrega = cls._default_config.get_entrega()
            if 'plazo_min' in entrega:
                actual_plazo_minimo = entrega['plazo_min']
            else:
                raise ValueError("No se proporcionó valor para plazo_minimo y no hay configuración por defecto")
        else:
            raise ValueError("No se proporcionó valor para plazo_minimo y no hay configuración por defecto")
        
        if plazo_maximo is not None:
            actual_plazo_maximo = plazo_maximo
        elif cls._default_config is not None:
            entrega = cls._default_config.get_entrega()
            if 'plazo_max' in entrega:
                actual_plazo_maximo = entrega['plazo_max']
            else:
                raise ValueError("No se proporcionó valor para plazo_maximo y no hay configuración por defecto")
        else:
            raise ValueError("No se proporcionó valor para plazo_maximo y no hay configuración por defecto")
        
        if actual_plazo_minimo < 0:
            raise DomainError("El plazo mínimo de entrega no puede ser negativo")
        
        if actual_plazo_maximo < 0:
            raise DomainError("El plazo máximo de entrega no puede ser negativo")
        
        if actual_plazo_maximo < actual_plazo_minimo:
            raise DomainError("El plazo máximo de entrega no puede ser menor al plazo mínimo")
        
        return cls(actual_plazo_minimo, actual_plazo_maximo)
    
    def get_plazo_minimo(self) -> int:
        """Obtiene el plazo mínimo de entrega."""
        return self.plazo_minimo
    
    def get_plazo_maximo(self) -> int:
        """Obtiene el plazo máximo de entrega."""
        return self.plazo_maximo
    
    def __str__(self) -> str:
        return f"Plazo de entrega: {self.plazo_minimo}-{self.plazo_maximo} días" 