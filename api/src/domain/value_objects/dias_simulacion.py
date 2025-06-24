from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError
from api.src.domain.value_objects.base_value_object import BaseValueObject
from typing import Optional

@dataclass(frozen=True)
class DiasSimulacion(BaseValueObject):
    """
    Value Object que representa los días de simulación.
    Debe ser un valor positivo mayor que cero.
    """
    dias: int
    
    @classmethod
    def _get_value_or_default(cls, value: Optional[int]) -> int:
        """
        Obtiene el valor de días de simulación o el valor por defecto de la configuración.
        
        Args:
            value: Valor proporcionado o None para usar valor por defecto
            
        Returns:
            int: Valor de días de simulación
            
        Raises:
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        if value is not None:
            return value
        
        if cls._default_config is not None:
            return cls._default_config.get_dias_simulacion()
        
        raise ValueError("No se proporcionó valor para días de simulación y no hay configuración por defecto")
    
    @classmethod
    def from_int(cls, dias: Optional[int] = None) -> 'DiasSimulacion':
        """
        Naming constructor que valida y crea un DiasSimulacion.
        
        Args:
            dias: Días de simulación (puede ser None para usar valor por defecto)
            
        Returns:
            DiasSimulacion: Una instancia válida de DiasSimulacion
            
        Raises:
            DomainError: Si el valor es inválido
            ValueError: Si el valor es None y no hay configuración por defecto
        """
        actual_dias = cls._get_value_or_default(dias)
        
        if actual_dias <= 0:
            raise DomainError(f"Los días de simulación deben ser mayores que cero, se recibió: {actual_dias}")
        
        return cls(actual_dias)
    
    def get_dias(self) -> int:
        """Obtiene los días de simulación."""
        return self.dias
    
    def __str__(self) -> str:
        return f"Días de simulación: {self.dias}"
    
    @classmethod
    def with_config(cls, config: 'Config') -> 'DiasSimulacion':
        """
        Configura los valores por defecto para este tipo de Value Object.
        
        Args:
            config: Configuración que contiene los valores por defecto
            
        Returns:
            La clase con la configuración establecida
        """
        cls._default_config = config
        return cls
    
    @classmethod
    def clear_default_config(cls) -> None:
        """
        Limpia la configuración por defecto establecida para esta clase.
        """
        cls._default_config = None 