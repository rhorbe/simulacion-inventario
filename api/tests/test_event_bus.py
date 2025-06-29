import pytest
from api.src.domain.bus.event_bus import EventBus
from api.src.infra.bus.in_memory_event_bus import InMemoryEventBus
from api.src.application.handlers.demanda_handler import DemandaEventHandler
from api.src.application.handlers.llegada_pedido_handler import LlegadaPedidoEventHandler
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido
from api.src.domain.models.simulation_context import SimulationContext
from api.src.domain.value_objects.configuracion_simulacion import ConfiguracionSimulacion
from api.src.domain.value_objects.precio_venta import PrecioVenta
from api.src.domain.value_objects.costo_faltante import CostoFaltante
from api.src.domain.value_objects.precio import Precio

# Valores dummy para los parámetros requeridos
PARAMS = dict(
    inventario_inicial=10,
    precio_venta=100.0,
    costo_almacenar=1.0,
    costo_faltante=50.0,
    costo_pedido_pequeno=5.0,
    costo_pedido_grande=3.0,
    plazo_entrega_min=1,
    plazo_entrega_max=2,
    demanda_media=10,
    dias_simulacion=30
)

class TestEventBus:
    
    def test_dispatch_demanda_event(self):
        bus = InMemoryEventBus()
        bus.register_handler(EventoDemanda, DemandaEventHandler())
        bus.register_handler(EventoLlegadaPedido, LlegadaPedidoEventHandler())
        
        evento = EventoDemanda(10, 5)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(r=10, Q=20, inventario=10, configuracion=configuracion)
        
        bus.dispatch(evento, context)
        
        # Verificar que se procesó correctamente
        assert context.obtener_inventario() == 5  # 10 - 5
        assert context.ingresos == 500.0  # 5 * 100
    
    def test_dispatch_llegada_pedido_event(self):
        bus = InMemoryEventBus()
        bus.register_handler(EventoDemanda, DemandaEventHandler())
        bus.register_handler(EventoLlegadaPedido, LlegadaPedidoEventHandler())
        
        evento = EventoLlegadaPedido(10, 15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(r=10, Q=20, inventario=5, configuracion=configuracion)
        
        bus.dispatch(evento, context)
        
        # Verificar que se procesó correctamente
        assert context.obtener_inventario() == 20  # 5 + 15
    
    def test_dispatch_unknown_event_raises_error(self):
        bus = InMemoryEventBus()
        bus.register_handler(EventoDemanda, DemandaEventHandler())
        bus.register_handler(EventoLlegadaPedido, LlegadaPedidoEventHandler())
        
        # Crear un evento desconocido (mock)
        class EventoDesconocido:
            pass
        
        evento = EventoDesconocido()
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(r=10, Q=20, inventario=5, configuracion=configuracion)
        
        with pytest.raises(ValueError, match="No se encontró handler para el evento"):
            bus.dispatch(evento, context)
    
    def test_register_handler(self):
        """Test que verifica que se pueden registrar handlers"""
        bus = InMemoryEventBus()
        handler = DemandaEventHandler()
        
        bus.register_handler(EventoDemanda, handler)
        
        # Verificar que el handler está registrado
        assert EventoDemanda in bus._handlers
        assert bus._handlers[EventoDemanda] == handler
    
    def test_register_multiple_handlers(self):
        """Test que verifica que se pueden registrar múltiples handlers"""
        bus = InMemoryEventBus()
        demanda_handler = DemandaEventHandler()
        llegada_handler = LlegadaPedidoEventHandler()
        
        bus.register_handler(EventoDemanda, demanda_handler)
        bus.register_handler(EventoLlegadaPedido, llegada_handler)
        
        # Verificar que ambos handlers están registrados
        assert EventoDemanda in bus._handlers
        assert EventoLlegadaPedido in bus._handlers
        assert bus._handlers[EventoDemanda] == demanda_handler
        assert bus._handlers[EventoLlegadaPedido] == llegada_handler 