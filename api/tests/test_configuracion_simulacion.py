import pytest
from api.src.domain.value_objects import ConfiguracionSimulacion
from api.src.domain.exceptions import DomainError


class TestConfiguracionSimulacion:
    def test_configuracion_valida(self):
        config = ConfiguracionSimulacion.from_parametros(
            inventario_inicial=100,
            precio_venta=10.0,
            costo_almacenar=0.5,
            costo_faltante=5.0,
            costo_pedido_pequeno=12.0,
            costo_pedido_grande=10.0,
            plazo_entrega_min=1,
            plazo_entrega_max=5,
            demanda_media=20
        )
        
        assert config.get_inventario_inicial() == 100
        assert config.get_precio_venta() == 10.0
        assert config.get_costo_almacenar() == 0.5
        assert config.get_costo_faltante() == 5.0
        assert config.get_costo_pedido_pequeno() == 12.0
        assert config.get_costo_pedido_grande() == 10.0
        assert config.get_plazo_entrega_min() == 1
        assert config.get_plazo_entrega_max() == 5
        assert config.get_demanda_media() == 20
        
        # Probar cálculo de costo unitario
        assert config.calcular_costo_unitario_pedido(100) == 12.0  # Pedido pequeño
        assert config.calcular_costo_unitario_pedido(400) == 10.0  # Pedido grande
    
    def test_configuracion_con_precio_negativo_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El precio no puede ser negativo"):
            ConfiguracionSimulacion.from_parametros(
                inventario_inicial=100,
                precio_venta=-10.0,
                costo_almacenar=0.5,
                costo_faltante=5.0,
                costo_pedido_pequeno=12.0,
                costo_pedido_grande=10.0,
                plazo_entrega_min=1,
                plazo_entrega_max=5,
                demanda_media=20
            ) 