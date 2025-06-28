import pytest
from api.src.domain.models.evento import Evento, EventoDemanda, EventoLlegadaPedido

class TestEventoBase:
    """Tests para la clase base Evento."""
    
    def test_evento_base_es_abstracta(self):
        """Test que verifica que Evento es una clase abstracta."""
        with pytest.raises(TypeError):
            Evento(dia=1, cantidad=10)

class TestEventoDemanda:
    """Tests para la clase EventoDemanda."""
    
    def test_crear_evento_demanda(self):
        """Test que verifica que se puede crear un evento de demanda."""
        evento = EventoDemanda(dia=1, cantidad=10)
        assert evento.dia == 1
        assert evento.cantidad == 10
        assert evento.get_dia() == 1
        assert evento.get_cantidad() == 10
        assert evento.get_tipo() == "demanda"
    
    def test_str_evento_demanda(self):
        """Test que verifica la representación en string del evento de demanda."""
        evento = EventoDemanda(dia=1, cantidad=10)
        assert str(evento) == "EventoDemanda(dia=1, cantidad=10)"
    
    def test_herencia_evento_demanda(self):
        """Test que verifica que EventoDemanda hereda de Evento."""
        evento = EventoDemanda(dia=1, cantidad=10)
        assert isinstance(evento, Evento)

class TestEventoLlegadaPedido:
    """Tests para la clase EventoLlegadaPedido."""
    
    def test_crear_evento_llegada_pedido(self):
        """Test que verifica que se puede crear un evento de llegada de pedido."""
        evento = EventoLlegadaPedido(dia=2, cantidad=20)
        assert evento.dia == 2
        assert evento.cantidad == 20
        assert evento.get_dia() == 2
        assert evento.get_cantidad() == 20
        assert evento.get_tipo() == "llegada_pedido"
    
    def test_str_evento_llegada_pedido(self):
        """Test que verifica la representación en string del evento de llegada de pedido."""
        evento = EventoLlegadaPedido(dia=2, cantidad=20)
        assert str(evento) == "EventoLlegadaPedido(dia=2, cantidad=20)"
    
    def test_herencia_evento_llegada_pedido(self):
        """Test que verifica que EventoLlegadaPedido hereda de Evento."""
        evento = EventoLlegadaPedido(dia=2, cantidad=20)
        assert isinstance(evento, Evento)

class TestEventoCompatibilidad:
    """Tests para verificar compatibilidad con la interfaz anterior."""
    
    def test_crear_evento_compatibilidad(self):
        """Test que verifica que se puede crear un evento con la interfaz anterior."""
        evento = EventoDemanda(dia=1, cantidad=10)
        assert evento.get_dia() == 1
        assert evento.get_cantidad() == 10
        assert evento.get_tipo() == "demanda"
    
    def test_str_evento_compatibilidad(self):
        """Test que verifica la representación en string."""
        evento = EventoDemanda(dia=1, cantidad=10)
        assert "EventoDemanda" in str(evento)
        assert "dia=1" in str(evento)
        assert "cantidad=10" in str(evento)
    
    def test_herencia_evento_compatibilidad(self):
        """Test que verifica la herencia correcta."""
        evento = EventoDemanda(dia=1, cantidad=10)
        assert isinstance(evento, Evento)
    
    def test_evento_compatibilidad_valor_por_defecto(self):
        """Test que verifica que se pueden crear eventos con valores por defecto."""
        evento = EventoDemanda(dia=1, cantidad=0)
        assert evento.get_dia() == 1
        assert evento.get_cantidad() == 0

class TestEventosIntegracion:
    """Tests de integración para verificar que los eventos funcionan juntos."""
    
    def test_lista_eventos_mixta(self):
        """Test que verifica que se pueden crear listas con diferentes tipos de eventos."""
        eventos = [
            EventoDemanda(dia=1, cantidad=10),
            EventoLlegadaPedido(dia=2, cantidad=20),
            EventoDemanda(dia=3, cantidad=5)
        ]
        
        assert len(eventos) == 3
        assert isinstance(eventos[0], EventoDemanda)
        assert isinstance(eventos[1], EventoLlegadaPedido)
        assert isinstance(eventos[2], EventoDemanda)
    
    def test_tipos_eventos_diferentes(self):
        """Test que verifica que los tipos de eventos son diferentes."""
        evento_demanda = EventoDemanda(dia=1, cantidad=10)
        evento_llegada = EventoLlegadaPedido(dia=1, cantidad=10)
        
        assert evento_demanda.get_tipo() == "demanda"
        assert evento_llegada.get_tipo() == "llegada_pedido"
        assert evento_demanda.get_tipo() != evento_llegada.get_tipo() 