
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from inventario import simular_politica

app = FastAPI()

class PoliticaAbastecimiento(BaseModel):
    punto_reorden: Optional[int] = None
    cantidad_pedido: int

class SimulacionRequest(BaseModel):
    inventario_inicial: int = Field(default=0)
    plazo_entrega_min: int = Field(default=1)
    plazo_entrega_max: int = Field(default=3)
    anios_simulacion: int = Field(default=1)
    costo_almacenar: float = Field(default=0.5)
    costo_faltante: float = Field(default=2.0)
    costo_pedido_pequenio: float = Field(default=10.0)
    costo_pedido_grande: float = Field(default=20.0)
    precio_venta: float = Field(default=100.0)
    politicas_abastecimiento: List[PoliticaAbastecimiento]
    demanda: List[int]

# Adapatar lo que hizo Rafa para parametrizar las constantes
app = FastAPI()

@app.get("/")
def read_root():
    return {"Esto es": "nuestro inventario"}

@app.post("/simular")
def simular(data: SimulacionRequest):
    return data
