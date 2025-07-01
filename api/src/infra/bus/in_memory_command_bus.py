from typing import Dict, Type, Any, List
from api.src.domain.bus.command_bus import CommandBus, CommandHandler
from api.src.domain.bus.middleware import Middleware, MiddlewareChain


class InMemoryCommandBus(CommandBus):
    """Implementación en memoria del bus de comandos con soporte para middlewares"""
    
    def __init__(self):
        self._handlers: Dict[Type, CommandHandler] = {}
        self._middleware_chain = MiddlewareChain()
    
    def register_handler(self, command_type: Type, handler: CommandHandler) -> None:
        """
        Registra un handler para un tipo de comando específico
        
        Args:
            command_type: Tipo de comando
            handler: Handler que procesará el comando
        """
        self._handlers[command_type] = handler
    
    async def execute(self, command: Any) -> Any:
        """
        Ejecuta un comando usando el handler registrado y la cadena de middlewares
        
        Args:
            command: Comando a ejecutar
            
        Returns:
            Resultado de la ejecución del comando
            
        Raises:
            ValueError: Si no hay handler registrado para el tipo de comando
        """
        command_type = type(command)
        
        if command_type not in self._handlers:
            raise ValueError(f"No se encontró handler para el comando: {command_type.__name__}")
        
        handler = self._handlers[command_type]
        
        # Si no hay middlewares, ejecutar directamente
        if not self._middleware_chain.middlewares:
            return await handler.handle(command)
        
        # Ejecutar a través de la cadena de middlewares
        return await self._middleware_chain.execute(command, lambda cmd: handler.handle(cmd))
    
    def add_middleware(self, middleware: Middleware) -> None:
        """Agrega un middleware al bus"""
        self._middleware_chain.add_middleware(middleware)
    
    def get_middlewares(self) -> List[Middleware]:
        """Retorna la lista de middlewares configurados"""
        return self._middleware_chain.middlewares.copy() 