from api.src.domain.models.evento import EventoLlegadaPedido, Evento
from api.src.domain.models.simulation_context import SimulationContext
from api.src.domain.bus.event_bus import EventHandler

class LlegadaPedidoEventHandler(EventHandler[EventoLlegadaPedido]):
    """Handler para eventos de llegada de pedido"""
    
    def can_handle(self, evento: Evento) -> bool:
        """Determina si este handler puede manejar el evento"""
        return isinstance(evento, EventoLlegadaPedido)
    
    def handle(self, evento: EventoLlegadaPedido, context: SimulationContext) -> None:
        """Maneja el evento de llegada de pedido"""
        cantidad = evento.get_cantidad()
        context.actualizar_inventario(cantidad) 