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

    while lista_eventos:
        evento_actual = lista_eventos.pop(0)
        dia = evento_actual.get_dia()

        if dia >= dias_simulacion: break

        if isinstance(evento_actual, EventoDemanda):
            d = evento_actual.get_cantidad()
            ventas = min(d, inventario)
            faltante = max(0, d - inventario)

            inventario -= ventas
            ingresos += ventas * configuracion.get_precio_venta()
            costo_total_faltante += faltante * configuracion.get_costo_faltante()
        elif isinstance(evento_actual, EventoLlegadaPedido):
            cantidad = evento_actual.get_cantidad()
            inventario += cantidad

        if inventario < politica.get_punto_reorden():
            nuevoPedido = EventoLlegadaPedido(
                dia + TiempoEntregaMother.random(seed=42).value(
                    configuracion.get_plazo_entrega_min(),
                    configuracion.get_plazo_entrega_max()
                ),
                politica.get_cantidad_pedido()
            )

            costo_pedidos += politica.get_cantidad_pedido() * configuracion.calcular_costo_unitario_pedido(
                politica.get_cantidad_pedido())
            lista_eventos.append(nuevoPedido)

        lista_eventos.sort(key=lambda x: x.get_dia())

        costo_almacenamiento += inventario * configuracion.get_costo_almacenar()

        if not any(evento.get_dia() >= (dia + 1) for evento in lista_eventos):
            nueva_demanda = EventoDemanda(
                dia + 1,
                DemandaMother.random(seed=42).value(configuracion.get_demanda_media())
            )

            lista_eventos.append(nueva_demanda)

        lista_eventos.sort(key=lambda x: x.get_dia())

    costo_total = costo_almacenamiento + costo_total_faltante + costo_pedidos
    ganancia = ingresos - costo_total

    return {
        "r": politica.get_punto_reorden(),
        "Q": politica.get_cantidad_pedido(),
        "ingresos": ingresos,
        "costo_alm": costo_almacenamiento,
        "costo_faltante": costo_total_faltante,
        "costo_pedidos": costo_pedidos,
        "ganancia": ganancia,
    }
