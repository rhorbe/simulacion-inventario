from fastapi import APIRouter, Depends

from api.application.inventario import simular_politica
from api.domain.repository.config import Config
from api.domain.dto.simulacion_request import SimulacionRequest
from api.dependency_injection import get_config

router = APIRouter()

@router.post("/simular")
async def simular_inventario(
    request: SimulacionRequest,
    config: Config = Depends(get_config)
):
    """
    Endpoint para simular el inventario basado en el modelo (r, Q).
    
    Args:
        request: Datos de la simulación
        config: Configuración inyectada por dependencia
    
    Returns:
        Resultados de la simulación
    """
    politicas = request.politicas_abastecimiento
    anios_simulacion = request.anios_simulacion
    dias_simulacion = request.dias_simulacion
    total_dias_simulacion = dias_simulacion * anios_simulacion
    resultados = []
    for politica in politicas:
        resultados.append(simular_politica(
            politica.punto_reorden,
            politica.cantidad_pedido,
            total_dias_simulacion,
            inventario_inicial=request.inventario_inicial,
            plazo_entrega_min=request.plazo_entrega_min,
            plazo_entrega_max=request.plazo_entrega_max,
            costo_almacenar=request.costo_almacenar,
            costo_faltante=request.costo_faltante,
            costo_pedido_pequeno=request.costo_pedido_pequenio,
            costo_pedido_grande=request.costo_pedido_grande,
            precio_venta=request.precio_venta,
            demanda=request.demanda
        ))

    return {'resultados': resultados}
