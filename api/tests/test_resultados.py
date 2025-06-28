import pytest
from api.src.domain.models.resultados_politica import ResultadosPolitica
from api.src.domain.value_objects.politica_inventario import PoliticaInventario
from api.src.domain.value_objects.configuracion_simulacion import ConfiguracionSimulacion
from api.src.domain.value_objects.precio_venta import PrecioVenta
from api.src.domain.value_objects.costo_faltante import CostoFaltante
from api.src.domain.value_objects.precio import Precio

class TestResultadosPolitica:
    """Tests para la clase ResultadosPolitica."""
    
    def test_crear_resultados_politica(self):
        """Test que verifica que se puede crear un objeto ResultadosPolitica."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        assert resultados.r == 10
        assert resultados.Q == 20
        assert resultados.inventario == 15
        assert resultados.costo_almacenamiento == 0.0
        assert resultados.costo_total_faltante == 0.0
        assert resultados.costo_pedidos == 0.0
        assert resultados.ingresos == 0.0
    
    def test_from_politica_and_config(self):
        """Test que verifica que se puede crear un objeto ResultadosPolitica desde una política y configuración."""
        # Crear política y configuración de prueba
        politica = PoliticaInventario.from_valores(punto_reorden=10, cantidad_pedido=20)
        configuracion = ConfiguracionSimulacion.from_parametros(
            inventario_inicial=15,
            precio_venta=100.0,
            costo_almacenar=1.0,
            costo_faltante=50.0,
            costo_pedido_pequeno=5.0,
            costo_pedido_grande=3.0,
            plazo_entrega_min=1,
            plazo_entrega_max=2,
            demanda_media=10,
            dias_simulacion=30
        )
        
        # Usar el nuevo constructor
        resultados = ResultadosPolitica.from_politica_and_config(politica, configuracion)
        
        # Verificar que se inicializó correctamente
        assert resultados.r == 10  # punto de reorden de la política
        assert resultados.Q == 20  # cantidad de pedido de la política
        assert resultados.inventario == 15  # inventario inicial de la configuración
        assert resultados.costo_almacenamiento == 0.0
        assert resultados.costo_total_faltante == 0.0
        assert resultados.costo_pedidos == 0.0
        assert resultados.ingresos == 0.0
    
    def test_agregar_costo_almacenamiento(self):
        """Test que verifica que se puede agregar costo de almacenamiento."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        resultados.agregar_costo_almacenamiento(5.0)
        assert resultados.costo_almacenamiento == 5.0
        
        resultados.agregar_costo_almacenamiento(3.0)
        assert resultados.costo_almacenamiento == 8.0
    
    def test_agregar_costo_faltante(self):
        """Test que verifica que se puede agregar costo por faltante."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        resultados.agregar_costo_faltante(10.0)
        assert resultados.costo_total_faltante == 10.0
        
        resultados.agregar_costo_faltante(5.0)
        assert resultados.costo_total_faltante == 15.0
    
    def test_agregar_costo_pedido(self):
        """Test que verifica que se puede agregar costo de pedido."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        resultados.agregar_costo_pedido(25.0)
        assert resultados.costo_pedidos == 25.0
        
        resultados.agregar_costo_pedido(15.0)
        assert resultados.costo_pedidos == 40.0
    
    def test_agregar_ingreso(self):
        """Test que verifica que se puede agregar ingreso."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        resultados.agregar_ingreso(100.0)
        assert resultados.ingresos == 100.0
        
        resultados.agregar_ingreso(50.0)
        assert resultados.ingresos == 150.0
    
    def test_actualizar_inventario(self):
        """Test que verifica que se puede actualizar el inventario."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        # Incrementar inventario
        resultados.actualizar_inventario(5)
        assert resultados.inventario == 20
        
        # Decrementar inventario
        resultados.actualizar_inventario(-3)
        assert resultados.inventario == 17
    
    def test_establecer_inventario(self):
        """Test que verifica que se puede establecer el inventario a un valor específico."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        resultados.establecer_inventario(25)
        assert resultados.inventario == 25
    
    def test_obtener_inventario(self):
        """Test que verifica que se puede obtener el nivel actual de inventario."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        assert resultados.obtener_inventario() == 15
    
    def test_calcular_ganancia(self):
        """Test que verifica el cálculo de ganancia."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        # Sin costos ni ingresos
        assert resultados.calcular_ganancia() == 0.0
        
        # Con ingresos pero sin costos
        resultados.agregar_ingreso(200.0)
        assert resultados.calcular_ganancia() == 200.0
        
        # Con ingresos y costos
        resultados.agregar_costo_almacenamiento(20.0)
        resultados.agregar_costo_faltante(10.0)
        resultados.agregar_costo_pedido(30.0)
        
        ganancia_esperada = 200.0 - (20.0 + 10.0 + 30.0)
        assert resultados.calcular_ganancia() == ganancia_esperada
    
    def test_to_dict(self):
        """Test que verifica la conversión a diccionario."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        resultados.agregar_ingreso(200.0)
        resultados.agregar_costo_almacenamiento(20.0)
        resultados.agregar_costo_faltante(10.0)
        resultados.agregar_costo_pedido(30.0)
        
        dict_resultados = resultados.to_dict()
        
        assert dict_resultados["r"] == 10
        assert dict_resultados["Q"] == 20
        assert dict_resultados["ingresos"] == 200.0
        assert dict_resultados["costo_alm"] == 20.0
        assert dict_resultados["costo_faltante"] == 10.0
        assert dict_resultados["costo_pedidos"] == 30.0
        assert dict_resultados["ganancia"] == 140.0  # 200 - (20 + 10 + 30)
    
    def test_resultados_acumulativos(self):
        """Test que verifica que los resultados se acumulan correctamente."""
        resultados = ResultadosPolitica(r=10, Q=20, inventario=15)
        
        # Simular múltiples operaciones
        resultados.agregar_ingreso(100.0)
        resultados.agregar_costo_almacenamiento(5.0)
        resultados.actualizar_inventario(-3)
        
        resultados.agregar_ingreso(50.0)
        resultados.agregar_costo_faltante(10.0)
        resultados.actualizar_inventario(5)
        
        assert resultados.ingresos == 150.0
        assert resultados.costo_almacenamiento == 5.0
        assert resultados.costo_total_faltante == 10.0
        assert resultados.inventario == 17  # 15 - 3 + 5
    
    def test_diferentes_politicas(self):
        """Test que verifica que diferentes políticas mantienen sus parámetros."""
        politica1 = PoliticaInventario.from_valores(punto_reorden=5, cantidad_pedido=15)
        politica2 = PoliticaInventario.from_valores(punto_reorden=20, cantidad_pedido=50)
        configuracion = ConfiguracionSimulacion.from_parametros(
            inventario_inicial=10,
            precio_venta=100.0,
            costo_almacenar=1.0,
            costo_faltante=50.0,
            costo_pedido_pequeno=5.0,
            costo_pedido_grande=3.0,
            plazo_entrega_min=1,
            plazo_entrega_max=2,
            demanda_media=10,
            dias_simulacion=30
        )
        
        resultados1 = ResultadosPolitica.from_politica_and_config(politica1, configuracion)
        resultados2 = ResultadosPolitica.from_politica_and_config(politica2, configuracion)
        
        assert resultados1.r == 5
        assert resultados1.Q == 15
        assert resultados2.r == 20
        assert resultados2.Q == 50
        assert resultados1.inventario == resultados2.inventario == 10 