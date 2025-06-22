import yaml
import os
from typing import Dict, Any, List

class Config:
    """
    Clase Singleton para manejar la configuración del proyecto.
    Permite acceder a las secciones de configuración como atributos.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls, config_path: str = None):
        """
        Implementa el patrón Singleton.
        Retorna la misma instancia si ya existe.
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
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
    
    @property
    def simulacion(self) -> Dict[str, Any]:
        """Sección de parámetros de simulación."""
        return self._config.get('simulacion', {})
    
    @property
    def entrega(self) -> Dict[str, Any]:
        """Sección de parámetros de entrega."""
        return self._config.get('entrega', {})
    
    @property
    def costos(self) -> Dict[str, Any]:
        """Sección de costos."""
        return self._config.get('costos', {})
    
    @property
    def precios(self) -> Dict[str, Any]:
        """Sección de precios."""
        return self._config.get('precios', {})
    
    @property
    def politicas_abastecimiento(self) -> List[Dict[str, Any]]:
        """Lista de políticas de abastecimiento."""
        return self._config.get('politicas_abastecimiento', [])

# Instancia global de configuración
config = Config()

# Variables de compatibilidad para mantener la interfaz existente
INVENTARIO_INICIAL = config.simulacion.get('inventario_inicial')
DEMANDA_MEDIA = config.simulacion.get('demanda_media')
PLAZO_ENTREGA_MIN = config.entrega.get('plazo_min')
PLAZO_ENTREGA_MAX = config.entrega.get('plazo_max')

COSTO_ALMACENAR = config.costos.get('almacenar')
COSTO_FALTANTE = config.costos.get('faltante')
COSTO_PEDIDO_PEQUENO = config.costos.get('pedido_pequeno')
COSTO_PEDIDO_GRANDE = config.costos.get('pedido_grande')

PRECIO_VENTA = config.precios.get('venta')

DIAS_SIMULACION = config.simulacion.get('dias_simulacion')
ANIOS_SIMULACION = config.simulacion.get('anios_simulacion')

POLITICAS_ABASTECIMIENTO = config.politicas_abastecimiento
