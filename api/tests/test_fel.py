import pytest
from api.src.domain.models.fel import FEL
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido

class TestFEL:
    """Tests para la clase FEL (Future Event List)."""
    
    def test_crear_fel_vacia(self):
        """Test que verifica que se puede crear una FEL vacía."""
        fel = FEL()
        
        assert fel.hay_eventos() == False
        assert fel.obtener_cantidad_eventos() == 0
        assert fel.obtener_siguiente_evento() is None
        assert str(fel) == "FEL: []"
    
    def test_agregar_evento(self):
        """Test que verifica que se puede agregar un evento a la FEL."""
        fel = FEL()
        evento = EventoDemanda(dia=5, cantidad=10)
        
        fel.agregar_evento(evento)
        
        assert fel.hay_eventos() == True
        assert fel.obtener_cantidad_eventos() == 1
    
    def test_obtener_siguiente_evento(self):
        """Test que verifica que se puede obtener el siguiente evento."""
        fel = FEL()
        evento = EventoDemanda(dia=5, cantidad=10)
        
        fel.agregar_evento(evento)
        evento_obtenido = fel.obtener_siguiente_evento()
        
        assert evento_obtenido == evento
        assert fel.hay_eventos() == False
        assert fel.obtener_cantidad_eventos() == 0
    
    def test_ordenamiento_automatico(self):
        """Test que verifica que los eventos se ordenan automáticamente por día."""
        fel = FEL()
        
        # Agregar eventos en orden desordenado
        evento3 = EventoDemanda(dia=3, cantidad=10)
        evento1 = EventoDemanda(dia=1, cantidad=5)
        evento2 = EventoDemanda(dia=2, cantidad=8)
        
        fel.agregar_evento(evento3)
        fel.agregar_evento(evento1)
        fel.agregar_evento(evento2)
        
        # Verificar que se obtienen en orden cronológico
        assert fel.obtener_siguiente_evento() == evento1  # día 1
        assert fel.obtener_siguiente_evento() == evento2  # día 2
        assert fel.obtener_siguiente_evento() == evento3  # día 3
        assert fel.obtener_siguiente_evento() is None
    
    def test_hay_eventos_futuros_en_dia(self):
        """Test que verifica la función hay_eventos_futuros_en_dia."""
        fel = FEL()
        
        # Sin eventos
        assert fel.hay_eventos_futuros_en_dia(5) == False
        
        # Con eventos
        fel.agregar_evento(EventoDemanda(dia=3, cantidad=10))
        fel.agregar_evento(EventoDemanda(dia=7, cantidad=15))
        
        assert fel.hay_eventos_futuros_en_dia(2) == True   # Hay eventos después del día 2
        assert fel.hay_eventos_futuros_en_dia(3) == True   # Hay eventos en el día 3
        assert fel.hay_eventos_futuros_en_dia(5) == True   # Hay eventos después del día 5
        assert fel.hay_eventos_futuros_en_dia(7) == True   # Hay eventos en el día 7
        assert fel.hay_eventos_futuros_en_dia(8) == False  # No hay eventos después del día 8
    
    def test_obtener_proximo_dia_evento(self):
        """Test que verifica la función obtener_proximo_dia_evento."""
        fel = FEL()
        
        # Sin eventos
        assert fel.obtener_proximo_dia_evento() is None
        
        # Con eventos
        fel.agregar_evento(EventoDemanda(dia=5, cantidad=10))
        fel.agregar_evento(EventoDemanda(dia=3, cantidad=8))
        
        assert fel.obtener_proximo_dia_evento() == 3  # El evento más temprano
        assert fel.obtener_cantidad_eventos() == 2    # No se removió ningún evento
    
    def test_limpiar(self):
        """Test que verifica que se puede limpiar la FEL."""
        fel = FEL()
        
        fel.agregar_evento(EventoDemanda(dia=1, cantidad=10))
        fel.agregar_evento(EventoDemanda(dia=2, cantidad=15))
        
        assert fel.obtener_cantidad_eventos() == 2
        
        fel.limpiar()
        
        assert fel.obtener_cantidad_eventos() == 0
        assert fel.hay_eventos() == False
        assert fel.obtener_siguiente_evento() is None
    
    def test_diferentes_tipos_eventos(self):
        """Test que verifica que se pueden manejar diferentes tipos de eventos."""
        fel = FEL()
        
        evento_demanda = EventoDemanda(dia=1, cantidad=10)
        evento_llegada = EventoLlegadaPedido(dia=2, cantidad=50)
        
        fel.agregar_evento(evento_llegada)  # Evento más tarde
        fel.agregar_evento(evento_demanda)  # Evento más temprano
        
        # Verificar que se obtienen en orden cronológico
        primer_evento = fel.obtener_siguiente_evento()
        segundo_evento = fel.obtener_siguiente_evento()
        
        assert primer_evento == evento_demanda
        assert segundo_evento == evento_llegada
        assert isinstance(primer_evento, EventoDemanda)
        assert isinstance(segundo_evento, EventoLlegadaPedido)
    
    def test_str_representacion(self):
        """Test que verifica la representación en string de la FEL."""
        fel = FEL()
        
        # FEL vacía
        assert str(fel) == "FEL: []"
        
        # FEL con eventos
        fel.agregar_evento(EventoDemanda(dia=1, cantidad=10))
        fel.agregar_evento(EventoLlegadaPedido(dia=2, cantidad=50))
        
        str_fel = str(fel)
        assert "FEL: [" in str_fel
        assert "demanda(día=1)" in str_fel
        assert "llegada_pedido(día=2)" in str_fel
    
    def test_len_operator(self):
        """Test que verifica el operador len."""
        fel = FEL()
        
        assert len(fel) == 0
        
        fel.agregar_evento(EventoDemanda(dia=1, cantidad=10))
        assert len(fel) == 1
        
        fel.agregar_evento(EventoDemanda(dia=2, cantidad=15))
        assert len(fel) == 2
        
        fel.obtener_siguiente_evento()
        assert len(fel) == 1
    
    def test_comportamiento_con_eventos_duplicados(self):
        """Test que verifica el comportamiento con eventos en el mismo día."""
        fel = FEL()
        
        evento1 = EventoDemanda(dia=5, cantidad=10)
        evento2 = EventoLlegadaPedido(dia=5, cantidad=20)
        
        fel.agregar_evento(evento1)
        fel.agregar_evento(evento2)
        
        # Ambos eventos están en el mismo día, se mantiene el orden de inserción
        assert fel.obtener_cantidad_eventos() == 2
        
        primer_evento = fel.obtener_siguiente_evento()
        segundo_evento = fel.obtener_siguiente_evento()
        
        assert primer_evento.get_dia() == 5
        assert segundo_evento.get_dia() == 5 