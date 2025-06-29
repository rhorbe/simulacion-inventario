from api.src.domain.models.evento import EventoDemanda, Evento
from api.src.domain.models.simulation_context import SimulationContext
from api.src.domain.bus.event_bus import EventHandler

class DemandaEventHandler(EventHandler[EventoDemanda]):
    """Handler para eventos de demanda"""
    
    def can_handle(self, evento: Evento) -> bool:
        """Determina si este handler puede manejar el evento"""
        return isinstance(evento, EventoDemanda)

    def handle(self, evento: EventoDemanda, context: SimulationContext) -> None:
        """Maneja el evento de demanda"""
        cantidad = evento.get_cantidad()
        inventario_actual = context.obtener_inventario()
        precio_venta = context.configuracion.get_precio_venta()
        if inventario_actual >= cantidad:
            context.actualizar_inventario(-cantidad)
            context.agregar_ingreso(cantidad * precio_venta)
        else:
            context.agregar_ingreso(inventario_actual * precio_venta)
            context.agregar_costo_faltante((cantidad - inventario_actual) * context.configuracion.get_costo_faltante())
            context.establecer_inventario(0) 