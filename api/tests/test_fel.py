import pytest
from api.src.domain.models.fel import FEL
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido

class TestFEL:
    """Tests para la clase FEL (Future Event List)."""
    
    def test_crear_fel_vacia(self):
        """Test que verifica que se puede crear una FEL vacía."""
        fel = FEL()
        assert not fel.hay_eventos()
    
    def test_crear_fel_con_eventos_iniciales(self):
        """Test que verifica que se puede crear una FEL con eventos iniciales."""
        evento1 = EventoDemanda(dia=5, cantidad=10)
        evento2 = EventoDemanda(dia=1, cantidad=5)
        evento3 = EventoLlegadaPedido(dia=3, cantidad=20)
        
        eventos_iniciales = [evento1, evento2, evento3]
        fel = FEL(eventos_iniciales)
        
        assert fel.hay_eventos()

    def test_crear_fel_con_lista_vacia(self):
        """Test que verifica que se puede crear una FEL con una lista vacía."""
        fel = FEL([])
        assert not fel.hay_eventos()
    
    def test_crear_fel_con_none(self):
        """Test que verifica que se puede crear una FEL con None (equivalente a lista vacía)."""
        fel = FEL(None)
        assert not fel.hay_eventos()
    
    def test_eventos_iniciales_no_modifican_lista_original(self):
        """Test que verifica que la lista original no se modifica al crear la FEL."""
        evento1 = EventoDemanda(dia=1, cantidad=10)
        evento2 = EventoDemanda(dia=2, cantidad=5)
        
        eventos_originales = [evento1, evento2]
        fel = FEL(eventos_originales)
        
        # Modificar la FEL
        fel.agregar_evento(EventoLlegadaPedido(dia=3, cantidad=15))
        
        # Verificar que la lista original no cambió
        assert len(eventos_originales) == 2
        assert eventos_originales[0] == evento1
        assert eventos_originales[1] == evento2
    
    def test_agregar_evento(self):
        """Test que verifica que se puede agregar un evento a una FEL vacía."""
        fel = FEL()
        evento = EventoDemanda(dia=1, cantidad=10)
        
        fel.agregar_evento(evento)
        
        assert fel.hay_eventos()

    def test_obtener_evento_actual(self):
        """Test que verifica que se obtiene el evento actual correctamente."""
        evento1 = EventoDemanda(dia=5, cantidad=10)
        evento2 = EventoDemanda(dia=1, cantidad=5)
        
        fel = FEL([evento1, evento2])
        
        # El primer evento debe ser el del día 1 (ordenado)
        primer_evento = fel.obtener_evento_actual()
        assert primer_evento.get_dia() == 1
        
        # El segundo evento debe ser el del día 5
        segundo_evento = fel.obtener_evento_actual()
        assert segundo_evento.get_dia() == 5
        
        # No hay más eventos
        assert not fel.hay_eventos()
    
    def test_ordenamiento_automatico(self):
        """Test que verifica que los eventos se ordenan automáticamente."""
        evento1 = EventoDemanda(dia=10, cantidad=10)
        evento2 = EventoDemanda(dia=1, cantidad=5)
        evento3 = EventoLlegadaPedido(dia=5, cantidad=20)
        
        fel = FEL([evento1, evento2, evento3])
        
        # Los eventos deben salir en orden: 1, 5, 10
        assert fel.obtener_evento_actual().get_dia() == 1
        assert fel.obtener_evento_actual().get_dia() == 5
        assert fel.obtener_evento_actual().get_dia() == 10
    
    def test_hay_eventos_futuros_en_dia(self):
        """Test que verifica la función hay_eventos_futuros_en_dia."""
        evento1 = EventoDemanda(dia=5, cantidad=10)
        evento2 = EventoDemanda(dia=10, cantidad=5)
        
        fel = FEL([evento1, evento2])
        
        assert fel.hay_eventos_futuros_en_dia(1)   # Hay eventos después del día 1 (días 5 y 10)
        assert fel.hay_eventos_futuros_en_dia(3)   # Hay eventos después del día 3 (días 5 y 10)
        assert fel.hay_eventos_futuros_en_dia(5)   # Hay evento en día 5
        assert fel.hay_eventos_futuros_en_dia(7)   # Hay evento después del día 7 (día 10)
        assert fel.hay_eventos_futuros_en_dia(10)  # Hay evento en día 10
        assert not fel.hay_eventos_futuros_en_dia(15)  # No hay eventos después del día 15
    
    def test_diferentes_tipos_eventos(self):
        """Test que verifica que se pueden manejar diferentes tipos de eventos."""
        evento_demanda = EventoDemanda(dia=1, cantidad=10)
        evento_llegada = EventoLlegadaPedido(dia=2, cantidad=20)
        
        fel = FEL([evento_demanda, evento_llegada])
        
        # Verificar que se pueden obtener ambos tipos
        primer_evento = fel.obtener_evento_actual()
        assert isinstance(primer_evento, EventoDemanda)
        
        segundo_evento = fel.obtener_evento_actual()
        assert isinstance(segundo_evento, EventoLlegadaPedido)
    
    def test_obtener_evento_actual_sin_eventos(self):
        """Test que verifica que obtener_evento_actual lanza excepción si no hay eventos."""
        fel = FEL()
        
        with pytest.raises(ValueError, match="No hay eventos disponibles en la FEL"):
            fel.obtener_evento_actual() 