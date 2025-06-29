from typing import Dict, Type, Any
from api.src.domain.bus.command_bus import CommandBus


class InMemoryCommandBus(CommandBus):
    """Implementación en memoria del bus de comandos"""
    
    def __init__(self):
        self._handlers: Dict[Type, Any] = {}
    
    def register_handler(self, command_type: Type, handler: Any) -> None:
        """Registra un handler para un tipo de comando específico"""
        self._handlers[command_type] = handler
    
    def execute(self, command: Any) -> Any:
        """
        Ejecuta un comando usando el handler registrado
        
        Args:
            command: Comando a ejecutar
            
        Returns:
            Resultado de la ejecución del comando
            
        Raises:
            ValueError: Si no hay handler registrado para el tipo de comando
        """
        command_type = type(command)
        if command_type not in self._handlers:
            raise ValueError(f"No handler registrado para el comando: {command_type.__name__}")
        
        handler = self._handlers[command_type]
        return handler.handle(command) 