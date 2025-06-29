from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.src.infra.controllers import health_controller
from api.src.infra.controllers import simulacion_controller
from api.src.infra.dependency_injection import get_command_bus, get_event_bus
from api.src.application.handlers.simular_command_handler import SimularCommandHandler
from api.src.application.commands.simular_command import SimularCommand
from api.src.application.handlers.demanda_handler import DemandaEventHandler
from api.src.application.handlers.llegada_pedido_handler import LlegadaPedidoEventHandler
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido

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

# Inicialización y registro de handlers en los buses (singleton)
command_bus = get_command_bus()
event_bus = get_event_bus()

# Registrar handlers del EventBus
event_bus.register_handler(EventoDemanda, DemandaEventHandler())
event_bus.register_handler(EventoLlegadaPedido, LlegadaPedidoEventHandler())

# Registrar handler del CommandBus con EventBus como dependencia
command_bus.register_handler(SimularCommand, SimularCommandHandler(event_bus))

# Registrar controladores
app.include_router(health_controller.router, tags=["health"])
app.include_router(simulacion_controller.router, tags=["simulacion"])