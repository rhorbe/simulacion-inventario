import yaml
import os
from typing import Dict, Any, List
from api.domain.config import Config

class YmlConfigRepository(Config):
    """
    Implementación de Config que carga la configuración desde un archivo YAML.
    Implementa el patrón Singleton para asegurar una única instancia.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls, config_path: str = None):
        """
        Implementa el patrón Singleton.
        Retorna la misma instancia si ya existe.
        """
        if cls._instance is None:
            cls._instance = super(YmlConfigRepository, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config_path: str = None):
        """
        Inicializa la configuración cargando desde el archivo YAML.
        Solo se ejecuta una vez por instancia.
        
        Args:
            config_path: Ruta al archivo de configuración. Si es None, usa config.yml en el directorio actual.
        """
        if not self._initialized:
            if config_path is None:
                config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
            
            with open(config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
            
            self._initialized = True
    
    def get_simulacion(self) -> Dict[str, Any]:
        """Sección de parámetros de simulación."""
        return self._config.get('simulacion', {})
    
    def get_entrega(self) -> Dict[str, Any]:
        """Sección de parámetros de entrega."""
        return self._config.get('entrega', {})
    
    def get_costos(self) -> Dict[str, Any]:
        """Sección de costos."""
        return self._config.get('costos', {})
    
    def get_precios(self) -> Dict[str, Any]:
        """Sección de precios."""
        return self._config.get('precios', {})
    
    def get_politicas_abastecimiento(self) -> List[Dict[str, Any]]:
        """Lista de políticas de abastecimiento."""
        return self._config.get('politicas_abastecimiento', []) 