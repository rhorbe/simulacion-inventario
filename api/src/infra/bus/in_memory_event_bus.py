from typing import Dict, Type, Any, List
from api.src.domain.bus.event_bus import EventBus, EventHandler
from api.src.domain.bus.middleware import Middleware, MiddlewareChain
from api.src.domain.models.evento import Evento
from api.src.domain.models.simulation_context import SimulationContext


class InMemoryEventBus(EventBus):
    """Implementación en memoria del bus de eventos con soporte para middlewares"""
    
    def __init__(self):
        self._handlers: Dict[Type, List[EventHandler]] = {}
        self._middleware_chain = MiddlewareChain()
    
    def register_handler(self, event_type: Type, handler: EventHandler) -> None:
        """
        Registra un handler para un tipo de evento específico
        
        Args:
            event_type: Tipo de evento
            handler: Handler que procesará el evento
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    async def dispatch(self, event: Any, context: Any = None) -> None:
        """
        Ejecuta el handler apropiado para el evento a través de la cadena de middlewares
        
        Args:
            evento: Evento a procesar
            context: Contexto de simulación
            
        Raises:
            ValueError: Si no hay handler registrado para el tipo de evento
        """
        event_type = type(event)
        
        if event_type not in self._handlers:
            return
        
        handlers = self._handlers[event_type]
        
        for handler in handlers:
            if not self._middleware_chain.middlewares:
                handler.handle(event, context)
            else:
                result = await self._middleware_chain.execute(event, lambda evt: handler.handle(evt, context))
    
    def add_middleware(self, middleware: Middleware) -> None:
        """Agrega un middleware al bus"""
        self._middleware_chain.add_middleware(middleware)
    
    def get_middlewares(self) -> List[Middleware]:
        """Retorna la lista de middlewares configurados"""
        return self._middleware_chain.middlewares.copy() 