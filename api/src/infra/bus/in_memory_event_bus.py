from typing import Dict, Type, Any, List
from api.src.domain.bus.event_bus import EventBus, EventHandler
from api.src.domain.bus.middleware import Middleware, MiddlewareChain
from api.src.domain.models.evento import Evento
from api.src.domain.models.simulation_context import SimulationContext
import asyncio


class InMemoryEventBus(EventBus):
    """Implementación en memoria del bus de eventos con soporte para middlewares"""
    
    def __init__(self):
        self._handlers: Dict[Type[Evento], EventHandler] = {}
        self._middleware_chain = MiddlewareChain()
    
    def register_handler(self, event_type: Type[Evento], handler: EventHandler) -> None:
        """
        Registra un handler para un tipo de evento específico
        
        Args:
            event_type: Tipo de evento
            handler: Handler que procesará el evento
        """
        self._handlers[event_type] = handler
    
    def dispatch(self, evento: Evento, context: SimulationContext) -> None:
        """
        Ejecuta el handler apropiado para el evento a través de la cadena de middlewares
        
        Args:
            evento: Evento a procesar
            context: Contexto de simulación
            
        Raises:
            ValueError: Si no hay handler registrado para el tipo de evento
        """
        event_type = type(evento)
        
        if event_type not in self._handlers:
            raise ValueError(f"No se encontró handler para el evento: {event_type.__name__}")
        
        handler = self._handlers[event_type]
        
        # Si no hay middlewares, ejecutar directamente
        if not self._middleware_chain.middlewares:
            handler.handle(evento, context)
            return
        
        # Ejecutar a través de la cadena de middlewares
        async def async_dispatch():
            async def final_handler(event):
                handler.handle(event, context)
                return None
            
            return await self._middleware_chain.execute(evento, final_handler)
        
        # Ejecutar de forma síncrona (para mantener compatibilidad)
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Si ya hay un loop corriendo, crear uno nuevo
                asyncio.run(async_dispatch())
            else:
                loop.run_until_complete(async_dispatch())
        except RuntimeError:
            # Si no hay loop, crear uno nuevo
            asyncio.run(async_dispatch())
    
    def add_middleware(self, middleware: Middleware) -> None:
        """Agrega un middleware al bus"""
        self._middleware_chain.add_middleware(middleware)
    
    def get_middlewares(self) -> List[Middleware]:
        """Retorna la lista de middlewares configurados"""
        return self._middleware_chain.middlewares.copy() 