from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.infra.controllers import health_controller, simulacion_controller

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

# Registrar controladores
app.include_router(health_controller.router, tags=["health"])
app.include_router(simulacion_controller.router, tags=["simulacion"])