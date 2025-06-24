from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion
from api.src.domain.object_mothers import DemandaMother, TiempoEntregaMother

def simular_politica(politica: PoliticaInventario, dias_simulacion: int, configuracion: ConfiguracionSimulacion):
    """
    Simula la política de inventario dada por (r, Q) durante dias_simulacion días.

    Args:
        politica (PoliticaInventario): Política de inventario (r, Q)
        dias_simulacion (int): Días totales de simulación
        configuracion (ConfiguracionSimulacion): Configuración de la simulación

    Returns:
        dict: Diccionario con los resultados de la simulación.
    """
    inventario = configuracion.get_inventario_inicial()
    lista_eventos = [EventoDemanda(0, DemandaMother.random(seed=42).value(configuracion.get_demanda_media()))]

    costo_almacenamiento = 0
    costo_total_faltante = 0
    costo_pedidos = 0
    ingresos = 0

    resultados = ResultadosPolitica(
        r=politica.get_punto_reorden(),
        Q=politica.get_cantidad_pedido(),
        inventario=configuracion.get_inventario_inicial()
    )


    while fel.hay_eventos():
        evento_actual = fel.obtener_siguiente_evento()
        dia = evento_actual.get_dia()

        if dia >= dias_simulacion: break

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
            costo_pedidos += politica.get_cantidad_pedido() * configuracion.calcular_costo_unitario_pedido(
                politica.get_cantidad_pedido())
            resultados.agregar_costo_pedido(costo_pedido)

            lista_eventos.append(nuevo_pedido)

        resultados.agregar_costo_almacenamiento(resultados.obtener_inventario() * configuracion.get_costo_almacenar())

        costo_almacenamiento += inventario * configuracion.get_costo_almacenar()

        if not any(evento.get_dia() >= (dia + 1) for evento in lista_eventos):
            nueva_demanda = EventoDemanda(
                dia + 1,
                DemandaMother.random(seed=42).value(configuracion.get_demanda_media())
            )

            lista_eventos.append(nueva_demanda)

        lista_eventos.sort(key=lambda x: x.get_dia())

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