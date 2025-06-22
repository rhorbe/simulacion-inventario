// Configuración de la aplicación
const CONFIG = {
    API_BASE_URL: '/api',
    API_ENDPOINTS: {
        SIMULAR: '/simular'
    },
    DEFAULT_VALUES: {
        inventario_inicial: 720,
        demanda: 200,
        dias_simulacion: 365,
        anios_simulacion: 5,
        plazo_entrega_min: 1,
        plazo_entrega_max: 5,
        costo_almacenar: 150.0,
        costo_faltante: 380.0,
        costo_pedido_pequenio: 40.0,
        costo_pedido_grande: 30.0,
        precio_venta: 250.0
    },
    CHART_COLORS: {
        ingresos: '#28a745',
        costos: '#dc3545',
        ganancia: '#17a2b8',
        almacenamiento: '#ffc107',
        faltante: '#fd7e14',
        pedidos: '#6f42c1'
    },
    VALIDATION: {
        min_inventario: 0,
        min_demanda: 1,
        min_dias: 1,
        min_anios: 1,
        min_plazo: 1,
        min_costos: 0,
        min_precio: 0
    }
}; 