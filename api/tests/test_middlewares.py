import pytest
import asyncio
from api.src.domain.bus.middleware import Middleware, MiddlewareContext, MiddlewareChain
from api.src.infra.bus.middlewares import (
    LoggingMiddleware, 
    TimingMiddleware, 
    MetricsMiddleware, 
    ValidationMiddleware,
    CachingMiddleware,
    RetryMiddleware
)
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido

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

class TestLoggingMiddleware:
    """Tests para el middleware de logging"""
    
    def test_logging_middleware_logs_success(self, caplog):
        """Test que verifica que el logging middleware registra éxitos"""
        middleware = LoggingMiddleware()
        
        async def test_handler(command):
            return "success"
        
        async def test():
            await middleware.process(
                MiddlewareContext(command_or_event="test_command"), 
                test_handler
            )
        
        asyncio.run(test())
        
        # Verificar que se registraron los logs
        assert "🔄 Procesando" in caplog.text
        assert "✅ test_command procesado exitosamente" in caplog.text
    
    def test_logging_middleware_logs_errors(self, caplog):
        """Test que verifica que el logging middleware registra errores"""
        middleware = LoggingMiddleware()
        
        async def test_handler(command):
            raise ValueError("Test error")
        
        async def test():
            try:
                await middleware.process(
                    MiddlewareContext(command_or_event="test_command"), 
                    test_handler
                )
            except ValueError:
                pass
        
        asyncio.run(test())
        
        # Verificar que se registraron los logs de error
        assert "🔄 Procesando" in caplog.text
        assert "❌ Error procesando" in caplog.text

class TestTimingMiddleware:
    """Tests para el middleware de timing"""
    
    def test_timing_middleware_measures_execution_time(self, caplog):
        """Test que verifica que el timing middleware mide el tiempo de ejecución"""
        middleware = TimingMiddleware()
        
        async def test_handler(command):
            import asyncio
            await asyncio.sleep(0.01)  # Simular trabajo
            return "success"
        
        async def test():
            await middleware.process(
                MiddlewareContext(command_or_event="test_command"), 
                test_handler
            )
        
        asyncio.run(test())
        
        # Verificar que se registró el tiempo
        assert "⏱️ test_command ejecutado en" in caplog.text

class TestMetricsMiddleware:
    """Tests para el middleware de métricas"""
    
    def test_metrics_middleware_collects_metrics(self):
        """Test que verifica que el metrics middleware recolecta métricas"""
        middleware = MetricsMiddleware()
        
        async def success_handler(command):
            return "success"
        
        async def error_handler(command):
            raise ValueError("Test error")
        
        async def test():
            # Ejecutar handler exitoso
            await middleware.process(
                MiddlewareContext(command_or_event="TestCommand"), 
                success_handler
            )
            
            # Ejecutar handler con error
            try:
                await middleware.process(
                    MiddlewareContext(command_or_event="TestCommand"), 
                    error_handler
                )
            except ValueError:
                pass
        
        asyncio.run(test())
        
        metrics = middleware.get_metrics()
        assert metrics['total_processed'] == 2
        assert metrics['successful'] == 1
        assert metrics['failed'] == 1
        assert 'TestCommand' in metrics['by_type']
        assert metrics['by_type']['TestCommand']['total'] == 2
        assert metrics['by_type']['TestCommand']['successful'] == 1
        assert metrics['by_type']['TestCommand']['failed'] == 1

class TestValidationMiddleware:
    """Tests para el middleware de validación"""
    
    def test_validation_middleware_validates_events(self, caplog):
        """Test que verifica que el validation middleware valida eventos"""
        middleware = ValidationMiddleware()
        
        # Evento válido
        valid_event = EventoDemanda(dia=1, cantidad=10)
        
        async def test_handler(event):
            return "success"
        
        async def test():
            await middleware.process(
                MiddlewareContext(command_or_event=valid_event), 
                test_handler
            )
        
        asyncio.run(test())
        
        # Verificar que se registró la validación exitosa
        assert "✅ EventoDemanda validado correctamente" in caplog.text
    
    def test_validation_middleware_rejects_invalid_events(self):
        """Test que verifica que el validation middleware rechaza eventos inválidos"""
        middleware = ValidationMiddleware()
        
        # Evento inválido (día negativo)
        invalid_event = EventoDemanda(dia=-1, cantidad=10)
        
        async def test_handler(event):
            return "success"
        
        async def test():
            with pytest.raises(ValueError, match="Día inválido"):
                await middleware.process(
                    MiddlewareContext(command_or_event=invalid_event), 
                    test_handler
                )
        
        asyncio.run(test())

class TestCachingMiddleware:
    """Tests para el middleware de cache"""
    
    def test_caching_middleware_caches_results(self, caplog):
        """Test que verifica que el caching middleware cachea resultados"""
        middleware = CachingMiddleware()
        
        call_count = 0
        
        async def test_handler(command):
            nonlocal call_count
            call_count += 1
            return f"result_{call_count}"
        
        async def test():
            # Primera llamada - debe ejecutar el handler
            result1 = await middleware.process(
                MiddlewareContext(command_or_event="test_command"), 
                test_handler
            )
            
            # Segunda llamada - debe usar cache
            result2 = await middleware.process(
                MiddlewareContext(command_or_event="test_command"), 
                test_handler
            )
            
            assert result1 == "result_1"
            assert result2 == "result_1"  # Mismo resultado del cache
            assert call_count == 1  # Handler solo se llamó una vez
        
        asyncio.run(test())
        
        # Verificar logs de cache
        assert "💾 Resultado cacheado" in caplog.text
        assert "💾 Resultado obtenido del cache" in caplog.text

class TestRetryMiddleware:
    """Tests para el middleware de reintentos"""
    
    def test_retry_middleware_retries_on_failure(self, caplog):
        """Test que verifica que el retry middleware reintenta en caso de fallo"""
        middleware = RetryMiddleware(max_retries=2, delay=0.01)
        
        call_count = 0
        
        async def failing_handler(command):
            nonlocal call_count
            call_count += 1
            if call_count < 3:  # Falla las primeras 2 veces
                raise ValueError("Temporary failure")
            return "success"
        
        async def test():
            result = await middleware.process(
                MiddlewareContext(command_or_event="test_command"), 
                failing_handler
            )
            
            assert result == "success"
            assert call_count == 3  # Se llamó 3 veces (2 fallos + 1 éxito)
        
        asyncio.run(test())
        
        # Verificar logs de reintentos
        assert "🔄 Reintento" in caplog.text
    
    def test_retry_middleware_gives_up_after_max_retries(self, caplog):
        """Test que verifica que el retry middleware se rinde después del máximo de reintentos"""
        middleware = RetryMiddleware(max_retries=2, delay=0.01)
        
        async def always_failing_handler(command):
            raise ValueError("Always fails")
        
        async def test():
            with pytest.raises(ValueError, match="Always fails"):
                await middleware.process(
                    MiddlewareContext(command_or_event="test_command"), 
                    always_failing_handler
                )
        
        asyncio.run(test())
        
        # Verificar logs de agotamiento de reintentos
        assert "❌ Agotados los reintentos" in caplog.text 