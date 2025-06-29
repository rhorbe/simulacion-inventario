from api.src.domain.models.evento import EventoDemanda, EventoLlegadaPedido, Evento
from api.src.domain.models.resultados_politica import ResultadosPolitica
from api.src.domain.models.fel import FEL
from api.src.domain.bus.event_bus import EventBus
from api.src.domain.models.simulation_context import SimulationContext
from api.src.domain.value_objects import PoliticaInventario, ConfiguracionSimulacion
from api.src.domain.object_mothers import DemandaMother, TiempoEntregaMother


class SimulacionInventario:
    """Clase que encapsula la lógica de simulación de inventario"""
    
    def __init__(self, politica: PoliticaInventario, configuracion: ConfiguracionSimulacion, event_bus: EventBus):
        self.politica = politica
        self.configuracion = configuracion
        self.event_bus = event_bus
        self.fel = self._inicializar_fel()
        self.context = self._crear_contexto()
    
    def _inicializar_fel(self) -> FEL:
        """Inicializa la FEL con el evento de demanda inicial"""
        return FEL([
            (EventoDemanda(
                0,
                DemandaMother.random(seed=42).value(self.configuracion.get_demanda_media())
            ))
        ])
    
    def _crear_contexto(self) -> SimulationContext:
        """Crea el contexto de simulación"""
        resultados = ResultadosPolitica.from_politica_and_config(self.politica, self.configuracion)
        return SimulationContext(resultados=resultados, configuracion=self.configuracion)
    
    def ejecutar(self) -> dict:
        """Ejecuta la simulación completa"""
        while self.fel.hay_eventos():
            evento = self.fel.siguiente()
            
            if evento.get_dia() >= self.configuracion.get_dias_simulacion():
                break

            self._procesar_evento(evento)
            self._verificar_punto_reorden(evento)
            self._agregar_costo_almacenamiento()
            self._programar_siguiente_demanda(evento)
        
        return self.context.resultados.to_dict()
    
    def _procesar_evento(self, evento: Evento) -> None:
        """Procesa un evento usando el event bus"""
        self.event_bus.dispatch(evento, self.context)
    
    def _verificar_punto_reorden(self, evento: Evento) -> None:
        """Verifica si se debe hacer un pedido"""
        if self._es_punto_de_reorden():
            self._realizar_pedido(evento)
    
    def _es_punto_de_reorden(self) -> bool:
        """Determina si se alcanzó el punto de reorden"""
        return self.context.resultados.obtener_inventario() < self.politica.get_punto_reorden()
    
    def _realizar_pedido(self, evento: Evento) -> None:
        """Realiza un pedido cuando se alcanza el punto de reorden"""
        cantidad = self.politica.get_cantidad_pedido()
        costo_unitario = self.configuracion.calcular_costo_unitario_pedido(cantidad)
        
        self.context.resultados.agregar_costo_pedido(cantidad * costo_unitario)
        
        entrega = self._calcular_dia_entrega(evento)
        self.fel.agregar_evento(EventoLlegadaPedido(entrega, cantidad))
    
    def _calcular_dia_entrega(self, evento: Evento) -> int:
        """Calcula el día de entrega del pedido"""
        return evento.get_dia() + TiempoEntregaMother.random(seed=42).value(
            self.configuracion.get_plazo_entrega_min(),
            self.configuracion.get_plazo_entrega_max()
        )
    
    def _agregar_costo_almacenamiento(self) -> None:
        """Agrega el costo de almacenamiento diario"""
        inventario_actual = self.context.resultados.obtener_inventario()
        costo_almacenamiento = inventario_actual * self.configuracion.get_costo_almacenar()
        self.context.resultados.agregar_costo_almacenamiento(costo_almacenamiento)
    
    def _programar_siguiente_demanda(self, evento: Evento) -> None:
        """Programa la siguiente demanda si no hay eventos futuros"""
        if not self.fel.hay_eventos_futuros_en_dia(evento.get_dia() + 1):
            self.fel.agregar_evento(EventoDemanda(
                evento.get_dia() + 1,
                DemandaMother.random(seed=42).value(self.configuracion.get_demanda_media())
            )) 