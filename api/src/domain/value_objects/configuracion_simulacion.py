from dataclasses import dataclass
from api.src.domain.exceptions.domain_error import DomainError
from api.src.domain.value_objects.inventario_inicial import InventarioInicial
from api.src.domain.value_objects.demanda_media import DemandaMedia
from api.src.domain.value_objects.precio_venta import PrecioVenta
from api.src.domain.value_objects.plazo_de_entrega import PlazoDeEntrega
from api.src.domain.value_objects.costo_pedido import CostoPedido
from api.src.domain.value_objects.costo_almacenar import CostoAlmacenar
from api.src.domain.value_objects.costo_faltante import CostoFaltante
from api.src.domain.value_objects.base_value_object import BaseValueObject
from api.src.domain.repository.config import Config
from typing import Optional, Any

@dataclass(frozen=True)
class ConfiguracionSimulacion(BaseValueObject):
    """
    Value Object que representa la configuración completa de una simulación.
    Encapsula todos los parámetros necesarios para ejecutar la simulación.
    """
    inventario_inicial: InventarioInicial
    precio_venta: PrecioVenta
    costo_almacenar: CostoAlmacenar
    costo_faltante: CostoFaltante
    costo_pedido: CostoPedido
    plazo_entrega: PlazoDeEntrega
    demanda_media: DemandaMedia
    
    @classmethod
    def _get_value_or_default(cls, value: Optional[Any]) -> Any:
        """
        Este método no se usa directamente en ConfiguracionSimulacion.
        Se implementa para cumplir con la interfaz abstracta.
        """
        raise NotImplementedError("Este método no se usa en ConfiguracionSimulacion")
    
    @classmethod
    def from_parametros(
        cls,
        inventario_inicial: Optional[int] = None,
        precio_venta: Optional[float] = None,
        costo_almacenar: Optional[float] = None,
        costo_faltante: Optional[float] = None,
        costo_pedido_pequeno: Optional[float] = None,
        costo_pedido_grande: Optional[float] = None,
        plazo_entrega_min: Optional[int] = None,
        plazo_entrega_max: Optional[int] = None,
        demanda_media: Optional[int] = None
    ) -> 'ConfiguracionSimulacion':
        """
        Naming constructor que valida y crea una ConfiguracionSimulacion.
        
        Args:
            inventario_inicial: Inventario inicial (puede ser None para usar valor por defecto)
            precio_venta: Precio de venta por unidad (puede ser None para usar valor por defecto)
            costo_almacenar: Costo de almacenamiento por unidad por día (puede ser None para usar valor por defecto)
            costo_faltante: Costo por unidad faltante (puede ser None para usar valor por defecto)
            costo_pedido_pequeno: Costo por unidad para pedidos pequeños (puede ser None para usar valor por defecto)
            costo_pedido_grande: Costo por unidad para pedidos grandes (puede ser None para usar valor por defecto)
            plazo_entrega_min: Plazo mínimo de entrega en días (puede ser None para usar valor por defecto)
            plazo_entrega_max: Plazo máximo de entrega en días (puede ser None para usar valor por defecto)
            demanda_media: Demanda media diaria (puede ser None para usar valor por defecto)
            
        Returns:
            ConfiguracionSimulacion: Una instancia válida de ConfiguracionSimulacion
            
        Raises:
            DomainError: Si algún parámetro es inválido
            ValueError: Si algún valor es None y no hay configuración por defecto
        """
        return cls(
            inventario_inicial=InventarioInicial.from_int(inventario_inicial),
            precio_venta=PrecioVenta.from_float(precio_venta),
            costo_almacenar=CostoAlmacenar.from_float(costo_almacenar),
            costo_faltante=CostoFaltante.from_float(costo_faltante),
            costo_pedido=CostoPedido.from_costos(costo_pedido_pequeno, costo_pedido_grande),
            plazo_entrega=PlazoDeEntrega.from_plazos(plazo_entrega_min, plazo_entrega_max),
            demanda_media=DemandaMedia.from_int(demanda_media)
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
    
    @classmethod
    def with_config(cls, config: 'Config') -> 'ConfiguracionSimulacion':
        """
        Configura los valores por defecto para este tipo de Value Object y todos los Value Objects que usa.
        
        Args:
            config: Configuración que contiene los valores por defecto
            
        Returns:
            La clase con la configuración establecida
        """
        # Configurar la configuración por defecto para esta clase
        cls._default_config = config
        
        # Configurar la configuración por defecto para todos los Value Objects que usa
        InventarioInicial.with_config(config)
        DemandaMedia.with_config(config)
        PrecioVenta.with_config(config)
        CostoAlmacenar.with_config(config)
        CostoFaltante.with_config(config)
        CostoPedido.with_config(config)
        PlazoDeEntrega.with_config(config)
        
        return cls 

    @classmethod
    def clear_default_config(cls) -> None:
        """
        Limpia la configuración por defecto establecida para esta clase y todos los Value Objects que usa.
        """
        cls._default_config = None
        
        # Limpiar la configuración por defecto de todos los Value Objects que usa
        InventarioInicial.clear_default_config()
        DemandaMedia.clear_default_config()
        PrecioVenta.clear_default_config()
        CostoAlmacenar.clear_default_config()
        CostoFaltante.clear_default_config()
        CostoPedido.clear_default_config()
        PlazoDeEntrega.clear_default_config() 