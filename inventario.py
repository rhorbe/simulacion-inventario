import time
from evento import Evento
import numpy as np
import random
from config import (
    INVENTARIO_INICIAL, 
    DEMANDA_MEDIA, 
    PLAZO_ENTREGA_MIN, 
    PLAZO_ENTREGA_MAX,
    COSTO_ALMACENAR, 
    COSTO_FALTANTE, 
    COSTO_PEDIDO_PEQUENO, 
    COSTO_PEDIDO_GRANDE,
    PRECIO_VENTA,
    DIAS_SIMULACION,
    ANIOS_SIMULACION
)


TIEMPO_TOTAL_SIMULACION = DIAS_SIMULACION * ANIOS_SIMULACION  # Total de días de simulación
# Lista de politicas a comparar: cada tupla es (r, Q)
politicas = [
    {"r": 40, "Q": 140},  # politica actual
    {"r": 30, "Q": 140},
    {"r": 60, "Q": 140},
    {"r": 40, "Q": 100},
    {"r": 40, "Q": 200},
    {"r": 50, "Q": 180},
]


# Generador de números aleatorios de numpy
generador_aleatorio = np.random.default_rng(seed=42)


def generar_demanda():
    """
    Genera una demanda aleatoria para un día.

    La demanda se asume como una variable aleatoria con distribución de Poisson
    con media DEMANDA_MEDIA.

    Returns:
        int: Demanda aleatoria para un día.
    """
    return generador_aleatorio.poisson(DEMANDA_MEDIA)


def generar_tiempo_entrega():
    """
    Genera un plazo de entrega aleatorio en días.

    El plazo de entrega se asume como una variable aleatoria con distribución uniforme
    entre PLAZO_ENTREGA_MIN y PLAZO_ENTREGA_MAX.

    Returns:
        int: Plazo de entrega aleatorio en días.
    """
    return random.randint(PLAZO_ENTREGA_MIN, PLAZO_ENTREGA_MAX)


def costo_unitario_pedido(q, costo_pedido_pequeno=COSTO_PEDIDO_PEQUENO, costo_pedido_grande=COSTO_PEDIDO_GRANDE):
    """
    Calcula el costo unitario de un pedido según su cantidad.

    Args:
        q (int): Cantidad del pedido.

    Returns:
        float: Costo unitario del pedido.
    """

    return costo_pedido_pequeno if q < 300 else costo_pedido_grande


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

def simular_politica(r, Q, dias_simulacion=TIEMPO_TOTAL_SIMULACION, **kwargs):
    """
    Simula la política de inventario dada por (r, Q) durante DIAS_SIMULACION días.

    Args:
        r (int): Nivel de reposición.
        Q (int): Tamaño del lote de reposición.

    Returns:
        dict: Diccionario con los resultados de la simulación.
    """
    inventario = kwargs.get("inventario_inicial", INVENTARIO_INICIAL)
    precio_venta = kwargs.get("precio_venta", PRECIO_VENTA)
    costo_almacenar = kwargs.get("costo_almacenar", COSTO_ALMACENAR)
    costo_por_faltante = kwargs.get("costo_faltante", COSTO_FALTANTE)
    costo_pedido_pequeno = kwargs.get("costo_pedido_pequeno", COSTO_PEDIDO_PEQUENO)
    costo_pedido_grande = kwargs.get("costo_pedido_grande", COSTO_PEDIDO_GRANDE)
    
    lista_eventos = [Evento("demanda", 0, generar_demanda())]

    costo_almacenamiento = 0
    costo_total_faltante = 0
    costo_pedidos = 0
    ingresos = 0

    while lista_eventos:
        evento_actual = lista_eventos.pop(0)
        tipo_evento = evento_actual.get_tipo()
        dia = evento_actual.get_dia()

        if dia >= dias_simulacion: break

        match tipo_evento:
            case "demanda":
                demanda = evento_actual.get_cantidad()
                ventas, faltante = calcular_resultados_diarios(demanda, inventario)
                inventario -= ventas
                ingresos += ventas * precio_venta
                costo_total_faltante += faltante * costo_por_faltante
            case "llegada_pedido":
                cantidad = evento_actual.get_cantidad()
                inventario += cantidad

        if inventario < r:
            nuevoPedido = Evento("llegada_pedido", dia + generar_tiempo_entrega(), Q)
            costo_pedidos += Q * costo_unitario_pedido(Q, costo_pedido_pequeno, costo_pedido_grande)
            lista_eventos.append(nuevoPedido)
            lista_eventos.sort(key=lambda x: x.get_dia())

        
        costo_almacenamiento += inventario * costo_almacenar

        # Generar nueva demanda para el siguiente día
        # Tengo que verificar si ya se procesaron todos los eventos del dia actual para podier generar la nueva demanda

        # Si no hay eventos pendientes para el día siguiente, generar una nueva demanda
        if not existen_eventos_pendientes(lista_eventos, dia + 1):
            nueva_demanda = Evento("demanda", dia + 1, generar_demanda())
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


def procesar_reposicion(dia, q, pedidos_pendientes, costo_pedidos):

    llegada_pedido = dia + generar_tiempo_entrega()
    pedidos_pendientes.append((llegada_pedido, q))
    costo_pedidos += q * costo_unitario_pedido(q)

    return pedidos_pendientes, costo_pedidos


def simular():
    for politica in politicas:
        resultado = simular_politica(politica["r"], politica["Q"])
        imprimir_resultados(resultado)