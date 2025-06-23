import pytest
from api.src.domain.value_objects import Precio
from api.src.domain.exceptions import DomainError


class TestPrecio:
    def test_precio_valido(self):
        precio = Precio.from_float(10.50)
        assert float(precio) == 10.50
        assert str(precio) == "$10.50"
    
    def test_precio_cero(self):
        precio = Precio.from_float(0.0)
        assert float(precio) == 0.0
    
    def test_precio_negativo_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El precio no puede ser negativo"):
            Precio.from_float(-5.0) 