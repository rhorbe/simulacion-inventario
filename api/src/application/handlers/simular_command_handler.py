from typing import List
from api.src.application.commands.simular_command import SimularCommand
from api.src.application.inventario import SimulacionInventario


class SimularCommandHandler:
    """Handler que procesa el comando de simulación"""
    
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
            simulacion = SimulacionInventario(politica, command.configuracion)
            resultados.append(simulacion.ejecutar())
        return resultados 