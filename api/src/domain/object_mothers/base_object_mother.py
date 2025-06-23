from abc import ABC, abstractmethod

class BaseObjectMother(ABC):
    """
    Clase base abstracta para todos los Object Mother del dominio.
    """
    @classmethod
    @abstractmethod
    def random(cls, seed):
        """
        Devuelve una instancia del Object Mother con la semilla indicada.
        """
        pass 