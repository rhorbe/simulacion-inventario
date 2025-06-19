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
DIAS_SIMULACION = 365
ANIOS_SIMULACION = 5

POLITICAS_ABASTECIMIENTO = [
    {"punto_reorden": 40, "cantidad_pedido": 140},  # politica actual
    {"punto_reorden": 30, "cantidad_pedido": 140},
    {"punto_reorden": 60, "cantidad_pedido": 140},
    {"punto_reorden": 40, "cantidad_pedido": 100},
    {"punto_reorden": 40, "cantidad_pedido": 200},
    {"punto_reorden": 50, "cantidad_pedido": 180},
]
