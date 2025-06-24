import pytest
from api.src.domain.models.fel import FEL
from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido

class TestFEL:
    """Tests para la clase FEL (Future Event List)."""
    
    def test_crear_fel_vacia(self):
        """Test que verifica que se puede crear una FEL vacía."""
        fel = FEL()
        assert len(fel) == 0
        assert not fel.hay_eventos()
    
    def test_crear_fel_con_eventos_iniciales(self):
        """Test que verifica que se puede crear una FEL con eventos iniciales."""
        evento1 = EventoDemanda(dia=5, cantidad=10)
        evento2 = EventoDemanda(dia=1, cantidad=5)
        evento3 = EventoLlegadaPedido(dia=3, cantidad=20)
        
        eventos_iniciales = [evento1, evento2, evento3]
        fel = FEL(eventos_iniciales)
        
        assert len(fel) == 3
        assert fel.hay_eventos()
        
        # Verificar que los eventos están ordenados por día
        primer_evento = fel.obtener_siguiente_evento()
        assert primer_evento.get_dia() == 1  # El evento del día 1 debe ser el primero
        
        segundo_evento = fel.obtener_siguiente_evento()
        assert segundo_evento.get_dia() == 3  # El evento del día 3 debe ser el segundo
        
        tercer_evento = fel.obtener_siguiente_evento()
        assert tercer_evento.get_dia() == 5  # El evento del día 5 debe ser el tercero
    
    def test_crear_fel_con_lista_vacia(self):
        """Test que verifica que se puede crear una FEL con una lista vacía."""
        fel = FEL([])
        assert len(fel) == 0
        assert not fel.hay_eventos()
    
    def test_crear_fel_con_none(self):
        """Test que verifica que se puede crear una FEL con None (equivalente a lista vacía)."""
        fel = FEL(None)
        assert len(fel) == 0
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
        
        assert len(fel) == 1
        assert fel.hay_eventos()
        
        evento_obtenido = fel.obtener_siguiente_evento()
        assert evento_obtenido == evento
    
    def test_obtener_siguiente_evento(self):
        """Test que verifica que se obtiene el próximo evento correctamente."""
        evento1 = EventoDemanda(dia=5, cantidad=10)
        evento2 = EventoDemanda(dia=1, cantidad=5)
        
        fel = FEL([evento1, evento2])
        
        # El primer evento debe ser el del día 1 (ordenado)
        primer_evento = fel.obtener_siguiente_evento()
        assert primer_evento.get_dia() == 1
        assert len(fel) == 1
        
        # El segundo evento debe ser el del día 5
        segundo_evento = fel.obtener_siguiente_evento()
        assert segundo_evento.get_dia() == 5
        assert len(fel) == 0
        assert not fel.hay_eventos()
    
    def test_ordenamiento_automatico(self):
        """Test que verifica que los eventos se ordenan automáticamente."""
        evento1 = EventoDemanda(dia=10, cantidad=10)
        evento2 = EventoDemanda(dia=1, cantidad=5)
        evento3 = EventoLlegadaPedido(dia=5, cantidad=20)
        
        fel = FEL([evento1, evento2, evento3])
        
        # Los eventos deben salir en orden: 1, 5, 10
        assert fel.obtener_siguiente_evento().get_dia() == 1
        assert fel.obtener_siguiente_evento().get_dia() == 5
        assert fel.obtener_siguiente_evento().get_dia() == 10
    
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
    
    def test_obtener_proximo_dia_evento(self):
        """Test que verifica la función obtener_proximo_dia_evento."""
        evento1 = EventoDemanda(dia=5, cantidad=10)
        evento2 = EventoDemanda(dia=1, cantidad=5)
        
        fel = FEL([evento1, evento2])
        
        # Debe retornar el día del próximo evento (1) sin removerlo
        proximo_dia = fel.obtener_proximo_dia_evento()
        assert proximo_dia == 1
        assert len(fel) == 2  # La cantidad no cambió
        
        # Después de obtener el evento, el próximo día debe ser 5
        fel.obtener_siguiente_evento()
        proximo_dia = fel.obtener_proximo_dia_evento()
        assert proximo_dia == 5
    
    def test_limpiar(self):
        """Test que verifica la función limpiar."""
        evento1 = EventoDemanda(dia=1, cantidad=10)
        evento2 = EventoDemanda(dia=2, cantidad=5)
        
        fel = FEL([evento1, evento2])
        assert len(fel) == 2
        
        fel.limpiar()
        assert len(fel) == 0
        assert not fel.hay_eventos()
    
    def test_obtener_cantidad_eventos(self):
        """Test que verifica la función obtener_cantidad_eventos."""
        evento1 = EventoDemanda(dia=1, cantidad=10)
        evento2 = EventoDemanda(dia=2, cantidad=5)
        
        fel = FEL([evento1, evento2])
        assert fel.obtener_cantidad_eventos() == 2
        
        fel.obtener_siguiente_evento()
        assert fel.obtener_cantidad_eventos() == 1
        
        fel.obtener_siguiente_evento()
        assert fel.obtener_cantidad_eventos() == 0
    
    def test_diferentes_tipos_eventos(self):
        """Test que verifica que se pueden manejar diferentes tipos de eventos."""
        evento_demanda = EventoDemanda(dia=1, cantidad=10)
        evento_llegada = EventoLlegadaPedido(dia=2, cantidad=20)
        
        fel = FEL([evento_demanda, evento_llegada])
        
        assert len(fel) == 2
        
        # Verificar que se pueden obtener ambos tipos
        primer_evento = fel.obtener_siguiente_evento()
        assert isinstance(primer_evento, EventoDemanda)
        
        segundo_evento = fel.obtener_siguiente_evento()
        assert isinstance(segundo_evento, EventoLlegadaPedido)
    
    def test_str_representacion(self):
        """Test que verifica la representación en string de la FEL."""
        # FEL vacía
        fel_vacia = FEL()
        assert str(fel_vacia) == "FEL: []"
        
        # FEL con eventos
        evento1 = EventoDemanda(dia=1, cantidad=10)
        evento2 = EventoLlegadaPedido(dia=2, cantidad=20)
        
        fel = FEL([evento1, evento2])
        str_representacion = str(fel)
        
        assert "FEL: [" in str_representacion
        assert "demanda(día=1)" in str_representacion
        assert "llegada_pedido(día=2)" in str_representacion
    
    def test_len_operator(self):
        """Test que verifica el operador len."""
        evento1 = EventoDemanda(dia=1, cantidad=10)
        evento2 = EventoDemanda(dia=2, cantidad=5)
        
        fel = FEL([evento1, evento2])
        assert len(fel) == 2
        
        fel.obtener_siguiente_evento()
        assert len(fel) == 1
        
        fel.obtener_siguiente_evento()
        assert len(fel) == 0
    
    def test_comportamiento_con_eventos_duplicados(self):
        """Test que verifica el comportamiento con eventos en el mismo día."""
        evento1 = EventoDemanda(dia=1, cantidad=10)
        evento2 = EventoLlegadaPedido(dia=1, cantidad=20)
        evento3 = EventoDemanda(dia=1, cantidad=5)
        
        fel = FEL([evento1, evento2, evento3])
        
        # Todos los eventos del día 1 deben ser procesados
        assert len(fel) == 3
        
        # Los eventos se mantienen en el orden original para el mismo día
        # (el ordenamiento es estable)
        primer_evento = fel.obtener_siguiente_evento()
        segundo_evento = fel.obtener_siguiente_evento()
        tercer_evento = fel.obtener_siguiente_evento()
        
        assert primer_evento.get_dia() == 1
        assert segundo_evento.get_dia() == 1
        assert tercer_evento.get_dia() == 1 