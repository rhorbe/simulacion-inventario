from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from api.application.inventario import simular_politica
from api.infra.yml_config_repository import YmlConfigRepository
from fastapi.middleware.cors import CORSMiddleware

config = YmlConfigRepository()
app = FastAPI()

# Configuración de CORS más permisiva para desarrollo
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class PoliticaAbastecimiento(BaseModel):
    punto_reorden: Optional[int] = None
    cantidad_pedido: int

class SimulacionRequest(BaseModel):
    inventario_inicial: int = Field(default=config.simulacion.get('inventario_inicial'))
    plazo_entrega_min: int = Field(default=config.entrega.get('plazo_min'))
    plazo_entrega_max: int = Field(default=config.entrega.get('plazo_max'))
    dias_simulacion: int = Field(default=config.simulacion.get('dias_simulacion'))
    anios_simulacion: int = Field(default=config.simulacion.get('anios_simulacion'))
    costo_almacenar: float = Field(default=config.costos.get('almacenar'))
    costo_faltante: float = Field(default=config.costos.get('faltante'))
    costo_pedido_pequenio: float = Field(default=config.costos.get('pedido_pequeno'))
    costo_pedido_grande: float = Field(default=config.costos.get('pedido_grande'))
    precio_venta: float = Field(default=config.precios.get('venta'))
    politicas_abastecimiento: List[PoliticaAbastecimiento] = Field(default=config.politicas_abastecimiento)
    demanda: int = Field(default=config.simulacion.get('demanda_media'))

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

@app.get("/")
def read_root():
    return {"message": "API de Simulación de Inventario funcionando correctamente"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando"}
