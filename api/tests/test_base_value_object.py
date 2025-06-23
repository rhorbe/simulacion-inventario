import pytest
from api.src.domain.value_objects import BaseValueObject, Cantidad, Precio, PoliticaInventario
from api.src.domain.exceptions import DomainError
from api.src.domain.repository.config import Config
from api.src.infra.repository.yml_config_repository import YmlConfigRepository


class TestBaseValueObject:
    def test_with_config_method(self):
        """Test que verifica que el método with_config funciona correctamente."""
        config = YmlConfigRepository()
        
        # Configurar Cantidad con valores por defecto
        CantidadConConfig = Cantidad.with_config(config)
        
        # Verificar que la configuración se estableció
        assert CantidadConConfig.get_default_config() == config
        
        # Limpiar configuración
        CantidadConConfig.clear_default_config()
        assert CantidadConConfig.get_default_config() is None
    
    def test_multiple_value_objects_with_same_config(self):
        """Test que verifica que múltiples Value Objects pueden usar la misma configuración."""
        config = YmlConfigRepository()
        
        # Configurar múltiples Value Objects
        CantidadConConfig = Cantidad.with_config(config)
        PrecioConConfig = Precio.with_config(config)
        PoliticaConConfig = PoliticaInventario.with_config(config)
        
        # Verificar que todos tienen la misma configuración
        assert CantidadConConfig.get_default_config() == config
        assert PrecioConConfig.get_default_config() == config
        assert PoliticaConConfig.get_default_config() == config
        
        # Limpiar configuraciones
        CantidadConConfig.clear_default_config()
        PrecioConConfig.clear_default_config()
        PoliticaConConfig.clear_default_config()
    
    def test_clear_default_config(self):
        """Test que verifica que clear_default_config funciona correctamente."""
        config = YmlConfigRepository()
        
        # Configurar y luego limpiar
        CantidadConConfig = Cantidad.with_config(config)
        assert CantidadConConfig.get_default_config() == config
        
        CantidadConConfig.clear_default_config()
        assert CantidadConConfig.get_default_config() is None
    
    def test_value_objects_still_work_without_config(self):
        """Test que verifica que los Value Objects siguen funcionando sin configuración."""
        # Crear Value Objects sin configuración
        cantidad = Cantidad.from_int(10)
        precio = Precio.from_float(5.5)
        politica = PoliticaInventario.from_valores(20, 100)
        
        # Verificar que funcionan correctamente
        assert int(cantidad) == 10
        assert float(precio) == 5.5
        assert politica.get_punto_reorden() == 20
        assert politica.get_cantidad_pedido() == 100 