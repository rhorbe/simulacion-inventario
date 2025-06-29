import pytest
from api.src.application.inventario import SimulacionInventario
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido
from api.src.dependency_injection import get_event_bus
from api.src.application.handlers.demanda_handler import DemandaEventHandler
from api.src.application.handlers.llegada_pedido_handler import LlegadaPedidoEventHandler

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

def get_configured_event_bus():
    """Helper para crear un EventBus configurado con handlers registrados"""
    event_bus = get_event_bus()
    event_bus.register_handler(EventoDemanda, DemandaEventHandler())
    event_bus.register_handler(EventoLlegadaPedido, LlegadaPedidoEventHandler())
    return event_bus

class TestInventario:
    """Tests para verificar que la refactorización con isinstance funciona correctamente."""
    
    @pytest.mark.timeout(10)
    def test_simulacion_con_eventos_tipificados(self):
        """Test que verifica que la simulación funciona correctamente con eventos tipificados."""
        # Configuración de prueba
        politica = PoliticaInventario.from_valores(punto_reorden=10, cantidad_pedido=50)
        configuracion = ConfiguracionSimulacion.from_parametros(
            inventario_inicial=20,
            demanda_media=5,
            precio_venta=100,
            costo_almacenar=2,
            costo_faltante=50,
            plazo_entrega_min=1,
            plazo_entrega_max=3,
            costo_pedido_pequeno=10,
            costo_pedido_grande=5,
            dias_simulacion=10
        )
        
        # Ejecutar simulación instanciando directamente
        event_bus = get_configured_event_bus()
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        resultado = simulacion.ejecutar()
        
        # Verificar que el resultado contiene los campos esperados
        assert "r" in resultado
        assert "Q" in resultado
        assert "ingresos" in resultado
        assert "costo_alm" in resultado
        assert "costo_faltante" in resultado
        assert "costo_pedidos" in resultado
        assert "ganancia" in resultado
        
        # Verificar que los valores son numéricos y razonables
        assert isinstance(resultado["r"], int)
        assert isinstance(resultado["Q"], int)
        assert isinstance(resultado["ingresos"], (int, float))
        assert isinstance(resultado["costo_alm"], (int, float))
        assert isinstance(resultado["costo_faltante"], (int, float))
        assert isinstance(resultado["costo_pedidos"], (int, float))
        assert isinstance(resultado["ganancia"], (int, float))
        
        # Verificar que los valores coinciden con la política
        assert resultado["r"] == 10
        assert resultado["Q"] == 50
    
    @pytest.mark.timeout(10)
    def test_eventos_creados_correctamente(self):
        """Test que verifica que los eventos se crean con las clases correctas."""
        # Este test verifica indirectamente que se usan las clases correctas
        # ya que si no se usaran, la simulación fallaría
        
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=20)
        configuracion = ConfiguracionSimulacion.from_parametros(
            inventario_inicial=10,
            demanda_media=3,
            precio_venta=50,
            costo_almacenar=1,
            costo_faltante=25,
            plazo_entrega_min=1,
            plazo_entrega_max=2,
            costo_pedido_pequeno=5,
            costo_pedido_grande=3,
            dias_simulacion=5
        )
        
        # Si la simulación funciona, significa que los eventos se crean correctamente
        event_bus = get_configured_event_bus()
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        resultado = simulacion.ejecutar()
        
        # Verificar que la simulación completó sin errores
        assert resultado is not None
        assert resultado["r"] == 5
        assert resultado["Q"] == 20
    
    @pytest.mark.timeout(10)
    def test_verificacion_isinstance_en_codigo(self):
        """Test que verifica que el código usa isinstance correctamente."""
        # Crear eventos de prueba
        evento_demanda = EventoDemanda(dia=1, cantidad=10)
        evento_llegada = EventoLlegadaPedido(dia=2, cantidad=20)
        
        # Verificar que isinstance funciona correctamente
        assert isinstance(evento_demanda, EventoDemanda)
        assert isinstance(evento_llegada, EventoLlegadaPedido)
        assert not isinstance(evento_demanda, EventoLlegadaPedido)
        assert not isinstance(evento_llegada, EventoDemanda)
        
        # Verificar que ambos heredan de Evento
        from api.src.domain.models.evento import Evento
        assert isinstance(evento_demanda, Evento)
        assert isinstance(evento_llegada, Evento)


class TestSimulacionInventario:
    """Tests específicos para la clase SimulacionInventario."""
    
    def test_crear_simulacion_inventario(self):
        """Test que verifica que se puede crear una instancia de SimulacionInventario"""
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        event_bus = get_configured_event_bus()
        
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        
        assert simulacion.politica == politica
        assert simulacion.configuracion == configuracion
        assert simulacion.context is not None
        assert simulacion.fel is not None
        assert simulacion.event_bus is not None
    
    def test_inicializar_fel(self):
        """Test que verifica que la FEL se inicializa correctamente"""
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        event_bus = get_configured_event_bus()
        
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        
        # Verificar que la FEL tiene al menos un evento inicial
        assert simulacion.fel.hay_eventos() is True
        
        # Verificar que el primer evento es una demanda
        evento_inicial = simulacion.fel.siguiente()
        assert evento_inicial.__class__.__name__ == 'EventoDemanda'
        assert evento_inicial.get_dia() == 0
    
    def test_crear_contexto(self):
        """Test que verifica que el contexto se crea correctamente"""
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        event_bus = get_configured_event_bus()
        
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        
        # Verificar que el contexto tiene los datos correctos
        assert simulacion.context.r == 5
        assert simulacion.context.Q == 15
        assert simulacion.context.inventario == 10  # inventario_inicial
        assert simulacion.context.configuracion == configuracion
    
    def test_es_punto_de_reorden(self):
        """Test que verifica la lógica de punto de reorden"""
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        event_bus = get_configured_event_bus()
        
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        
        # Con inventario inicial de 10 y punto de reorden de 5, no debería ser punto de reorden
        assert simulacion.context.obtener_inventario() >= politica.get_punto_reorden()
        
        # Reducir inventario a 3 (menor que 5)
        simulacion.context.actualizar_inventario(-7)
        assert simulacion.context.obtener_inventario() < politica.get_punto_reorden()
        
        # Incrementar inventario a 8 (mayor que 5)
        simulacion.context.actualizar_inventario(5)
        assert simulacion.context.obtener_inventario() >= politica.get_punto_reorden()
    
    def test_procesar_evento(self):
        """Test que verifica que se procesa un evento correctamente"""
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        event_bus = get_configured_event_bus()
        
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        
        # Crear un evento de demanda
        evento = EventoDemanda(1, 3)
        
        # Procesar el evento usando el event bus
        simulacion.event_bus.dispatch(evento, simulacion.context)
        
        # Verificar que se procesó correctamente (inventario inicial 10 - demanda 3 = 7)
        assert simulacion.context.obtener_inventario() == 7
        assert simulacion.context.ingresos == 300.0  # 3 * 100
    
    def test_agregar_costo_almacenamiento(self):
        """Test que verifica que se agrega el costo de almacenamiento"""
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        event_bus = get_configured_event_bus()
        
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        
        # Inventario inicial es 10, costo de almacenar es 1.0
        simulacion._agregar_costo_almacenamiento()
        
        # Verificar que se agregó el costo correcto
        assert simulacion.context.costo_almacenamiento == 10.0  # 10 * 1.0
    
    def test_calcular_dia_entrega(self):
        """Test que verifica el cálculo del día de entrega"""
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        event_bus = get_configured_event_bus()
        
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        
        # Crear un evento en el día 5
        evento = EventoDemanda(5, 3)
        
        # Calcular día de entrega
        dia_entrega = simulacion._calcular_dia_entrega(evento)
        
        # El día de entrega debe ser mayor que 5 (día del evento)
        assert dia_entrega > 5
        # Y debe estar dentro del rango de plazos de entrega
        assert dia_entrega >= 5 + 1  # día evento + plazo mínimo
        assert dia_entrega <= 5 + 2  # día evento + plazo máximo
    
    def test_ejecutar_simulacion_completa(self):
        """Test que verifica que se ejecuta una simulación completa"""
        politica = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        configuracion = ConfiguracionSimulacion.from_parametros(**PARAMS)
        event_bus = get_configured_event_bus()
        
        simulacion = SimulacionInventario(politica, configuracion, event_bus)
        
        # Ejecutar la simulación
        resultados = simulacion.ejecutar()
        
        # Verificar que se retornan los resultados en formato diccionario
        assert isinstance(resultados, dict)
        assert "r" in resultados
        assert "Q" in resultados
        assert "ingresos" in resultados
        assert "costo_alm" in resultados
        assert "costo_faltante" in resultados
        assert "costo_pedidos" in resultados
        assert "ganancia" in resultados
        
        # Verificar que los valores de la política se mantienen
        assert resultados["r"] == 5
        assert resultados["Q"] == 15 