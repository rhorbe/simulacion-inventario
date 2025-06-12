import numpy as np
import random

# Parámetros generales de la simulación

# Unidades
INVENTARIO_INICIAL = 720
DEMANDA_MEDIA = 200  # Media diaria para Poisson
PLAZO_ENTREGA_MIN = 1
PLAZO_ENTREGA_MAX = 5

# Costos
COSTO_ALMACENAR = 150  # $ por unidad por dia
COSTO_FALTANTE = 380  # $ por unidad
COSTO_PEDIDO_PEQUENO = 40  # $ por unidad si Q < 300
COSTO_PEDIDO_GRANDE = 30  # $ por unidad si Q ≥ 300

# Precios
PRECIO_VENTA = 250

# Tiempo
DIAS_SIMULACION = 5 * 365  # 5 años

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


def costo_unitario_pedido(q):
    """
    Calcula el costo unitario de un pedido según su cantidad.

    Args:
        q (int): Cantidad del pedido.

    Returns:
        float: Costo unitario del pedido.
    """

    return COSTO_PEDIDO_PEQUENO if q < 300 else COSTO_PEDIDO_GRANDE


def imprimir_resultados(resultado):
    print(f"\nPolítica (r={resultado['r']}, Q={resultado['Q']}):")
    print(f"  Ingresos:        ${resultado['ingresos']:.2f}")
    print(f"  Costo almacén:   ${resultado['costo_alm']:.2f}")
    print(f"  Costo faltantes: ${resultado['costo_faltante']:.2f}")
    print(f"  Costo pedidos:   ${resultado['costo_pedidos']:.2f}")
    print(f"  Ganancia neta:   ${resultado['ganancia']:.2f}")


def simular_politica(r, Q):
    """
    Simula la política de inventario dada por (r, Q) durante DIAS_SIMULACION días.

    Args:
        r (int): Nivel de reposición.
        Q (int): Tamaño del lote de reposición.

    Returns:
        dict: Diccionario con los resultados de la simulación.
    """
    inventario = INVENTARIO_INICIAL
    pedidos_pendientes = (
        []
    )  # Lista de pedidos pendientes (tuplas de (día_llegada, cantidad))

    costo_almancenamiento = 0
    costo_faltante = 0
    costo_pedidos = 0
    ingresos = 0

    for dia in range(DIAS_SIMULACION):

        # Llegada de pedidos
        inventario, pedidos_pendientes = procesar_llegada_pedidos(
            dia, inventario, pedidos_pendientes
        )

        # Demanda del día
        demanda = generar_demanda()
        ventas, faltante = calcular_resultados_diarios(demanda, inventario)
        inventario -= ventas

        # Pedidos
        if inventario < r:
            pedidos_pendientes, costo_pedidos = procesar_reposicion(
                dia, Q, pedidos_pendientes, costo_pedidos
            )

        # Registrar métricas
        ingresos += ventas * PRECIO_VENTA
        costo_faltante += faltante * COSTO_FALTANTE
        costo_almancenamiento += inventario * COSTO_ALMACENAR

    costo_total = costo_almancenamiento + costo_faltante + costo_pedidos
    ganancia = ingresos - costo_total

    return {
        "r": r,
        "Q": Q,
        "ingresos": ingresos,
        "costo_alm": costo_almancenamiento,
        "costo_faltante": costo_faltante,
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


if __name__ == "__main__":
    simular()
