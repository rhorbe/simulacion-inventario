import pytest
from api.src.domain.value_objects import Cantidad
from api.src.domain.exceptions import DomainError


class TestCantidad:
    def test_cantidad_valida(self):
        cantidad = Cantidad.from_int(10)
        assert int(cantidad) == 10
        assert str(cantidad) == "10"
    
    def test_cantidad_cero(self):
        cantidad = Cantidad.from_int(0)
        assert int(cantidad) == 0
    
    def test_cantidad_negativa_levanta_excepcion(self):
        with pytest.raises(DomainError, match="La cantidad no puede ser negativa"):
            Cantidad.from_int(-5) 