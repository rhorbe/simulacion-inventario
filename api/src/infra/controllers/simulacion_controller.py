from fastapi import APIRouter, Depends
from typing import List

from api.src.application.command_bus import CommandBus
from api.src.application.commands.simular_command import SimularCommand
from api.src.domain.repository.config import Config
from api.src.domain.dto.simulacion_request import SimulacionRequest
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion
from api.src.dependency_injection import get_config, get_command_bus

router = APIRouter()

@router.post("/simular")
async def simular_inventario(
    request: SimulacionRequest,
    config: Config = Depends(get_config),
    command_bus: CommandBus = Depends(get_command_bus)
):
    """
    Endpoint para simular el inventario basado en el modelo (r, Q).
    
    Args:
        request: Datos de la simulación
        config: Configuración inyectada por dependencia
        command_bus: Bus de comandos inyectado por dependencia
    
    Returns:
        Resultados de la simulación
    """
    # Mapear request a ValueObjects
    politicas = _mapear_politicas(request.politicas_abastecimiento, config)
    configuracion = _mapear_configuracion(request, config)
    
    # Crear y ejecutar comando a través del bus
    command = SimularCommand(politicas=politicas, configuracion=configuracion)
    resultados = command_bus.execute(command)
    
    return {'resultados': resultados}


def _mapear_politicas(politicas_dto: List, config: Config) -> List[PoliticaInventario]:
    """Mapea DTOs de políticas a ValueObjects"""
    # Configurar Value Objects con la configuración por defecto
    PoliticaInventarioConConfig = PoliticaInventario.with_config(config)
    
    politicas = []
    for politica_dto in politicas_dto:
        # Crear política de inventario usando ValueObjects con valores por defecto
        # Los parámetros None se reemplazarán con valores de la configuración
        politica = PoliticaInventarioConConfig.from_valores(
            punto_reorden=politica_dto.punto_reorden,
            cantidad_pedido=politica_dto.cantidad_pedido
        )
        politicas.append(politica)
    
    # Limpiar configuraciones por defecto
    PoliticaInventarioConConfig.clear_default_config()
    
    return politicas


def _mapear_configuracion(request: SimulacionRequest, config: Config) -> ConfiguracionSimulacion:
    """Mapea request a ValueObject de configuración"""
    # Configurar Value Objects con la configuración por defecto
    ConfiguracionSimulacionConConfig = ConfiguracionSimulacion.with_config(config)
    
    anios_simulacion = request.anios_simulacion
    dias_simulacion = request.dias_simulacion
    total_dias_simulacion = dias_simulacion * anios_simulacion
    
    # Crear configuración de simulación usando ValueObjects con valores por defecto
    # Los parámetros None se reemplazarán con valores de la configuración
    configuracion = ConfiguracionSimulacionConConfig.from_parametros(
        inventario_inicial=request.inventario_inicial,
        precio_venta=request.precio_venta,
        costo_almacenar=request.costo_almacenar,
        costo_faltante=request.costo_faltante,
        costo_pedido_pequeno=request.costo_pedido_pequenio,
        costo_pedido_grande=request.costo_pedido_grande,
        plazo_entrega_min=request.plazo_entrega_min,
        plazo_entrega_max=request.plazo_entrega_max,
        demanda_media=request.demanda,
        dias_simulacion=total_dias_simulacion
    )
    
    # Limpiar configuraciones por defecto
    ConfiguracionSimulacionConConfig.clear_default_config()
    
    return configuracion
