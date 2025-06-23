import pytest
from api.src.domain.value_objects import PlazoDeEntrega
from api.src.domain.exceptions import DomainError


class TestPlazoDeEntrega:
    def test_plazo_valido(self):
        plazo = PlazoDeEntrega.from_plazos(1, 5)
        assert plazo.get_plazo_minimo() == 1
        assert plazo.get_plazo_maximo() == 5
        assert str(plazo) == "Plazo de entrega: 1-5 días"
    
    def test_plazo_minimo_igual_maximo(self):
        plazo = PlazoDeEntrega.from_plazos(3, 3)
        assert plazo.get_plazo_minimo() == 3
        assert plazo.get_plazo_maximo() == 3
    
    def test_plazo_minimo_negativo_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El plazo mínimo de entrega no puede ser negativo"):
            PlazoDeEntrega.from_plazos(-1, 5)
    
    def test_plazo_maximo_negativo_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El plazo máximo de entrega no puede ser negativo"):
            PlazoDeEntrega.from_plazos(1, -5)
    
    def test_plazo_maximo_menor_minimo_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El plazo máximo de entrega no puede ser menor al plazo mínimo"):
            PlazoDeEntrega.from_plazos(5, 1) 