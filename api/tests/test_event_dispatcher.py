import pytest
from src.domain.models.event_dispatcher import EventDispatcher
from src.application.handlers.demanda_handler import DemandaEventHandler
from src.application.handlers.llegada_pedido_handler import LlegadaPedidoEventHandler
from src.domain.models.evento import EventoDemanda, EventoLlegadaPedido
from src.domain.models.resultados_politica import ResultadosPolitica
from src.domain.models.simulation_context import SimulationContext
from src.domain.value_objects.configuracion_simulacion import ConfiguracionSimulacion
from src.domain.value_objects.precio_venta import PrecioVenta
from src.domain.value_objects.costo_faltante import CostoFaltante
from src.domain.value_objects.precio import Precio

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

class TestEventDispatcher:
    
    def test_dispatch_demanda_event(self):
        dispatcher = EventDispatcher([
            DemandaEventHandler(),
            LlegadaPedidoEventHandler()
        ])
        
        evento = EventoDemanda(10, 5)
        resultados = ResultadosPolitica(r=10, Q=20, inventario=10)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(resultados=resultados, configuracion=configuracion)
        
        dispatcher.dispatch(evento, context)
        
        # Verificar que se procesó correctamente
        assert context.resultados.obtener_inventario() == 5  # 10 - 5
        assert context.resultados.ingresos == 500.0  # 5 * 100
    
    def test_dispatch_llegada_pedido_event(self):
        dispatcher = EventDispatcher([
            DemandaEventHandler(),
            LlegadaPedidoEventHandler()
        ])
        
        evento = EventoLlegadaPedido(10, 15)
        resultados = ResultadosPolitica(r=10, Q=20, inventario=5)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(resultados=resultados, configuracion=configuracion)
        
        dispatcher.dispatch(evento, context)
        
        # Verificar que se procesó correctamente
        assert context.resultados.obtener_inventario() == 20  # 5 + 15
    
    def test_dispatch_unknown_event_raises_error(self):
        dispatcher = EventDispatcher([
            DemandaEventHandler(),
            LlegadaPedidoEventHandler()
        ])
        
        # Crear un evento desconocido (mock)
        class EventoDesconocido:
            pass
        
        evento = EventoDesconocido()
        resultados = ResultadosPolitica(r=10, Q=20, inventario=5)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(resultados=resultados, configuracion=configuracion)
        
        with pytest.raises(ValueError, match="No se encontró handler para el evento"):
            dispatcher.dispatch(evento, context) 