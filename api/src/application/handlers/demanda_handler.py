from api.src.domain.models.evento import EventoDemanda, Evento, EventoLlegadaPedido
from api.src.domain.models.simulation_context import SimulationContext
from api.src.domain.handlers.event_handler import EventHandler

class DemandaEventHandler(EventHandler[EventoDemanda]):
    def can_handle(self, evento: Evento) -> bool:
        return isinstance(evento, EventoDemanda)

    def handle(self, evento: EventoDemanda, context: SimulationContext) -> None:
        cantidad = evento.get_cantidad()
        inventario_actual = context.resultados.obtener_inventario()
        precio_venta = context.configuracion.get_precio_venta()
        if inventario_actual >= cantidad:
            context.resultados.actualizar_inventario(-cantidad)
            context.resultados.agregar_ingreso(cantidad * precio_venta)
        else:
            context.resultados.agregar_ingreso(inventario_actual * precio_venta)
            context.resultados.agregar_costo_faltante((cantidad - inventario_actual) * context.configuracion.get_costo_faltante())
            context.resultados.establecer_inventario(0) 