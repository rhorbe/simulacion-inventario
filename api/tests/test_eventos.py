import pytest
from api.src.domain.models.evento import EventoBase, EventoDemanda, EventoLlegadaPedido, Evento

class TestEventoBase:
    """Tests para la clase base abstracta de eventos."""
    
    def test_evento_base_es_abstracta(self):
        """Test que verifica que EventoBase es una clase abstracta."""
        with pytest.raises(TypeError):
            EventoBase()

class TestEventoDemanda:
    """Tests para el evento de demanda."""
    
    def test_crear_evento_demanda(self):
        """Test que verifica que se puede crear un evento de demanda."""
        evento = EventoDemanda(dia=5, cantidad=10)
        
        assert evento.get_dia() == 5
        assert evento.get_cantidad() == 10
        assert evento.get_tipo() == "demanda"
    
    def test_str_evento_demanda(self):
        """Test que verifica la representación en string del evento de demanda."""
        evento = EventoDemanda(dia=5, cantidad=10)
        str_evento = str(evento)
        
        assert "EventoDemanda" in str_evento
        assert "dia=5" in str_evento
        assert "cantidad=10" in str_evento
    
    def test_herencia_evento_demanda(self):
        """Test que verifica que EventoDemanda hereda de EventoBase."""
        evento = EventoDemanda(dia=5, cantidad=10)
        
        assert isinstance(evento, EventoBase)
        assert isinstance(evento, EventoDemanda)

class TestEventoLlegadaPedido:
    """Tests para el evento de llegada de pedido."""
    
    def test_crear_evento_llegada_pedido(self):
        """Test que verifica que se puede crear un evento de llegada de pedido."""
        evento = EventoLlegadaPedido(dia=10, cantidad=50)
        
        assert evento.get_dia() == 10
        assert evento.get_cantidad() == 50
        assert evento.get_tipo() == "llegada_pedido"
    
    def test_str_evento_llegada_pedido(self):
        """Test que verifica la representación en string del evento de llegada de pedido."""
        evento = EventoLlegadaPedido(dia=10, cantidad=50)
        str_evento = str(evento)
        
        assert "EventoLlegadaPedido" in str_evento
        assert "dia=10" in str_evento
        assert "cantidad=50" in str_evento
    
    def test_herencia_evento_llegada_pedido(self):
        """Test que verifica que EventoLlegadaPedido hereda de EventoBase."""
        evento = EventoLlegadaPedido(dia=10, cantidad=50)
        
        assert isinstance(evento, EventoBase)
        assert isinstance(evento, EventoLlegadaPedido)

class TestEventoCompatibilidad:
    """Tests para la clase Evento de compatibilidad."""
    
    def test_crear_evento_compatibilidad(self):
        """Test que verifica que se puede crear un evento de compatibilidad."""
        evento = Evento(tipo="demanda", dia=5, cantidad=10)
        
        assert evento.get_dia() == 5
        assert evento.get_cantidad() == 10
        assert evento.get_tipo() == "demanda"
    
    def test_str_evento_compatibilidad(self):
        """Test que verifica la representación en string del evento de compatibilidad."""
        evento = Evento(tipo="llegada_pedido", dia=10, cantidad=50)
        str_evento = str(evento)
        
        assert "Evento" in str_evento
        assert "tipo=llegada_pedido" in str_evento
        assert "dia=10" in str_evento
        assert "cantidad=50" in str_evento
    
    def test_herencia_evento_compatibilidad(self):
        """Test que verifica que Evento hereda de EventoBase."""
        evento = Evento(tipo="demanda", dia=5, cantidad=10)
        
        assert isinstance(evento, EventoBase)
        assert isinstance(evento, Evento)
    
    def test_evento_compatibilidad_valor_por_defecto(self):
        """Test que verifica que el valor por defecto de cantidad funciona."""
        evento = Evento(tipo="demanda", dia=5)
        
        assert evento.get_cantidad() == 0

class TestEventosIntegracion:
    """Tests de integración para verificar que los eventos funcionan juntos."""
    
    def test_lista_eventos_mixta(self):
        """Test que verifica que se pueden mezclar diferentes tipos de eventos en una lista."""
        eventos = [
            EventoDemanda(dia=1, cantidad=10),
            EventoLlegadaPedido(dia=2, cantidad=50),
            Evento(tipo="demanda", dia=3, cantidad=15)
        ]
        
        # Verificar que todos heredan de EventoBase
        for evento in eventos:
            assert isinstance(evento, EventoBase)
        
        # Verificar que se pueden ordenar por día
        eventos_ordenados = sorted(eventos, key=lambda x: x.get_dia())
        dias = [evento.get_dia() for evento in eventos_ordenados]
        assert dias == [1, 2, 3]
    
    def test_tipos_eventos_diferentes(self):
        """Test que verifica que los tipos de eventos son diferentes."""
        evento_demanda = EventoDemanda(dia=1, cantidad=10)
        evento_llegada = EventoLlegadaPedido(dia=1, cantidad=10)
        
        assert evento_demanda.get_tipo() != evento_llegada.get_tipo()
        assert evento_demanda.get_tipo() == "demanda"
        assert evento_llegada.get_tipo() == "llegada_pedido" 