import random
from typing import Optional
from .base_object_mother import BaseObjectMother

class TiempoEntregaMother(BaseObjectMother):
    """
    Object Mother para generar tiempos de entrega aleatorios.
    Encapsula la lógica de generación de plazos de entrega usando distribución uniforme.
    """
    
    def __init__(self, seed: Optional[int] = 42):
        """
        Inicializa el generador de tiempos de entrega.
        
        Args:
            seed: Semilla para el generador de números aleatorios (opcional)
        """
        self.generador_aleatorio = random.Random(seed)
    
    def generar_tiempo_entrega(self, plazo_min: int, plazo_max: int) -> int:
        """
        Genera un plazo de entrega aleatorio en días.

        El plazo de entrega se asume como una variable aleatoria con distribución uniforme
        entre plazo_min y plazo_max.

        Args:
            plazo_min (int): Plazo mínimo de entrega
            plazo_max (int): Plazo máximo de entrega

        Returns:
            int: Plazo de entrega aleatorio en días.
        """
        return self.generador_aleatorio.randint(plazo_min, plazo_max)
    
    def value(self, plazo_min: int, plazo_max: int) -> int:
        """
        Método de conveniencia que genera un tiempo de entrega aleatorio.
        Permite uso fluido: TiempoEntregaMother.random(seed=42).value(plazo_min, plazo_max)
        
        Args:
            plazo_min (int): Plazo mínimo de entrega
            plazo_max (int): Plazo máximo de entrega
            
        Returns:
            int: Plazo de entrega aleatorio en días.
        """
        return self.generar_tiempo_entrega(plazo_min, plazo_max)
    
    def set_seed(self, seed: int) -> None:
        """
        Establece una nueva semilla para el generador de números aleatorios.
        
        Args:
            seed: Nueva semilla para el generador
        """
        self.generador_aleatorio = random.Random(seed)

    @classmethod
    def random(cls, seed=42):
        return cls(seed=seed) 