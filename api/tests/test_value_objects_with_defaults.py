import pytest
from api.src.domain.value_objects import (
    Cantidad, Precio, PlazoDeEntrega, CostoPedido, PoliticaInventario, ConfiguracionSimulacion,
    InventarioInicial, DemandaMedia, PrecioVenta, CostoAlmacenar, CostoFaltante
)
from api.src.domain.exceptions import DomainError
from api.src.domain.repository.config import Config
from api.src.infra.repository.yml_config_repository import YmlConfigRepository
import os

@pytest.fixture(autouse=True)
def reset_config_singleton():
    YmlConfigRepository._instance = None
    YmlConfigRepository._initialized = False
    yield
    YmlConfigRepository._instance = None
    YmlConfigRepository._initialized = False

class TestValueObjectsWithDefaults:
    def test_inventario_inicial_with_default(self, reset_config_singleton):
        """Test que verifica que InventarioInicial usa valor por defecto cuando se pasa None."""
        config = YmlConfigRepository()
        
        # Configurar InventarioInicial con valores por defecto
        InventarioInicialConConfig = InventarioInicial.with_config(config)
        
        # Crear InventarioInicial sin valor (debe usar valor por defecto)
        inventario = InventarioInicialConConfig.from_int(None)
        
        # Verificar que se usó el valor por defecto
        assert int(inventario) == config.get_simulacion()['inventario_inicial']
        
        # Limpiar configuración
        InventarioInicialConConfig.clear_default_config()
    
    def test_demanda_media_with_default(self, reset_config_singleton):
        """Test que verifica que DemandaMedia usa valor por defecto cuando se pasa None."""
        config = YmlConfigRepository()
        
        # Configurar DemandaMedia con valores por defecto
        DemandaMediaConConfig = DemandaMedia.with_config(config)
        
        # Crear DemandaMedia sin valor (debe usar valor por defecto)
        demanda = DemandaMediaConConfig.from_int(None)
        
        # Verificar que se usó el valor por defecto
        assert int(demanda) == config.get_simulacion()['demanda_media']
        
        # Limpiar configuración
        DemandaMediaConConfig.clear_default_config()
    
    def test_precio_venta_with_default(self, reset_config_singleton):
        """Test que verifica que PrecioVenta usa valor por defecto cuando se pasa None."""
        config = YmlConfigRepository()
        
        # Configurar PrecioVenta con valores por defecto
        PrecioVentaConConfig = PrecioVenta.with_config(config)
        
        # Crear PrecioVenta sin valor (debe usar valor por defecto)
        precio = PrecioVentaConConfig.from_float(None)
        
        # Verificar que se usó el valor por defecto
        assert float(precio) == config.get_precios()['venta']
        
        # Limpiar configuración
        PrecioVentaConConfig.clear_default_config()
    
    def test_costo_almacenar_with_default(self, reset_config_singleton):
        """Test que verifica que CostoAlmacenar usa valor por defecto cuando se pasa None."""
        config = YmlConfigRepository()
        
        # Configurar CostoAlmacenar con valores por defecto
        CostoAlmacenarConConfig = CostoAlmacenar.with_config(config)
        
        # Crear CostoAlmacenar sin valor (debe usar valor por defecto)
        costo = CostoAlmacenarConConfig.from_float(None)
        
        # Verificar que se usó el valor por defecto
        assert float(costo) == config.get_costos()['almacenar']
        
        # Limpiar configuración
        CostoAlmacenarConConfig.clear_default_config()
    
    def test_costo_faltante_with_default(self, reset_config_singleton):
        """Test que verifica que CostoFaltante usa valor por defecto cuando se pasa None."""
        config = YmlConfigRepository()
        
        # Configurar CostoFaltante con valores por defecto
        CostoFaltanteConConfig = CostoFaltante.with_config(config)
        
        # Crear CostoFaltante sin valor (debe usar valor por defecto)
        costo = CostoFaltanteConConfig.from_float(None)
        
        # Verificar que se usó el valor por defecto
        assert float(costo) == config.get_costos()['faltante']
        
        # Limpiar configuración
        CostoFaltanteConConfig.clear_default_config()
    
    def test_plazo_de_entrega_with_defaults(self, reset_config_singleton):
        """Test que verifica que PlazoDeEntrega usa valores por defecto cuando se pasan None."""
        config = YmlConfigRepository()
        
        # Configurar PlazoDeEntrega con valores por defecto
        PlazoConConfig = PlazoDeEntrega.with_config(config)
        
        # Crear PlazoDeEntrega sin valores (debe usar valores por defecto)
        plazo = PlazoConConfig.from_plazos(None, None)
        
        # Verificar que se usaron los valores por defecto
        assert plazo.get_plazo_minimo() == config.get_entrega()['plazo_min']
        assert plazo.get_plazo_maximo() == config.get_entrega()['plazo_max']
        
        # Limpiar configuración
        PlazoConConfig.clear_default_config()
    
    def test_costo_pedido_with_defaults(self, reset_config_singleton):
        """Test que verifica que CostoPedido usa valores por defecto cuando se pasan None."""
        config = YmlConfigRepository()
        
        # Configurar CostoPedido con valores por defecto
        CostoConConfig = CostoPedido.with_config(config)
        
        # Crear CostoPedido sin valores (debe usar valores por defecto)
        costo = CostoConConfig.from_costos(None, None)
        
        # Verificar que se usaron los valores por defecto
        assert costo.get_costo_pedido_pequeno() == config.get_costos()['pedido_pequeno']
        assert costo.get_costo_pedido_grande() == config.get_costos()['pedido_grande']
        
        # Limpiar configuración
        CostoConConfig.clear_default_config()
    
    def test_politica_inventario_with_defaults(self, reset_config_singleton):
        """Test que verifica que PoliticaInventario usa valores por defecto cuando se pasan None."""
        config = YmlConfigRepository()
        
        # Configurar PoliticaInventario con valores por defecto
        PoliticaConConfig = PoliticaInventario.with_config(config)
        
        # Crear PoliticaInventario sin valores (debe usar valores por defecto)
        politica = PoliticaConConfig.from_valores(None, None)
        
        # Verificar que se usaron los valores por defecto
        primera_politica = config.get_politicas_abastecimiento()[0]
        assert politica.get_punto_reorden() == primera_politica['punto_reorden']
        assert politica.get_cantidad_pedido() == primera_politica['cantidad_pedido']
        
        # Limpiar configuración
        PoliticaConConfig.clear_default_config()
    
    def test_configuracion_simulacion_with_defaults(self, reset_config_singleton):
        """Test que verifica que ConfiguracionSimulacion usa valores por defecto cuando se pasan None."""
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/infra/repository/config.yml'))
        config = YmlConfigRepository(config_path)
        ConfigConConfig = ConfiguracionSimulacion.with_config(config)
        configuracion = ConfigConConfig.from_parametros(
            inventario_inicial=None,
            precio_venta=None,
            costo_almacenar=None,
            costo_faltante=None,
            costo_pedido_pequeno=None,
            costo_pedido_grande=None,
            plazo_entrega_min=None,
            plazo_entrega_max=None,
            demanda_media=None
        )
        simulacion = config.get_simulacion()
        costos = config.get_costos()
        entrega = config.get_entrega()
        precios = config.get_precios()
        assert configuracion.get_inventario_inicial() == simulacion['inventario_inicial']
        assert configuracion.get_precio_venta() == precios['venta']
        assert configuracion.get_costo_almacenar() == costos['almacenar']
        assert configuracion.get_costo_faltante() == costos['faltante']
        assert configuracion.get_costo_pedido_pequeno() == costos['pedido_pequeno']
        assert configuracion.get_costo_pedido_grande() == costos['pedido_grande']
        assert configuracion.get_plazo_entrega_min() == entrega['plazo_min']
        assert configuracion.get_plazo_entrega_max() == entrega['plazo_max']
        assert configuracion.get_demanda_media() == simulacion['demanda_media']
        ConfigConConfig.clear_default_config()
    
    def test_mixed_values_with_defaults(self, reset_config_singleton):
        """Test que verifica que se pueden mezclar valores explícitos con valores por defecto."""
        config = YmlConfigRepository()
        
        # Configurar Value Objects con valores por defecto
        InventarioInicialConConfig = InventarioInicial.with_config(config)
        PrecioVentaConConfig = PrecioVenta.with_config(config)
        
        # Crear con valores mixtos
        inventario_explicito = InventarioInicialConConfig.from_int(100)  # Valor explícito
        precio_por_defecto = PrecioVentaConConfig.from_float(None)  # Valor por defecto
        
        # Verificar que se usaron los valores correctos
        assert int(inventario_explicito) == 100
        assert float(precio_por_defecto) == config.get_precios()['venta']
        
        # Limpiar configuraciones
        InventarioInicialConConfig.clear_default_config()
        PrecioVentaConConfig.clear_default_config()
    
    def test_error_when_no_config_and_none_value(self, reset_config_singleton):
        """Test que verifica que se lanza error cuando no hay configuración y se pasa None."""
        class DummyConfig:
            def get_simulacion(self): return {}
            def get_entrega(self): return {}
            def get_costos(self): return {}
            def get_precios(self): return {}
            def get_politicas_abastecimiento(self): return []
        InventarioInicialConConfig = InventarioInicial.with_config(DummyConfig())
        with pytest.raises(ValueError, match="No se proporcionó valor para inventario_inicial y no hay configuración por defecto"):
            InventarioInicialConConfig.from_int(None)
        InventarioInicialConConfig.clear_default_config()
    
    def test_validation_still_works_with_defaults(self, reset_config_singleton):
        """Test que verifica que las validaciones siguen funcionando con valores por defecto."""
        config = YmlConfigRepository()
        
        # Configurar con configuración inválida (precio negativo)
        config.get_precios()['venta'] = -10.0
        
        PrecioVentaConConfig = PrecioVenta.with_config(config)
        
        # Debe lanzar DomainError por precio negativo
        with pytest.raises(DomainError, match="El precio no puede ser negativo"):
            PrecioVentaConConfig.from_float(None)
        
        # Limpiar configuración
        PrecioVentaConConfig.clear_default_config() 