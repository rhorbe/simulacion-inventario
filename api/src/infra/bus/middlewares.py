import time
import logging
from typing import Any, Callable
from api.src.domain.bus.middleware import Middleware, MiddlewareContext

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(Middleware):
    """Middleware para logging de comandos y eventos"""
    
    async def process(self, context: MiddlewareContext, next_middleware: Callable) -> Any:
        command_or_event = context.command_or_event
        event_type = command_or_event.__class__.__name__
        
        logger.info(f"🔄 Procesando {event_type}: {command_or_event}")
        
        try:
            result = await next_middleware(context)
            logger.info(f"✅ {event_type} procesado exitosamente")
            return result
        except Exception as e:
            logger.error(f"❌ Error procesando {event_type}: {str(e)}")
            raise

class TimingMiddleware(Middleware):
    """Middleware para medir el tiempo de ejecución"""
    
    async def process(self, context: MiddlewareContext, next_middleware: Callable) -> Any:
        start_time = time.time()
        event_type = context.command_or_event.__class__.__name__
        
        try:
            result = await next_middleware(context)
            execution_time = time.time() - start_time
            logger.info(f"⏱️ {event_type} ejecutado en {execution_time:.4f} segundos")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"⏱️ {event_type} falló después de {execution_time:.4f} segundos")
            raise

class MetricsMiddleware(Middleware):
    """Middleware para recolectar métricas"""
    
    def __init__(self):
        self.metrics = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'by_type': {}
        }
    
    async def process(self, context: MiddlewareContext, next_middleware: Callable) -> Any:
        event_type = context.command_or_event.__class__.__name__
        
        # Actualizar métricas
        self.metrics['total_processed'] += 1
        if event_type not in self.metrics['by_type']:
            self.metrics['by_type'][event_type] = {
                'total': 0,
                'successful': 0,
                'failed': 0
            }
        self.metrics['by_type'][event_type]['total'] += 1
        
        try:
            result = await next_middleware(context)
            self.metrics['successful'] += 1
            self.metrics['by_type'][event_type]['successful'] += 1
            return result
        except Exception as e:
            self.metrics['failed'] += 1
            self.metrics['by_type'][event_type]['failed'] += 1
            raise
    
    def get_metrics(self) -> dict:
        """Retorna las métricas recolectadas"""
        return self.metrics.copy()

class ValidationMiddleware(Middleware):
    """Middleware para validación de comandos y eventos"""
    
    async def process(self, context: MiddlewareContext, next_middleware: Callable) -> Any:
        command_or_event = context.command_or_event
        event_type = command_or_event.__class__.__name__
        
        # Validaciones básicas
        if hasattr(command_or_event, 'get_dia') and command_or_event.get_dia() < 0:
            raise ValueError(f"Día inválido en {event_type}: {command_or_event.get_dia()}")
        
        if hasattr(command_or_event, 'get_cantidad') and command_or_event.get_cantidad() <= 0:
            raise ValueError(f"Cantidad inválida en {event_type}: {command_or_event.get_cantidad()}")
        
        logger.info(f"✅ {event_type} validado correctamente")
        return await next_middleware(context)

class CachingMiddleware(Middleware):
    """Middleware para cache de resultados"""
    
    def __init__(self):
        self.cache = {}
    
    async def process(self, context: MiddlewareContext, next_middleware: Callable) -> Any:
        command_or_event = context.command_or_event
        cache_key = self._generate_cache_key(command_or_event)
        
        # Verificar cache
        if cache_key in self.cache:
            logger.info(f"💾 Resultado obtenido del cache para {command_or_event.__class__.__name__}")
            return self.cache[cache_key]
        
        # Ejecutar y cachear
        result = await next_middleware(context)
        self.cache[cache_key] = result
        logger.info(f"💾 Resultado cacheado para {command_or_event.__class__.__name__}")
        
        return result
    
    def _generate_cache_key(self, command_or_event: Any) -> str:
        """Genera una clave única para el cache"""
        return f"{command_or_event.__class__.__name__}_{hash(str(command_or_event))}"
    
    def clear_cache(self) -> None:
        """Limpia el cache"""
        self.cache.clear()
        logger.info("🗑️ Cache limpiado")

class RetryMiddleware(Middleware):
    """Middleware para reintentos automáticos"""
    
    def __init__(self, max_retries: int = 3, delay: float = 0.1):
        self.max_retries = max_retries
        self.delay = delay
    
    async def process(self, context: MiddlewareContext, next_middleware: Callable) -> Any:
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await next_middleware(context)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    logger.warning(f"🔄 Reintento {attempt + 1}/{self.max_retries} para {context.command_or_event.__class__.__name__}")
                    await self._delay()
                else:
                    logger.error(f"❌ Agotados los reintentos para {context.command_or_event.__class__.__name__}")
        
        raise last_exception
    
    async def _delay(self) -> None:
        """Espera antes del siguiente reintento"""
        import asyncio
        await asyncio.sleep(self.delay) 