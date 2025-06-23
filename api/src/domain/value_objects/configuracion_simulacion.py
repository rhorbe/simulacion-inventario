from dataclasses import dataclass
from api.src.domain.value_objects.cantidad import Cantidad
from api.src.domain.value_objects.precio import Precio
from api.src.domain.value_objects.plazo_de_entrega import PlazoDeEntrega
from api.src.domain.value_objects.costo_pedido import CostoPedido

@dataclass(frozen=True)
class ConfiguracionSimulacion:
    """
    Value Object que representa la configuración completa de una simulación.
    Encapsula todos los parámetros necesarios para ejecutar la simulación.
    """
    inventario_inicial: Cantidad
    precio_venta: Precio
    costo_almacenar: Precio
    costo_faltante: Precio
    costo_pedido: CostoPedido
    plazo_entrega: PlazoDeEntrega
    demanda_media: Cantidad
    
    @classmethod
    def from_parametros(
        cls,
        inventario_inicial: int,
        precio_venta: float,
        costo_almacenar: float,
        costo_faltante: float,
        costo_pedido_pequeno: float,
        costo_pedido_grande: float,
        plazo_entrega_min: int,
        plazo_entrega_max: int,
        demanda_media: int
    ) -> 'ConfiguracionSimulacion':
        """
        Naming constructor que valida y crea una ConfiguracionSimulacion.
        
        Args:
            inventario_inicial: Inventario inicial
            precio_venta: Precio de venta por unidad
            costo_almacenar: Costo de almacenamiento por unidad por día
            costo_faltante: Costo por unidad faltante
            costo_pedido_pequeno: Costo por unidad para pedidos pequeños
            costo_pedido_grande: Costo por unidad para pedidos grandes
            plazo_entrega_min: Plazo mínimo de entrega en días
            plazo_entrega_max: Plazo máximo de entrega en días
            demanda_media: Demanda media diaria
            
        Returns:
            ConfiguracionSimulacion: Una instancia válida de ConfiguracionSimulacion
            
        Raises:
            DomainError: Si algún parámetro es inválido
        """
        return cls(
            inventario_inicial=Cantidad.from_int(inventario_inicial),
            precio_venta=Precio.from_float(precio_venta),
            costo_almacenar=Precio.from_float(costo_almacenar),
            costo_faltante=Precio.from_float(costo_faltante),
            costo_pedido=CostoPedido.from_costos(costo_pedido_pequeno, costo_pedido_grande),
            plazo_entrega=PlazoDeEntrega.from_plazos(plazo_entrega_min, plazo_entrega_max),
            demanda_media=Cantidad.from_int(demanda_media)
        )
    
    def get_inventario_inicial(self) -> int:
        """Obtiene el inventario inicial."""
        return int(self.inventario_inicial)
    
    def get_precio_venta(self) -> float:
        """Obtiene el precio de venta."""
        return float(self.precio_venta)
    
    def get_costo_almacenar(self) -> float:
        """Obtiene el costo de almacenamiento."""
        return float(self.costo_almacenar)
    
    def get_costo_faltante(self) -> float:
        """Obtiene el costo por faltante."""
        return float(self.costo_faltante)
    
    def get_costo_pedido_pequeno(self) -> float:
        """Obtiene el costo de pedido pequeño."""
        return self.costo_pedido.get_costo_pedido_pequeno()
    
    def get_costo_pedido_grande(self) -> float:
        """Obtiene el costo de pedido grande."""
        return self.costo_pedido.get_costo_pedido_grande()
    
    def get_plazo_entrega_min(self) -> int:
        """Obtiene el plazo mínimo de entrega."""
        return self.plazo_entrega.get_plazo_minimo()
    
    def get_plazo_entrega_max(self) -> int:
        """Obtiene el plazo máximo de entrega."""
        return self.plazo_entrega.get_plazo_maximo()
    
    def get_demanda_media(self) -> int:
        """Obtiene la demanda media."""
        return int(self.demanda_media)
    
    def calcular_costo_unitario_pedido(self, cantidad: int) -> float:
        """Calcula el costo unitario de un pedido según su cantidad."""
        return self.costo_pedido.calcular_costo_unitario(cantidad)
    
    def __str__(self) -> str:
        return f"Configuración: Inventario inicial={self.inventario_inicial}, Precio venta={self.precio_venta}, Demanda media={self.demanda_media}" 