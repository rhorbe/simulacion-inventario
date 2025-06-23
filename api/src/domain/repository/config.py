from abc import ABC, abstractmethod
from typing import Dict, Any, List

class Config(ABC):
    """
    Interfaz abstracta para la configuración del sistema.
    Define el contrato que deben implementar las fuentes de configuración.
    """
    
    @abstractmethod
    def get_simulacion(self) -> Dict[str, Any]:
        """Obtiene la sección de parámetros de simulación."""
        pass
    
    @abstractmethod
    def get_entrega(self) -> Dict[str, Any]:
        """Obtiene la sección de parámetros de entrega."""
        pass
    
    @abstractmethod
    def get_costos(self) -> Dict[str, Any]:
        """Obtiene la sección de costos."""
        pass
    
    @abstractmethod
    def get_precios(self) -> Dict[str, Any]:
        """Obtiene la sección de precios."""
        pass
    
    @abstractmethod
    def get_politicas_abastecimiento(self) -> List[Dict[str, Any]]:
        """Obtiene la lista de políticas de abastecimiento."""
        pass
    
    # Propiedades para mantener compatibilidad con la interfaz existente
    @property
    def simulacion(self) -> Dict[str, Any]:
        """Sección de parámetros de simulación."""
        return self.get_simulacion()
    
    @property
    def entrega(self) -> Dict[str, Any]:
        """Sección de parámetros de entrega."""
        return self.get_entrega()
    
    @property
    def costos(self) -> Dict[str, Any]:
        """Sección de costos."""
        return self.get_costos()
    
    @property
    def precios(self) -> Dict[str, Any]:
        """Sección de precios."""
        return self.get_precios()
    
    @property
    def politicas_abastecimiento(self) -> List[Dict[str, Any]]:
        """Lista de políticas de abastecimiento."""
        return self.get_politicas_abastecimiento() 