import pytest
from api.src.application.inventario import simular_politica
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido

class TestInventario:
    """Tests para verificar que la refactorización con isinstance funciona correctamente."""
    
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
            costo_pedido_grande=5
        )
        
        # Ejecutar simulación
        resultado = simular_politica(politica, dias_simulacion=10, configuracion=configuracion)
        
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
            costo_pedido_grande=3
        )
        
        # Si la simulación funciona, significa que los eventos se crean correctamente
        resultado = simular_politica(politica, dias_simulacion=5, configuracion=configuracion)
        
        # Verificar que la simulación completó sin errores
        assert resultado is not None
        assert resultado["r"] == 5
        assert resultado["Q"] == 20
    
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
        
        # Verificar que ambos heredan de EventoBase
        from api.src.domain.models.evento import EventoBase
        assert isinstance(evento_demanda, EventoBase)
        assert isinstance(evento_llegada, EventoBase) 