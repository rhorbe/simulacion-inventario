from dataclasses import dataclass
from ..value_objects import PoliticaInventario, ConfiguracionSimulacion

@dataclass
class ResultadosPolitica:
    """
    Clase que encapsula los resultados de la simulación de inventario para una política específica.
    Contiene todos los costos e ingresos acumulados durante la simulación, junto con los parámetros de la política
    y las variables de estado que mutan durante la ejecución.
    """
    r: int
    Q: int
    inventario: int
    costo_almacenamiento: float = 0.0
    costo_total_faltante: float = 0.0
    costo_pedidos: float = 0.0
    ingresos: float = 0.0
    
    @classmethod
    def from_politica_and_config(cls, politica: PoliticaInventario, configuracion: ConfiguracionSimulacion) -> 'ResultadosPolitica':
        """
        Constructor de clase que crea una instancia de ResultadosPolitica a partir de una política y configuración.
        
        Args:
            politica: Política de inventario (r, Q)
            configuracion: Configuración de la simulación
            
        Returns:
            ResultadosPolitica: Nueva instancia inicializada con los parámetros de la política y el inventario inicial
        """
        return cls(
            r=politica.get_punto_reorden(),
            Q=politica.get_cantidad_pedido(),
            inventario=configuracion.get_inventario_inicial()
        )
    
    def agregar_costo_almacenamiento(self, costo: float) -> None:
        """Agrega un costo de almacenamiento al total acumulado."""
        self.costo_almacenamiento += costo
    
    def agregar_costo_faltante(self, costo: float) -> None:
        """Agrega un costo por faltante al total acumulado."""
        self.costo_total_faltante += costo
    
    def agregar_costo_pedido(self, costo: float) -> None:
        """Agrega un costo de pedido al total acumulado."""
        self.costo_pedidos += costo
    
    def agregar_ingreso(self, ingreso: float) -> None:
        """Agrega un ingreso al total acumulado."""
        self.ingresos += ingreso
    
    def actualizar_inventario(self, cantidad: int) -> None:
        """Actualiza el nivel de inventario (puede ser positivo para incrementos o negativo para decrementos)."""
        self.inventario += cantidad
    
    def establecer_inventario(self, cantidad: int) -> None:
        """Establece el nivel de inventario a un valor específico."""
        self.inventario = cantidad
    
    def obtener_inventario(self) -> int:
        """Obtiene el nivel actual de inventario."""
        return self.inventario
    
    def calcular_ganancia(self) -> float:
        """Calcula la ganancia total (ingresos - costos totales)."""
        costo_total = self.costo_almacenamiento + self.costo_total_faltante + self.costo_pedidos
        return self.ingresos - costo_total
    
    def to_dict(self) -> dict:
        """
        Convierte los resultados a un diccionario con el formato esperado por la API.
        
        Returns:
            dict: Diccionario con todos los resultados de la simulación
        """
        return {
            "r": self.r,
            "Q": self.Q,
            "ingresos": self.ingresos,
            "costo_alm": self.costo_almacenamiento,
            "costo_faltante": self.costo_total_faltante,
            "costo_pedidos": self.costo_pedidos,
            "ganancia": self.calcular_ganancia(),
        } 