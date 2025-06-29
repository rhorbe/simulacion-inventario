from api.src.domain.models.evento import EventoLlegadaPedido, Evento
from api.src.domain.models.simulation_context import SimulationContext
from api.src.domain.handlers.event_handler import EventHandler

class LlegadaPedidoEventHandler(EventHandler[EventoLlegadaPedido]):
    """Handler para eventos de llegada de pedido"""
    
    def can_handle(self, evento: Evento) -> bool:
        return isinstance(evento, EventoLlegadaPedido)
    
    def handle(self, evento: EventoLlegadaPedido, context: SimulationContext) -> None:
        cantidad = evento.get_cantidad()
        context.resultados.actualizar_inventario(cantidad) 