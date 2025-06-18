from dataclasses import dataclass

@dataclass
class Evento:
    tipo: str
    dia: int
    cantidad: int = 0

    def __str__(self):
        return f"Evento(tipo={self.tipo}, dia={self.dia}, cantidad={self.cantidad})"

    def get_dia(self):
        return self.dia
    
    def get_tipo(self):
        return self.tipo
    
    def get_cantidad(self):
        return self.cantidad
    
