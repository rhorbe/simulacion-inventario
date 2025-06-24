from typing import List, Optional
from api.src.domain.models.evento import EventoBase

class FEL:
    """
    Future Event List (FEL) - Lista de eventos futuros para simulación discreta de eventos.
    Encapsula la lógica de gestión de eventos ordenados por tiempo de ocurrencia.
    """
    
    def __init__(self):
        """Inicializa una lista de eventos futuros vacía."""
        self._eventos: List[EventoBase] = []
    
    def agregar_evento(self, evento: EventoBase) -> None:
        """
        Agrega un evento a la lista y mantiene el orden cronológico.
        
        Args:
            evento: Evento a agregar a la lista
        """
        self._eventos.append(evento)
        self._ordenar_eventos()
    
    def obtener_siguiente_evento(self) -> Optional[EventoBase]:
        """
        Obtiene y remueve el próximo evento de la lista (el de menor tiempo).
        
        Returns:
            El próximo evento o None si la lista está vacía
        """
        if not self._eventos:
            return None
        return self._eventos.pop(0)
    
    def hay_eventos(self) -> bool:
        """
        Verifica si hay eventos en la lista.
        
        Returns:
            True si hay eventos, False en caso contrario
        """
        return len(self._eventos) > 0
    
    def hay_eventos_futuros_en_dia(self, dia: int) -> bool:
        """
        Verifica si hay eventos programados para un día específico o posterior.
        
        Args:
            dia: Día de referencia
            
        Returns:
            True si hay eventos en o después del día especificado
        """
        return any(evento.get_dia() >= dia for evento in self._eventos)
    
    def obtener_proximo_dia_evento(self) -> Optional[int]:
        """
        Obtiene el día del próximo evento sin removerlo de la lista.
        
        Returns:
            El día del próximo evento o None si la lista está vacía
        """
        if not self._eventos:
            return None
        return self._eventos[0].get_dia()
    
    def limpiar(self) -> None:
        """Limpia todos los eventos de la lista."""
        self._eventos.clear()
    
    def obtener_cantidad_eventos(self) -> int:
        """
        Obtiene la cantidad de eventos en la lista.
        
        Returns:
            Número de eventos en la lista
        """
        return len(self._eventos)
    
    def _ordenar_eventos(self) -> None:
        """Ordena los eventos por día de ocurrencia (ascendente)."""
        self._eventos.sort(key=lambda x: x.get_dia())
    
    def __str__(self) -> str:
        """Representación en string de la FEL."""
        if not self._eventos:
            return "FEL: []"
        
        eventos_str = ", ".join([f"{evento.get_tipo()}(día={evento.get_dia()})" for evento in self._eventos])
        return f"FEL: [{eventos_str}]"
    
    def __len__(self) -> int:
        """Retorna la cantidad de eventos en la lista."""
        return len(self._eventos) 