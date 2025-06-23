import pytest
from api.src.domain.value_objects import PoliticaInventario
from api.src.domain.exceptions import DomainError


class TestPoliticaInventario:
    def test_politica_valida(self):
        politica = PoliticaInventario.from_valores(10, 50)
        assert politica.get_punto_reorden() == 10
        assert politica.get_cantidad_pedido() == 50
        assert str(politica) == "Política (r=10, Q=50)"
    
    def test_politica_con_cantidad_negativa_levanta_excepcion(self):
        with pytest.raises(DomainError, match="La cantidad no puede ser negativa"):
            PoliticaInventario.from_valores(10, -50) 