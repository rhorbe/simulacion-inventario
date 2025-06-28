from typing import List, Optional
from api.src.domain.models.evento import Evento

class FEL:
    """
    Future Event List (FEL) - Lista de eventos futuros para simulación discreta de eventos.
    Encapsula la lógica de gestión de eventos ordenados por tiempo de ocurrencia.
    """
    
    def __init__(self, eventos_iniciales: Optional[List[Evento]] = None):
        """
        Inicializa una lista de eventos futuros.
        
        Args:
            eventos_iniciales: Lista opcional de eventos iniciales. Si es None, se crea una lista vacía.
        """
        if eventos_iniciales is None:
            self._eventos: List[Evento] = []
        else:
            self._eventos = eventos_iniciales.copy()
            self._ordenar_eventos()
        
        # Evento actual que se está procesando
        self._evento_actual: Optional[Evento] = None
    
    def agregar_evento(self, evento: Evento) -> None:
        """
        Agrega un evento a la lista y mantiene el orden cronológico.
        
        Args:
            evento: Evento a agregar a la lista
        """
        self._eventos.append(evento)
        self._ordenar_eventos()

    def siguiente(self) -> Evento:
        """
        Obtiene el próximo evento de la lista (el de menor tiempo).
        Si no hay eventos en la lista, lanza una excepción.
        
        Returns:
            El próximo evento
            
        Raises:
            ValueError: Si no hay eventos disponibles en la FEL
        """
        if not self._eventos:
            raise ValueError("No hay eventos disponibles en la FEL")
        
        self._evento_actual = self._eventos.pop(0)
        return self._evento_actual

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

    def _ordenar_eventos(self) -> None:
        """Ordena los eventos por día de ocurrencia (ascendente)."""
        self._eventos.sort(key=lambda x: x.get_dia())
    
    def __str__(self) -> str:
        """Representación en string de la FEL."""
        if not self._eventos and not self._evento_actual:
            return "FEL: []"
        
        eventos_str = ", ".join([f"{evento.get_tipo()}(día={evento.get_dia()})" for evento in self._eventos])
        fel_str = f"FEL: [{eventos_str}]"
        
        if self._evento_actual:
            fel_str += f" | Actual: {self._evento_actual.get_tipo()}(día={self._evento_actual.get_dia()})"
        
        return fel_str
    
    def __len__(self) -> int:
        """Retorna la cantidad de eventos en la lista."""
        return len(self._eventos) 