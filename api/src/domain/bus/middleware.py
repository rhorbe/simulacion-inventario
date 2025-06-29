from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Any, List
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class MiddlewareContext:
    """Contexto que se pasa entre middlewares"""
    command_or_event: T
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class Middleware(ABC, Generic[T]):
    """Interfaz base para todos los middlewares"""
    
    @abstractmethod
    async def process(self, context: MiddlewareContext, next_middleware: Callable) -> Any:
        """
        Procesa el middleware actual y llama al siguiente en la cadena.
        
        Args:
            context: Contexto con el comando/evento y metadatos
            next_middleware: Función para llamar al siguiente middleware
            
        Returns:
            Resultado del procesamiento
        """
        pass

class MiddlewareChain:
    """Cadena de middlewares que se ejecutan en secuencia"""
    
    def __init__(self, middlewares: List[Middleware] = None):
        self.middlewares = middlewares or []
    
    def add_middleware(self, middleware: Middleware) -> 'MiddlewareChain':
        """Agrega un middleware al final de la cadena"""
        self.middlewares.append(middleware)
        return self
    
    def add_middleware_at_beginning(self, middleware: Middleware) -> 'MiddlewareChain':
        """Agrega un middleware al inicio de la cadena"""
        self.middlewares.insert(0, middleware)
        return self
    
    async def execute(self, command_or_event: T, final_handler: Callable) -> Any:
        """
        Ejecuta la cadena de middlewares con el comando/evento dado.
        
        Args:
            command_or_event: Comando o evento a procesar
            final_handler: Handler final que procesará el comando/evento
            
        Returns:
            Resultado del procesamiento
        """
        context = MiddlewareContext(command_or_event=command_or_event)
        
        # Crear la cadena de llamadas
        chain = self._build_chain(final_handler)
        
        # Ejecutar el primer middleware
        return await chain(context)
    
    def _build_chain(self, final_handler: Callable) -> Callable:
        """Construye la cadena de middlewares de forma recursiva"""
        
        async def chain(context: MiddlewareContext) -> Any:
            if not self.middlewares:
                return await final_handler(context.command_or_event)
            
            current_middleware = self.middlewares[0]
            remaining_middlewares = self.middlewares[1:]
            
            # Crear una cadena temporal con los middlewares restantes
            temp_chain = MiddlewareChain(remaining_middlewares)
            next_chain = temp_chain._build_chain(final_handler)
            
            return await current_middleware.process(context, next_chain)
        
        return chain 