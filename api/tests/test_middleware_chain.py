import pytest
import asyncio
from api.src.domain.bus.middleware import Middleware, MiddlewareContext, MiddlewareChain

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
    
    def test_middleware_can_modify_context(self):
        """Test que verifica que los middlewares pueden modificar el contexto"""
        chain = MiddlewareChain()
        
        class ContextModifyingMiddleware(Middleware):
            async def process(self, context, next_middleware):
                context.metadata["modified"] = True
                result = await next_middleware(context)
                return result
        
        middleware = ContextModifyingMiddleware()
        chain.add_middleware(middleware)
        
        async def test_handler(command):
            return "success"
        
        async def test():
            result = await chain.execute("test", test_handler)
            assert result == "success"
        
        asyncio.run(test())
    
    def test_middleware_can_handle_errors(self):
        """Test que verifica que los middlewares pueden manejar errores"""
        chain = MiddlewareChain()
        
        class ErrorHandlingMiddleware(Middleware):
            def __init__(self):
                self.error_caught = False
            
            async def process(self, context, next_middleware):
                try:
                    result = await next_middleware(context)
                    return result
                except ValueError as e:
                    self.error_caught = True
                    return f"Error handled: {str(e)}"
        
        middleware = ErrorHandlingMiddleware()
        chain.add_middleware(middleware)
        
        async def failing_handler(command):
            raise ValueError("Test error")
        
        async def test():
            result = await chain.execute("test", failing_handler)
            assert result == "Error handled: Test error"
            assert middleware.error_caught
        
        asyncio.run(test()) 