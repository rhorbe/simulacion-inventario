import pytest
from api.src.domain.value_objects import CostoPedido
from api.src.domain.exceptions import DomainError


class TestCostoPedido:
    def test_costo_valido(self):
        costo = CostoPedido.from_costos(10.0, 8.0)
        assert costo.get_costo_pedido_pequeno() == 10.0
        assert costo.get_costo_pedido_grande() == 8.0
        assert str(costo) == "Costos de pedido: pequeño=$10.00, grande=$8.00"
    
    def test_costo_pedido_pequeno_negativo_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El costo de pedido pequeño no puede ser negativo"):
            CostoPedido.from_costos(-10.0, 8.0)
    
    def test_costo_pedido_grande_negativo_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El costo de pedido grande no puede ser negativo"):
            CostoPedido.from_costos(10.0, -8.0)
    
    def test_costo_pequeno_igual_grande_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El costo de pedido pequeño debe ser mayor al costo de pedido grande"):
            CostoPedido.from_costos(8.0, 8.0)
    
    def test_costo_pequeno_menor_grande_levanta_excepcion(self):
        with pytest.raises(DomainError, match="El costo de pedido pequeño debe ser mayor al costo de pedido grande"):
            CostoPedido.from_costos(5.0, 8.0)
    
    def test_calcular_costo_unitario_pedido_pequeno(self):
        costo = CostoPedido.from_costos(10.0, 8.0)
        assert costo.calcular_costo_unitario(100) == 10.0  # Pedido pequeño (< 300)
    
    def test_calcular_costo_unitario_pedido_grande(self):
        costo = CostoPedido.from_costos(10.0, 8.0)
        assert costo.calcular_costo_unitario(400) == 8.0  # Pedido grande (>= 300) 