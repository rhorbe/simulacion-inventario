from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.src.infra.controllers import health_controller, simulacion_controller
from api.src.infra.dependency_injection import get_config, get_command_bus, get_event_bus
from api.src.domain.models.command import SimularCommand
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido
from api.src.application.handlers.demanda_handler import DemandaEventHandler
from api.src.application.handlers.llegada_pedido_handler import LlegadaPedidoEventHandler
from api.src.application.handlers.simular_command_handler import SimularCommandHandler
from api.src.infra.bus.middlewares import LoggingMiddleware

app = FastAPI(title="API de Simulación de Inventario", version="1.0.0")

# Configuración de CORS más permisiva para desarrollo
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    # Obtener los buses globales
    command_bus = get_command_bus()
    event_bus = get_event_bus()
    
    # Agregar middleware de logging
    logging_middleware = LoggingMiddleware("simulacion_inventario")
    command_bus.add_middleware(logging_middleware)
    event_bus.add_middleware(logging_middleware)
    
    # Registrar handlers de eventos
    event_bus.register_handler(EventoDemanda, DemandaEventHandler())
    event_bus.register_handler(EventoLlegadaPedido, LlegadaPedidoEventHandler())
    
    # Registrar handlers de comandos
    command_bus.register_handler(SimularCommand, SimularCommandHandler(event_bus))
    
    print("🚀 API de Simulación de Inventario iniciada correctamente")

# Registrar controladores
app.include_router(health_controller.router, tags=["health"])
app.include_router(simulacion_controller.router, tags=["simulacion"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)