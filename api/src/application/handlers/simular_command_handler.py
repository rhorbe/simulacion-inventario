from typing import List
from api.src.application.commands.simular_command import SimularCommand
from api.src.application.inventario import SimulacionInventario
from api.src.domain.handlers.command_handler import CommandHandler
from api.src.domain.bus.event_bus import EventBus


class SimularCommandHandler(CommandHandler[SimularCommand]):
    """Handler que procesa el comando de simulación"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    def handle(self, command: SimularCommand) -> List[dict]:
        """
        Procesa el comando ejecutando la simulación para cada política
        
        Args:
            command: Comando con políticas y configuración
            
        Returns:
            Lista de resultados de simulación para cada política
        """
        resultados = []
        for politica in command.politicas:
            simulacion = SimulacionInventario(politica, command.configuracion, self.event_bus)
            resultados.append(simulacion.ejecutar())
        return resultados 