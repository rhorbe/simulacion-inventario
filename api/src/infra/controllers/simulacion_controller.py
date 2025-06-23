from fastapi import APIRouter, Depends

from api.src.application.inventario import simular_politica
from api.src.domain.repository.config import Config
from api.src.domain.dto.simulacion_request import SimulacionRequest
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion
from api.src.dependency_injection import get_config

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
    
    # Crear configuración de simulación usando ValueObjects
    configuracion = ConfiguracionSimulacion.from_parametros(
        inventario_inicial=request.inventario_inicial,
        precio_venta=request.precio_venta,
        costo_almacenar=request.costo_almacenar,
        costo_faltante=request.costo_faltante,
        costo_pedido_pequeno=request.costo_pedido_pequenio,
        costo_pedido_grande=request.costo_pedido_grande,
        plazo_entrega_min=request.plazo_entrega_min,
        plazo_entrega_max=request.plazo_entrega_max,
        demanda_media=request.demanda
    )
    
    resultados = []
    for politica_dto in politicas:
        # Crear política de inventario usando ValueObjects
        politica = PoliticaInventario.from_valores(
            punto_reorden=politica_dto.punto_reorden,
            cantidad_pedido=politica_dto.cantidad_pedido
        )
        
        resultados.append(simular_politica(
            politica=politica,
            dias_simulacion=total_dias_simulacion,
            configuracion=configuracion
        ))

    return {'resultados': resultados}
