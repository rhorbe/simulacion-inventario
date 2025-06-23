import numpy as np
from typing import Optional
from .base_object_mother import BaseObjectMother

class DemandaMother(BaseObjectMother):
    """
    Object Mother para generar demandas aleatorias.
    Encapsula la lógica de generación de demandas usando distribución de Poisson.
    """
    
    def __init__(self, seed: Optional[int] = 42):
        """
        Inicializa el generador de demandas.
        
        Args:
            seed: Semilla para el generador de números aleatorios (opcional)
        """
        self.generador_aleatorio = np.random.default_rng(seed=seed)
    
    def generar_demanda(self, demanda_media: int) -> int:
        """
        Genera una demanda aleatoria para un día.

        La demanda se asume como una variable aleatoria con distribución de Poisson
        con media demanda_media.

        Args:
            demanda_media (int): Media de la distribución de Poisson

        Returns:
            int: Demanda aleatoria para un día.
        """
        return self.generador_aleatorio.poisson(demanda_media)
    
    def value(self, demanda_media: int) -> int:
        """
        Método de conveniencia que genera una demanda aleatoria.
        Permite uso fluido: DemandaMother.random(seed=42).value(demanda_media)
        
        Args:
            demanda_media (int): Media de la distribución de Poisson
            
        Returns:
            int: Demanda aleatoria para un día.
        """
        return self.generar_demanda(demanda_media)
    
    def set_seed(self, seed: int) -> None:
        """
        Establece una nueva semilla para el generador de números aleatorios.
        
        Args:
            seed: Nueva semilla para el generador
        """
        self.generador_aleatorio = np.random.default_rng(seed=seed)

    @classmethod
    def random(cls, seed=42):
        return cls(seed=seed) 