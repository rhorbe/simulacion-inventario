# Este archivo hace que el directorio sea un paquete de Python 

# Importaciones de todas las funciones factory desde archivos separados
from .config_factory import get_config
from .command_bus_factory import get_command_bus
from .event_bus_factory import get_event_bus

# Re-exportar todas las funciones para mantener la compatibilidad
__all__ = [
    'get_config',
    'get_command_bus', 
    'get_event_bus'
] 