from dataclasses import dataclass
from .resultados_politica import ResultadosPolitica
from ..value_objects.configuracion_simulacion import ConfiguracionSimulacion

@dataclass
class SimulationContext:
    """Contexto que contiene los datos compartidos de la simulación"""
    resultados: ResultadosPolitica
    configuracion: ConfiguracionSimulacion 