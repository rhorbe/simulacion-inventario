from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint de health check para verificar que la API está funcionando."""
    return {"status": "ok", "message": "API de Simulación de Inventario funcionando correctamente"} 