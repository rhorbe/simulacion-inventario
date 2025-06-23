from api.src.domain.models.evento import Evento
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
    precio_venta = configuracion.get_precio_venta()
    costo_almacenar = configuracion.get_costo_almacenar()
    costo_por_faltante = configuracion.get_costo_faltante()
    demanda_media = configuracion.get_demanda_media()
    plazo_entrega_min = configuracion.get_plazo_entrega_min()
    plazo_entrega_max = configuracion.get_plazo_entrega_max()
    
    r = politica.get_punto_reorden()
    Q = politica.get_cantidad_pedido()
    
    lista_eventos = [Evento("demanda", 0, DemandaMother.random(seed=42).value(demanda_media))]

    costo_almacenamiento = 0
    costo_total_faltante = 0
    costo_pedidos = 0
    ingresos = 0

    while lista_eventos:
        evento_actual = lista_eventos.pop(0)
        tipo_evento = evento_actual.get_tipo()
        dia = evento_actual.get_dia()

        if dia >= dias_simulacion: break

        if tipo_evento == "demanda":
            d = evento_actual.get_cantidad()
            ventas = min(d, inventario)
            faltante = max(0, d - inventario)

            inventario -= ventas
            ingresos += ventas * precio_venta
            costo_total_faltante += faltante * costo_por_faltante
        elif tipo_evento == "llegada_pedido":
            cantidad = evento_actual.get_cantidad()
            inventario += cantidad

        if inventario < r:
            nuevoPedido = Evento("llegada_pedido", dia + TiempoEntregaMother.random(seed=42).value(plazo_entrega_min, plazo_entrega_max), Q)
            costo_pedidos += Q * configuracion.calcular_costo_unitario_pedido(Q)
            lista_eventos.append(nuevoPedido)
            lista_eventos.sort(key=lambda x: x.get_dia())

        costo_almacenamiento += inventario * costo_almacenar

        if not any(evento.get_dia() >= (dia + 1) for evento in lista_eventos):
            nueva_demanda = Evento("demanda", dia + 1, DemandaMother.random(seed=42).value(demanda_media))
            lista_eventos.append(nueva_demanda)

        lista_eventos.sort(key=lambda x: x.get_dia())
    
    costo_total = costo_almacenamiento + costo_total_faltante + costo_pedidos
    ganancia = ingresos - costo_total

    return {
        "r": r,
        "Q": Q,
        "ingresos": ingresos,
        "costo_alm": costo_almacenamiento,
        "costo_faltante": costo_total_faltante,
        "costo_pedidos": costo_pedidos,
        "ganancia": ganancia,
    }

