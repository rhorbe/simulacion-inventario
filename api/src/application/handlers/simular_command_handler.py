from typing import List
from api.src.domain.bus.command_bus import CommandHandler
from api.src.domain.bus.event_bus import EventBus
from api.src.domain.dto.simular_command import SimularCommand
from api.src.application.inventario import SimulacionInventario

class SimularCommandHandler(CommandHandler[SimularCommand]):
    """Handler para el comando SimularCommand"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    def handle(self, command: SimularCommand) -> List[dict]:
        """
        Maneja el comando de simulación ejecutando la simulación para cada política
        
        Args:
            command: Comando de simulación con políticas y configuración
            
        Returns:
            Lista de resultados de simulación para cada política
        """
        resultados = []
        
        for politica in command.politicas:
            simulacion = SimulacionInventario(politica, command.configuracion, self.event_bus)
            resultado = simulacion.ejecutar()
            resultados.append(resultado)
        
        return resultados 