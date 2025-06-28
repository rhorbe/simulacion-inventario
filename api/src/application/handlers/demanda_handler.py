from dataclasses import dataclass
from api.src.domain.models.evento import Evento
from api.src.domain.models.event_handler import EventHandler
from api.src.domain.models.simulation_context import SimulationContext

@dataclass
class DemandaEventHandler:
    """Handler para eventos de demanda"""
    
    def can_handle(self, evento: Evento) -> bool:
        return evento.__class__.__name__ == 'EventoDemanda'
    
    def handle(self, evento, context: SimulationContext) -> None:
        d = evento.get_cantidad()
        inventario_actual = context.resultados.obtener_inventario()
        ventas = min(d, inventario_actual)
        faltante = max(0, d - inventario_actual)
        
        context.resultados.actualizar_inventario(-ventas)
        context.resultados.agregar_ingreso(ventas * context.configuracion.get_precio_venta())
        context.resultados.agregar_costo_faltante(faltante * context.configuracion.get_costo_faltante()) 