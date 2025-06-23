class DomainError(Exception):
    """
    Excepción base para errores de dominio.
    Representa violaciones de las reglas de negocio.
    """
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message 