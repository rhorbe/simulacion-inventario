from dataclasses import dataclass
from api.src.domain.models.evento import Evento
from api.src.domain.models.event_handler import EventHandler
from api.src.domain.models.simulation_context import SimulationContext

@dataclass
class LlegadaPedidoEventHandler:
    """Handler para eventos de llegada de pedido"""
    
    def can_handle(self, evento: Evento) -> bool:
        return evento.__class__.__name__ == 'EventoLlegadaPedido'
    
    def handle(self, evento, context: SimulationContext) -> None:
        cantidad = evento.get_cantidad()
        context.resultados.actualizar_inventario(cantidad) 