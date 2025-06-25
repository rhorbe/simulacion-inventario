from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido
from api.src.domain.models.resultados_politica import ResultadosPolitica
from api.src.domain.models.fel import FEL
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion
from api.src.domain.object_mothers import DemandaMother, TiempoEntregaMother


def simular_politica(politica: PoliticaInventario, configuracion: ConfiguracionSimulacion):
    """
    Simula la política de inventario dada por (r, Q) durante los días especificados en la configuración.

    Args:
        politica (PoliticaInventario): Política de inventario (r, Q)
        configuracion (ConfiguracionSimulacion): Configuración de la simulación

    Returns:
        dict: Diccionario con los resultados de la simulación.
    """
    # Inicializar FEL con el evento de demanda inicial
    fel = FEL(
        [
            (EventoDemanda(
                0,
                DemandaMother
                    .random(seed=42)
                    .value(configuracion.get_demanda_media())
            ))
        ])

    resultados = ResultadosPolitica(
        r=politica.get_punto_reorden(),
        Q=politica.get_cantidad_pedido(),
        inventario=configuracion.get_inventario_inicial()
    )

    while fel.hay_eventos():
        # Obtener el evento actual (automáticamente obtiene el siguiente si no hay uno actual)
        evento_actual = fel.obtener_evento_actual()
        dia = evento_actual.get_dia()

        if dia >= configuracion.get_dias_simulacion(): 
            break

        if isinstance(evento_actual, EventoDemanda):
            d = evento_actual.get_cantidad()
            inventario_actual = resultados.obtener_inventario()
            ventas = min(d, inventario_actual)
            faltante = max(0, d - inventario_actual)

            resultados.actualizar_inventario(-ventas)
            resultados.agregar_ingreso(ventas * configuracion.get_precio_venta())
            resultados.agregar_costo_faltante(faltante * configuracion.get_costo_faltante())
        elif isinstance(evento_actual, EventoLlegadaPedido):
            cantidad = evento_actual.get_cantidad()
            resultados.actualizar_inventario(cantidad)

        nuevo_pedido = revision(configuracion, dia, resultados.obtener_inventario(), politica)

        if nuevo_pedido is not None:
            costo_pedido = politica.get_cantidad_pedido() * configuracion.calcular_costo_unitario_pedido(
                politica.get_cantidad_pedido())
            resultados.agregar_costo_pedido(costo_pedido)

            fel.agregar_evento(nuevo_pedido)

        resultados.agregar_costo_almacenamiento(resultados.obtener_inventario() * configuracion.get_costo_almacenar())

        if not fel.hay_eventos_futuros_en_dia(dia + 1):
            nueva_demanda = EventoDemanda(
                dia + 1,
                DemandaMother.random(seed=42).value(configuracion.get_demanda_media())
            )

            fel.agregar_evento(nueva_demanda)

    return resultados.to_dict()


def revision(configuracion, dia, inventario, politica):
    if inventario < politica.get_punto_reorden():

        return EventoLlegadaPedido(
            dia + TiempoEntregaMother.random(seed=42).value(
                configuracion.get_plazo_entrega_min(),
                configuracion.get_plazo_entrega_max()
            ),
            politica.get_cantidad_pedido()
        )

    return None