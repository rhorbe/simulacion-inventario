from typing import Optional

from pydantic import BaseModel


class PoliticaAbastecimiento(BaseModel):
    punto_reorden: Optional[int] = None
    cantidad_pedido: int
