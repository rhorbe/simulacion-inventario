import pytest
from api.src.application.command_bus import CommandBus
from api.src.application.commands.simular_command import SimularCommand
from api.src.application.handlers.simular_command_handler import SimularCommandHandler
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion


class TestCommandBus:
    """Tests para el bus de comandos"""
    
    def test_register_handler(self):
        """Test que verifica que se puede registrar un handler"""
        bus = CommandBus()
        handler = SimularCommandHandler()
        
        bus.register_handler(SimularCommand, handler)
        
        # Verificar que el handler está registrado
        assert SimularCommand in bus._handlers
        assert bus._handlers[SimularCommand] == handler
    
    def test_execute_command_with_registered_handler(self):
        """Test que verifica que se puede ejecutar un comando con handler registrado"""
        bus = CommandBus()
        handler = SimularCommandHandler()
        bus.register_handler(SimularCommand, handler)
        
        # Crear comando de prueba
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
        command = SimularCommand(politicas=[politica], configuracion=configuracion)
        
        # Ejecutar comando
        resultados = bus.execute(command)
        
        # Verificar que se retornan resultados
        assert isinstance(resultados, list)
        assert len(resultados) == 1
        assert "r" in resultados[0]
        assert "Q" in resultados[0]
        assert "ganancia" in resultados[0]
    
    def test_execute_command_without_handler_raises_error(self):
        """Test que verifica que se lanza error si no hay handler registrado"""
        bus = CommandBus()
        
        # Crear comando sin registrar handler
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
        command = SimularCommand(politicas=[politica], configuracion=configuracion)
        
        # Verificar que se lanza error
        with pytest.raises(ValueError, match="No handler registrado para"):
            bus.execute(command)
    
    def test_execute_multiple_policies(self):
        """Test que verifica que se pueden ejecutar múltiples políticas"""
        bus = CommandBus()
        handler = SimularCommandHandler()
        bus.register_handler(SimularCommand, handler)
        
        # Crear múltiples políticas
        politica1 = PoliticaInventario.from_valores(punto_reorden=10, cantidad_pedido=50)
        politica2 = PoliticaInventario.from_valores(punto_reorden=20, cantidad_pedido=100)
        
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
        command = SimularCommand(politicas=[politica1, politica2], configuracion=configuracion)
        
        # Ejecutar comando
        resultados = bus.execute(command)
        
        # Verificar que se retornan resultados para ambas políticas
        assert isinstance(resultados, list)
        assert len(resultados) == 2
        assert resultados[0]["r"] == 10
        assert resultados[0]["Q"] == 50
        assert resultados[1]["r"] == 20
        assert resultados[1]["Q"] == 100 