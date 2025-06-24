import pytest
from api.src.domain.models.resultados_politica import ResultadosPolitica

class TestResultadosPolitica:
    """Tests para la clase ResultadosPolitica."""
    
    def test_crear_resultados_politica(self):
        """Test que verifica que se puede crear un objeto ResultadosPolitica."""
        resultados = ResultadosPolitica(r=10, Q=50, inventario=20)
        
        assert resultados.r == 10
        assert resultados.Q == 50
        assert resultados.inventario == 20
        assert resultados.costo_almacenamiento == 0.0
        assert resultados.costo_total_faltante == 0.0
        assert resultados.costo_pedidos == 0.0
        assert resultados.ingresos == 0.0
    
    def test_agregar_costo_almacenamiento(self):
        """Test que verifica que se puede agregar costo de almacenamiento."""
        resultados = ResultadosPolitica(r=5, Q=20, inventario=15)
        
        resultados.agregar_costo_almacenamiento(10.5)
        assert resultados.costo_almacenamiento == 10.5
        
        resultados.agregar_costo_almacenamiento(5.2)
        assert resultados.costo_almacenamiento == 15.7
    
    def test_agregar_costo_faltante(self):
        """Test que verifica que se puede agregar costo por faltante."""
        resultados = ResultadosPolitica(r=15, Q=30, inventario=25)
        
        resultados.agregar_costo_faltante(25.0)
        assert resultados.costo_total_faltante == 25.0
        
        resultados.agregar_costo_faltante(15.5)
        assert resultados.costo_total_faltante == 40.5
    
    def test_agregar_costo_pedido(self):
        """Test que verifica que se puede agregar costo de pedido."""
        resultados = ResultadosPolitica(r=8, Q=25, inventario=12)
        
        resultados.agregar_costo_pedido(100.0)
        assert resultados.costo_pedidos == 100.0
        
        resultados.agregar_costo_pedido(50.0)
        assert resultados.costo_pedidos == 150.0
    
    def test_agregar_ingreso(self):
        """Test que verifica que se puede agregar ingreso."""
        resultados = ResultadosPolitica(r=12, Q=40, inventario=18)
        
        resultados.agregar_ingreso(200.0)
        assert resultados.ingresos == 200.0
        
        resultados.agregar_ingreso(75.5)
        assert resultados.ingresos == 275.5
    
    def test_actualizar_inventario(self):
        """Test que verifica que se puede actualizar el inventario."""
        resultados = ResultadosPolitica(r=10, Q=50, inventario=20)
        
        # Incrementar inventario
        resultados.actualizar_inventario(10)
        assert resultados.inventario == 30
        
        # Decrementar inventario
        resultados.actualizar_inventario(-5)
        assert resultados.inventario == 25
        
        # Decrementar más del disponible
        resultados.actualizar_inventario(-30)
        assert resultados.inventario == -5
    
    def test_establecer_inventario(self):
        """Test que verifica que se puede establecer el inventario a un valor específico."""
        resultados = ResultadosPolitica(r=10, Q=50, inventario=20)
        
        resultados.establecer_inventario(100)
        assert resultados.inventario == 100
        
        resultados.establecer_inventario(0)
        assert resultados.inventario == 0
        
        resultados.establecer_inventario(-10)
        assert resultados.inventario == -10
    
    def test_obtener_inventario(self):
        """Test que verifica que se puede obtener el nivel actual de inventario."""
        resultados = ResultadosPolitica(r=10, Q=50, inventario=20)
        
        assert resultados.obtener_inventario() == 20
        
        resultados.actualizar_inventario(10)
        assert resultados.obtener_inventario() == 30
    
    def test_calcular_ganancia(self):
        """Test que verifica el cálculo de ganancia."""
        resultados = ResultadosPolitica(r=10, Q=50, inventario=20)
        
        # Sin costos ni ingresos
        assert resultados.calcular_ganancia() == 0.0
        
        # Con ingresos pero sin costos
        resultados.agregar_ingreso(1000.0)
        assert resultados.calcular_ganancia() == 1000.0
        
        # Con ingresos y costos
        resultados.agregar_costo_almacenamiento(100.0)
        resultados.agregar_costo_faltante(50.0)
        resultados.agregar_costo_pedido(200.0)
        
        ganancia_esperada = 1000.0 - (100.0 + 50.0 + 200.0)
        assert resultados.calcular_ganancia() == ganancia_esperada
    
    def test_to_dict(self):
        """Test que verifica la conversión a diccionario."""
        resultados = ResultadosPolitica(r=10, Q=50, inventario=20)
        resultados.agregar_ingreso(1000.0)
        resultados.agregar_costo_almacenamiento(100.0)
        resultados.agregar_costo_faltante(50.0)
        resultados.agregar_costo_pedido(200.0)
        
        dict_resultado = resultados.to_dict()
        
        assert dict_resultado["r"] == 10
        assert dict_resultado["Q"] == 50
        assert dict_resultado["ingresos"] == 1000.0
        assert dict_resultado["costo_alm"] == 100.0
        assert dict_resultado["costo_faltante"] == 50.0
        assert dict_resultado["costo_pedidos"] == 200.0
        assert dict_resultado["ganancia"] == 650.0  # 1000 - (100 + 50 + 200)
    
    def test_resultados_acumulativos(self):
        """Test que verifica que los resultados se acumulan correctamente."""
        resultados = ResultadosPolitica(r=5, Q=15, inventario=10)
        
        # Simular múltiples operaciones
        for i in range(5):
            resultados.agregar_ingreso(100.0)
            resultados.agregar_costo_almacenamiento(10.0)
            resultados.agregar_costo_faltante(5.0)
            resultados.agregar_costo_pedido(20.0)
            resultados.actualizar_inventario(2)  # Incrementar inventario
        
        assert resultados.ingresos == 500.0
        assert resultados.costo_almacenamiento == 50.0
        assert resultados.costo_total_faltante == 25.0
        assert resultados.costo_pedidos == 100.0
        assert resultados.inventario == 20  # 10 + (5 * 2)
        
        ganancia_esperada = 500.0 - (50.0 + 25.0 + 100.0)
        assert resultados.calcular_ganancia() == ganancia_esperada
    
    def test_diferentes_politicas(self):
        """Test que verifica que diferentes políticas mantienen sus parámetros."""
        resultados1 = ResultadosPolitica(r=10, Q=50, inventario=20)
        resultados2 = ResultadosPolitica(r=20, Q=100, inventario=40)
        
        assert resultados1.r == 10
        assert resultados1.Q == 50
        assert resultados1.inventario == 20
        assert resultados2.r == 20
        assert resultados2.Q == 100
        assert resultados2.inventario == 40
        
        # Verificar que los parámetros se mantienen en el diccionario
        dict1 = resultados1.to_dict()
        dict2 = resultados2.to_dict()
        
        assert dict1["r"] == 10
        assert dict1["Q"] == 50
        assert dict2["r"] == 20
        assert dict2["Q"] == 100 