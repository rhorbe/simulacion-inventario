import random

import numpy as np

from api.src.domain.models.evento import Evento
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion

# Generador de números aleatorios de numpy
generador_aleatorio = np.random.default_rng(seed=42)

def generar_demanda(demanda_media):
    """
    Genera una demanda aleatoria para un día.

    La demanda se asume como una variable aleatoria con distribución de Poisson
    con media demanda_media.

    Args:
        demanda_media (int): Media de la distribución de Poisson

    Returns:
        int: Demanda aleatoria para un día.
    """
    return generador_aleatorio.poisson(demanda_media)


def generar_tiempo_entrega(plazo_min, plazo_max):
    """
    Genera un plazo de entrega aleatorio en días.

    El plazo de entrega se asume como una variable aleatoria con distribución uniforme
    entre plazo_min y plazo_max.

    Args:
        plazo_min (int): Plazo mínimo de entrega
        plazo_max (int): Plazo máximo de entrega

    Returns:
        int: Plazo de entrega aleatorio en días.
    """
    return random.randint(plazo_min, plazo_max)


def imprimir_resultados(resultado):
    costo_faltante = resultado["costo_faltante"]
    costo_almacenar = resultado["costo_alm"]
    costo_pedidos = resultado["costo_pedidos"]
    costo_total = costo_faltante + costo_almacenar + costo_pedidos

    print(f"\nPolítica (r={resultado['r']}, Q={resultado['Q']}):")
    print(f"  Ingresos:        ${resultado['ingresos']:.2f}")
    print(f"  Costo almacén:   ${resultado['costo_alm']:.2f}")
    print(f"  Costo faltantes: ${resultado['costo_faltante']:.2f}")
    print(f"  Costo pedidos:   ${resultado['costo_pedidos']:.2f}")
    print(f"  Costo total:     ${costo_total:.2f}")
    print(f"  Ganancia neta:   ${resultado['ganancia']:.2f}")

def existen_eventos_pendientes(lista_eventos, dia):
    """
    Verifica si hay eventos pendientes para el día actual.

    Args:
        lista_eventos (list): Lista de eventos pendientes.
        dia (int): Día actual.

    Returns:
        bool: True si hay eventos pendientes, False en caso contrario.
    """
    return any(evento.get_dia() >= dia for evento in lista_eventos)


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
    
    lista_eventos = [Evento("demanda", 0, generar_demanda(demanda_media))]

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
            demanda = evento_actual.get_cantidad()
            ventas, faltante = calcular_resultados_diarios(demanda, inventario)
            inventario -= ventas
            ingresos += ventas * precio_venta
            costo_total_faltante += faltante * costo_por_faltante
        elif tipo_evento == "llegada_pedido":
            cantidad = evento_actual.get_cantidad()
            inventario += cantidad

        if inventario < r:
            nuevoPedido = Evento("llegada_pedido", dia + generar_tiempo_entrega(plazo_entrega_min, plazo_entrega_max), Q)
            costo_pedidos += Q * configuracion.calcular_costo_unitario_pedido(Q)
            lista_eventos.append(nuevoPedido)
            lista_eventos.sort(key=lambda x: x.get_dia())

        costo_almacenamiento += inventario * costo_almacenar

        # Si no hay eventos pendientes para el día siguiente, generar una nueva demanda
        if not existen_eventos_pendientes(lista_eventos, dia + 1):
            nueva_demanda = Evento("demanda", dia + 1, generar_demanda(demanda_media))
            lista_eventos.append(nueva_demanda)

        # Ordenar eventos por día
        lista_eventos.sort(key=lambda x: x.get_dia())
    
    # Calcular costos finales
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


def calcular_faltante(demanda, inventario):
    return max(0, demanda - inventario)


def calcular_ventas(demanda, inventario):
    return min(demanda, inventario)


def calcular_resultados_diarios(demanda, inventario):
    ventas = calcular_ventas(demanda, inventario)
    faltante = calcular_faltante(demanda, inventario)

    return ventas, faltante


def procesar_llegada_pedidos(dia, inventario, pedidos_pendientes):
    pedidos_que_llegan = [p for p in pedidos_pendientes if p[0] == dia]

    for llegada, cantidad in pedidos_que_llegan:
        inventario += cantidad

    pedidos_pendientes = [p for p in pedidos_pendientes if p[0] > dia]

    return inventario, pedidos_pendientes