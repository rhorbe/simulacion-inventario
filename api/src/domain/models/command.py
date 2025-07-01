from abc import abstractmethod
from dataclasses import dataclass
from typing import List
from .message import BaseMessage
from ..value_objects import PoliticaInventario, ConfiguracionSimulacion

class Comando(BaseMessage):
    """Interfaz base para todos los comandos"""
    pass

@dataclass
class SimularCommand(Comando):
    """Comando para ejecutar la simulación de inventario"""
    politicas: List[PoliticaInventario]
    configuracion: ConfiguracionSimulacion 