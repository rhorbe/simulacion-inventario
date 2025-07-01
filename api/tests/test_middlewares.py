import pytest
import asyncio
from api.src.domain.bus.middleware import Middleware, MiddlewareContext, MiddlewareChain
# from api.src.infra.bus.middlewares import LoggingMiddleware
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido
from api.src.domain.models.command import SimularCommand
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion, DiasSimulacion, DemandaMedia, PlazoDeEntrega, CostoPedido, CostoAlmacenar, CostoFaltante, PrecioVenta, InventarioInicial

class TestMiddlewareChain:
    """Tests para la cadena de middlewares"""
    
    def test_empty_chain_executes_handler_directly(self):
        """Test que verifica que una cadena vacía ejecuta el handler directamente"""
        chain = MiddlewareChain()
        
        async def test_handler(command):
            return f"Processed: {command}"
        
        async def test():
            result = await chain.execute("test_command", test_handler)
            assert result == "Processed: test_command"
        
        asyncio.run(test())
    
    def test_single_middleware(self):
        """Test que verifica que un middleware único funciona correctamente"""
        chain = MiddlewareChain()
        
        class TestMiddleware(Middleware):
            def __init__(self):
                self.processed = False
            
            async def process(self, context, next_middleware):
                self.processed = True
                result = await next_middleware(context)
                return f"Middleware: {result}"
        
        middleware = TestMiddleware()
        chain.add_middleware(middleware)
        
        async def test_handler(command):
            return f"Handler: {command}"
        
        async def test():
            result = await chain.execute("test", test_handler)
            assert result == "Middleware: Handler: test"
            assert middleware.processed
        
        asyncio.run(test())
    
    def test_multiple_middlewares(self):
        """Test que verifica que múltiples middlewares se ejecutan en orden"""
        chain = MiddlewareChain()
        
        class TestMiddleware(Middleware):
            def __init__(self, name):
                self.name = name
            
            async def process(self, context, next_middleware):
                result = await next_middleware(context)
                return f"{self.name}({result})"
        
        chain.add_middleware(TestMiddleware("A"))
        chain.add_middleware(TestMiddleware("B"))
        chain.add_middleware(TestMiddleware("C"))
        
        async def test_handler(command):
            return "HANDLER"
        
        async def test():
            result = await chain.execute("test", test_handler)
            assert result == "A(B(C(HANDLER)))"
        
        asyncio.run(test()) 