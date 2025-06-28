from dataclasses import dataclass
from typing import List
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion


@dataclass
class SimularCommand:
    """Comando para ejecutar la simulación de inventario"""
    politicas: List[PoliticaInventario]
    configuracion: ConfiguracionSimulacion 