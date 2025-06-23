from typing import List, Optional
from pydantic import BaseModel
from api.domain.dto.politica_abastecimiento import PoliticaAbastecimiento

class SimulacionRequest(BaseModel):
    inventario_inicial: Optional[int] = None
    plazo_entrega_min: Optional[int] = None
    plazo_entrega_max: Optional[int] = None
    dias_simulacion: Optional[int] = None
    anios_simulacion: Optional[int] = None
    costo_almacenar: Optional[float] = None
    costo_faltante: Optional[float] = None
    costo_pedido_pequenio: Optional[float] = None
    costo_pedido_grande: Optional[float] = None
    precio_venta: Optional[float] = None
    politicas_abastecimiento: Optional[List[PoliticaAbastecimiento]] = None
    demanda: Optional[int] = None

