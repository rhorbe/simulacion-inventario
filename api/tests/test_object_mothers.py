import pytest
import numpy as np
from api.src.domain.object_mothers import DemandaMother, TiempoEntregaMother

class TestDemandaMother:
    """Tests para el Object Mother de demandas."""
    
    def test_generar_demanda_con_semilla_fija(self):
        """Test que verifica que la demanda se genera correctamente con semilla fija."""
        demanda = DemandaMother.random(seed=42)
        demanda_media = 10
        
        # Generar múltiples demandas para verificar consistencia
        demandas = [demanda.value(demanda_media) for _ in range(100)]
        
        # Verificar que todas las demandas son enteros no negativos
        assert all(isinstance(d, int) and d >= 0 for d in demandas)
        
        # Verificar que la media aproximada está cerca del valor esperado
        media_observada = np.mean(demandas)
        assert abs(media_observada - demanda_media) < 2  # Tolerancia razonable
    
    def test_generar_demanda_diferentes_medias(self):
        """Test que verifica que la demanda se genera correctamente para diferentes medias."""
        demanda = DemandaMother.random(seed=42)
        
        # Probar con diferentes medias
        for media in [1, 5, 10, 20]:
            d = demanda.value(media)
            assert isinstance(d, int) and d >= 0
    
    def test_cambiar_semilla(self):
        """Test que verifica que cambiar la semilla produce diferentes resultados."""
        demanda1 = DemandaMother.random(seed=42)
        demanda2 = DemandaMother.random(seed=42)
        demanda3 = DemandaMother.random(seed=123)
        
        demanda_media = 10
        
        # Con la misma semilla, deberían generar la misma secuencia
        secuencia1 = [demanda1.value(demanda_media) for _ in range(10)]
        secuencia2 = [demanda2.value(demanda_media) for _ in range(10)]
        secuencia3 = [demanda3.value(demanda_media) for _ in range(10)]
        assert secuencia1 == secuencia2
        assert secuencia1 != secuencia3
    
    def test_set_seed(self):
        """Test que verifica que set_seed funciona correctamente."""
        demanda = DemandaMother.random(seed=42)
        demanda_media = 10
        
        # Generar una demanda
        secuencia1 = [demanda.value(demanda_media) for _ in range(5)]
        
        # Cambiar semilla
        demanda.set_seed(123)
        secuencia2 = [demanda.value(demanda_media) for _ in range(5)]
        
        # Las demandas deberían ser diferentes
        assert secuencia1 != secuencia2


class TestTiempoEntregaMother:
    """Tests para el Object Mother de tiempos de entrega."""
    
    def test_generar_tiempo_entrega_rango_valido(self):
        """Test que verifica que el tiempo de entrega está en el rango válido."""
        tiempo_entrega = TiempoEntregaMother.random(seed=42)
        plazo_min = 1
        plazo_max = 5
        
        # Generar múltiples tiempos de entrega
        tiempos = [tiempo_entrega.value(plazo_min, plazo_max) for _ in range(100)]
        
        # Verificar que todos están en el rango válido
        assert all(plazo_min <= t <= plazo_max for t in tiempos)
        assert all(isinstance(t, int) for t in tiempos)
    
    def test_generar_tiempo_entrega_diferentes_rangos(self):
        """Test que verifica que funciona con diferentes rangos."""
        tiempo_entrega = TiempoEntregaMother.random(seed=42)
        
        # Probar con diferentes rangos
        rangos = [(1, 3), (2, 7), (0, 10), (5, 5)]
        
        for plazo_min, plazo_max in rangos:
            t = tiempo_entrega.value(plazo_min, plazo_max)
            assert plazo_min <= t <= plazo_max
            assert isinstance(t, int)
    
    def test_generar_tiempo_entrega_mismo_rango(self):
        """Test que verifica que funciona cuando min y max son iguales."""
        tiempo_entrega = TiempoEntregaMother.random(seed=42)
        plazo = 5
        
        t = tiempo_entrega.value(plazo, plazo)
        assert t == plazo
    
    def test_cambiar_semilla(self):
        """Test que verifica que cambiar la semilla produce diferentes resultados."""
        tiempo1 = TiempoEntregaMother.random(seed=42)
        tiempo2 = TiempoEntregaMother.random(seed=42)
        tiempo3 = TiempoEntregaMother.random(seed=123)
        
        plazo_min, plazo_max = 1, 5
        
        # Con la misma semilla, deberían generar la misma secuencia
        secuencia1 = [tiempo1.value(plazo_min, plazo_max) for _ in range(10)]
        secuencia2 = [tiempo2.value(plazo_min, plazo_max) for _ in range(10)]
        secuencia3 = [tiempo3.value(plazo_min, plazo_max) for _ in range(10)]
        assert secuencia1 == secuencia2
        assert secuencia1 != secuencia3
    
    def test_set_seed(self):
        """Test que verifica que set_seed funciona correctamente."""
        tiempo_entrega = TiempoEntregaMother.random(seed=42)
        plazo_min, plazo_max = 1, 5
        
        # Generar un tiempo de entrega
        secuencia1 = [tiempo_entrega.value(plazo_min, plazo_max) for _ in range(5)]
        
        # Cambiar semilla
        tiempo_entrega.set_seed(123)
        secuencia2 = [tiempo_entrega.value(plazo_min, plazo_max) for _ in range(5)]
        
        # Los tiempos deberían ser diferentes
        assert secuencia1 != secuencia2


class TestObjectMothersIntegracion:
    """Tests de integración para verificar que los Object Mothers funcionan juntos."""
    
    def test_ambos_mothers_con_misma_semilla(self):
        """Test que verifica que ambos mothers pueden usar la misma semilla."""
        demanda = DemandaMother.random(seed=42)
        tiempo_entrega = TiempoEntregaMother.random(seed=42)
        
        # Generar valores
        d = demanda.value(10)
        t = tiempo_entrega.value(1, 5)
        
        # Verificar que ambos generan valores válidos
        assert isinstance(d, int) and d >= 0
        assert isinstance(t, int) and 1 <= t <= 5
    
    def test_ambos_mothers_independientes(self):
        """Test que verifica que los mothers son independientes entre sí."""
        demanda = DemandaMother.random(seed=42)
        tiempo_entrega = TiempoEntregaMother.random(seed=42)
        
        # Generar múltiples valores
        demandas = [demanda.value(10) for _ in range(5)]
        tiempos = [tiempo_entrega.value(1, 5) for _ in range(5)]
        
        # Verificar que ambos generan secuencias válidas
        assert len(set(demandas)) > 1  # Al menos algunos valores diferentes
        assert len(set(tiempos)) > 1   # Al menos algunos valores diferentes 