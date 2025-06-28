from typing import Type, Any, Dict, Callable


class CommandBus:
    """Bus de comandos simplificado para CQRS"""
    
    def __init__(self):
        self._handlers: Dict[Type, Callable] = {}
    
    def register_handler(self, command_type: Type, handler: Callable) -> None:
        """Registra un handler para un tipo de comando"""
        self._handlers[command_type] = handler
    
    def execute(self, command: Any) -> Any:
        """Ejecuta un comando usando el handler registrado"""
        command_type = type(command)
        if command_type not in self._handlers:
            raise ValueError(f"No handler registrado para {command_type}")
        
        handler = self._handlers[command_type]
        return handler.handle(command) 