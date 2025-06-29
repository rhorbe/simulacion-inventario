import pytest
from api.src.application.handlers.demanda_handler import DemandaEventHandler
from api.src.application.handlers.llegada_pedido_handler import LlegadaPedidoEventHandler
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido
from api.src.domain.models.resultados_politica import ResultadosPolitica
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

class TestDemandaEventHandler:
    
    def test_can_handle_demanda_event(self):
        handler = DemandaEventHandler()
        evento = EventoDemanda(10, 5)
        
        assert handler.can_handle(evento) is True
    
    def test_cannot_handle_llegada_pedido_event(self):
        handler = DemandaEventHandler()
        evento = EventoLlegadaPedido(10, 5)
        
        assert handler.can_handle(evento) is False
    
    def test_handle_demanda_with_sufficient_inventory(self):
        handler = DemandaEventHandler()
        evento = EventoDemanda(10, 5)  # Demanda de 5 unidades
        resultados = ResultadosPolitica(r=10, Q=20, inventario=10)  # Inventario inicial de 10
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(resultados=resultados, configuracion=configuracion)
        
        handler.handle(evento, context)
        
        # Se vendieron 5 unidades (min entre demanda 5 e inventario 10)
        assert context.resultados.obtener_inventario() == 5  # 10 - 5
        assert context.resultados.ingresos == 500.0  # 5 * 100
        assert context.resultados.costo_total_faltante == 0.0  # No hay faltante
    
    def test_handle_demanda_with_insufficient_inventory(self):
        handler = DemandaEventHandler()
        evento = EventoDemanda(10, 8)  # Demanda de 8 unidades
        resultados = ResultadosPolitica(r=10, Q=20, inventario=3)  # Inventario inicial de 3
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(resultados=resultados, configuracion=configuracion)
        
        handler.handle(evento, context)
        
        # Se vendieron 3 unidades (min entre demanda 8 e inventario 3)
        assert context.resultados.obtener_inventario() == 0  # 3 - 3
        assert context.resultados.ingresos == 300.0  # 3 * 100
        assert context.resultados.costo_total_faltante == 250.0  # 5 faltantes * 50


class TestLlegadaPedidoEventHandler:
    
    def test_can_handle_llegada_pedido_event(self):
        handler = LlegadaPedidoEventHandler()
        evento = EventoLlegadaPedido(10, 5)
        
        assert handler.can_handle(evento) is True
    
    def test_cannot_handle_demanda_event(self):
        handler = LlegadaPedidoEventHandler()
        evento = EventoDemanda(10, 5)
        
        assert handler.can_handle(evento) is False
    
    def test_handle_llegada_pedido(self):
        handler = LlegadaPedidoEventHandler()
        evento = EventoLlegadaPedido(10, 15)  # Llegan 15 unidades
        resultados = ResultadosPolitica(r=10, Q=20, inventario=5)  # Inventario inicial de 5
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        context = SimulationContext(resultados=resultados, configuracion=configuracion)
        
        handler.handle(evento, context)
        
        # El inventario se incrementa en 15 unidades
        assert context.resultados.obtener_inventario() == 20  # 5 + 15 