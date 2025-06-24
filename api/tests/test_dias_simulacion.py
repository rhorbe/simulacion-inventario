import pytest
from api.src.domain.value_objects.dias_simulacion import DiasSimulacion
from api.src.domain.exceptions.domain_error import DomainError

class TestDiasSimulacion:
    """Tests para el Value Object DiasSimulacion."""
    
    def test_dias_simulacion_valido(self):
        """Test que verifica que se puede crear un DiasSimulacion válido."""
        dias_simulacion = DiasSimulacion.from_int(30)
        
        assert dias_simulacion.get_dias() == 30
        assert str(dias_simulacion) == "Días de simulación: 30"
    
    def test_dias_simulacion_cero_levanta_excepcion(self):
        """Test que verifica que un valor de cero levanta excepción."""
        with pytest.raises(DomainError, match="Los días de simulación deben ser mayores que cero"):
            DiasSimulacion.from_int(0)
    
    def test_dias_simulacion_negativo_levanta_excepcion(self):
        """Test que verifica que un valor negativo levanta excepción."""
        with pytest.raises(DomainError, match="Los días de simulación deben ser mayores que cero"):
            DiasSimulacion.from_int(-10)
    
    def test_dias_simulacion_con_valor_por_defecto(self):
        """Test que verifica que se puede usar valor por defecto desde configuración."""
        # Simular configuración con valor por defecto
        class MockConfig:
            def get_dias_simulacion(self):
                return 100
        
        config = MockConfig()
        DiasSimulacion.with_config(config)
        
        # Crear sin especificar valor
        dias_simulacion = DiasSimulacion.from_int()
        
        assert dias_simulacion.get_dias() == 100
        
        # Limpiar configuración
        DiasSimulacion.clear_default_config()
    
    def test_dias_simulacion_sin_configuracion_y_sin_valor_levanta_excepcion(self):
        """Test que verifica que sin configuración y sin valor se levanta excepción."""
        with pytest.raises(ValueError, match="No se proporcionó valor para días de simulación y no hay configuración por defecto"):
            DiasSimulacion.from_int()
    
    def test_dias_simulacion_valor_explicito_sobrescribe_defecto(self):
        """Test que verifica que un valor explícito sobrescribe el valor por defecto."""
        # Simular configuración con valor por defecto
        class MockConfig:
            def get_dias_simulacion(self):
                return 100
        
        config = MockConfig()
        DiasSimulacion.with_config(config)
        
        # Crear con valor explícito
        dias_simulacion = DiasSimulacion.from_int(50)
        
        assert dias_simulacion.get_dias() == 50  # No usa el valor por defecto
        
        # Limpiar configuración
        DiasSimulacion.clear_default_config()
    
    def test_dias_simulacion_grandes_valores(self):
        """Test que verifica que se pueden usar valores grandes."""
        dias_simulacion = DiasSimulacion.from_int(365)
        
        assert dias_simulacion.get_dias() == 365
    
    def test_dias_simulacion_valor_uno(self):
        """Test que verifica que se puede usar el valor mínimo válido (1)."""
        dias_simulacion = DiasSimulacion.from_int(1)
        
        assert dias_simulacion.get_dias() == 1 