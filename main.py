
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from inventario import simular_politica

from config import (
    INVENTARIO_INICIAL, 
    DEMANDA_MEDIA, 
    PLAZO_ENTREGA_MIN, 
    PLAZO_ENTREGA_MAX,
    COSTO_ALMACENAR, 
    COSTO_FALTANTE, 
    COSTO_PEDIDO_PEQUENO, 
    COSTO_PEDIDO_GRANDE,
    PRECIO_VENTA,
    DIAS_SIMULACION,
    ANIOS_SIMULACION,
    POLITICAS_ABASTECIMIENTO
)

app = FastAPI()

class PoliticaAbastecimiento(BaseModel):
    punto_reorden: Optional[int] = None
    cantidad_pedido: int

class SimulacionRequest(BaseModel):
    inventario_inicial: int = Field(default=INVENTARIO_INICIAL)
    plazo_entrega_min: int = Field(default=PLAZO_ENTREGA_MIN)
    plazo_entrega_max: int = Field(default=PLAZO_ENTREGA_MAX)
    dias_simulacion: int = Field(default=DIAS_SIMULACION)  # Convertir años a días
    anios_simulacion: int = Field(default=ANIOS_SIMULACION)
    costo_almacenar: float = Field(default=COSTO_ALMACENAR)
    costo_faltante: float = Field(default=COSTO_FALTANTE)
    costo_pedido_pequenio: float = Field(default=COSTO_PEDIDO_PEQUENO)
    costo_pedido_grande: float = Field(default=COSTO_PEDIDO_GRANDE)
    precio_venta: float = Field(default=PRECIO_VENTA)
    politicas_abastecimiento: List[PoliticaAbastecimiento] = Field(POLITICAS_ABASTECIMIENTO)
    demanda: int = Field(default=DEMANDA_MEDIA)

# Adaptar lo que hizo Rafa para parametrizar las constantes
app = FastAPI()

@app.get("/")
def read_root():
    return {"Esto es": "nuestro inventario"}

@app.post("/simular")
def simular(data: SimulacionRequest):
    politicas = data.politicas_abastecimiento
    anios_simulacion = data.anios_simulacion
    dias_simulacion = data.dias_simulacion
    total_dias_simulacion = dias_simulacion * anios_simulacion
    resultados = []
    for politica in politicas:
        resultados.append(simular_politica(
            politica.punto_reorden, 
            politica.cantidad_pedido,
            total_dias_simulacion,
            inventario_inicial=data.inventario_inicial,
            plazo_entrega_min=data.plazo_entrega_min,
            plazo_entrega_max=data.plazo_entrega_max,
            costo_almacenar=data.costo_almacenar,
            costo_faltante=data.costo_faltante,
            costo_pedido_pequeno=data.costo_pedido_pequenio,
            costo_pedido_grande=data.costo_pedido_grande,
            precio_venta=data.precio_venta,
            demanda=data.demanda
        ))
    
    return {'resultados': resultados}
