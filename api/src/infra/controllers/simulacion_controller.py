from fastapi import APIRouter, Depends
from typing import List

from api.src.domain.bus.command_bus import CommandBus
from api.src.domain.models.command import SimularCommand
from api.src.domain.repository.config import Config
from api.src.domain.dto.simulacion_request import SimulacionRequest
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion
from api.src.infra.dependency_injection import get_config, get_command_bus

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
        request: Datos de la simulación incluyendo políticas y configuración
        config: Configuración del sistema
        command_bus: Bus de comandos inyectado
        
    Returns:
        Lista de resultados para cada política evaluada
    """
    # Crear política por defecto si no se proporciona
    if not request.politicas_abastecimiento:
        # Crear una política por defecto basada en los parámetros
        politica = PoliticaInventario.from_valores(
            punto_reorden=request.inventario_inicial // 2 if request.inventario_inicial else 50,
            cantidad_pedido=request.inventario_inicial if request.inventario_inicial else 100
        )
        politicas = [politica]
    else:
        # Convertir políticas del DTO
        politicas = [
            PoliticaInventario.from_valores(
                punto_reorden=pol.punto_reorden,
                cantidad_pedido=pol.cantidad_pedido
            )
            for pol in request.politicas_abastecimiento
        ]
    
    # Crear configuración
    configuracion = ConfiguracionSimulacion.from_parametros(
        inventario_inicial=request.inventario_inicial or 100,
        demanda_media=request.demanda or 50,
        precio_venta=request.precio_venta or 10.0,
        costo_almacenar=request.costo_almacenar or 1.0,
        costo_faltante=request.costo_faltante or 5.0,
        plazo_entrega_min=request.plazo_entrega_min or 1,
        plazo_entrega_max=request.plazo_entrega_max or 3,
        costo_pedido_pequeno=request.costo_pedido_pequenio or 10.0,
        costo_pedido_grande=request.costo_pedido_grande or 20.0,
        dias_simulacion=request.dias_simulacion or 30
    )
    
    # Crear y ejecutar comando
    command = SimularCommand(politicas=politicas, configuracion=configuracion)
    resultados = await command_bus.execute(command)
    
    return {
        "message": "Simulación completada exitosamente",
        "resultados": resultados,
        "politicas_evaluadas": len(politicas)
    }


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
