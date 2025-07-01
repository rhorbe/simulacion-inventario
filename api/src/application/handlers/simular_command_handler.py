from typing import List
from api.src.domain.bus.command_bus import CommandHandler
from api.src.domain.bus.event_bus import EventBus
from api.src.domain.models.command import SimularCommand
from api.src.application.inventario import SimulacionInventario

class SimularCommandHandler(CommandHandler[SimularCommand]):
    """Handler para el comando SimularCommand"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    async def handle(self, command: SimularCommand) -> List[dict]:
        """
        Maneja el comando de simulación ejecutando la simulación para cada política
        
        Args:
            command: Comando de simulación con políticas y configuración
            
        Returns:
            Lista de resultados para cada política evaluada
        """
        resultados = []
        
        for politica in command.politicas:
            # Crear simulación para esta política
            simulacion = SimulacionInventario(
                politica=politica,
                configuracion=command.configuracion,
                event_bus=self.event_bus
            )
            
            # Ejecutar simulación
            resultado = await simulacion.ejecutar()
            
            # Agregar información de la política al resultado
            resultado_politica = {
                "r": resultado["r"],
                "Q": resultado["Q"],
                "ganancia": resultado["ganancia"],
                "costo_alm": resultado["costo_alm"],
                "costo_faltante": resultado["costo_faltante"],
                "costo_pedidos": resultado["costo_pedidos"],
                "ingresos": resultado["ingresos"]
            }
            
            resultados.append(resultado_politica)
        
        return resultados 