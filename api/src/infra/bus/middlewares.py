import json
import socket
from datetime import datetime
from typing import Any, Callable
from api.src.domain.bus.middleware import Middleware, MiddlewareContext


class LoggingMiddleware(Middleware):
    def __init__(self, logger_name: str = "simulacion_inventario"):
        self.host = 'logstash'
        self.port = 5000
        self.socket = None
    
    def _send_log(self, log_data: dict):
        """Envía log JSON directamente a Logstash"""
        try:
            if self.socket is None:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
            
            # Crear mensaje JSON con timestamp
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "logger": "simulacion_inventario",
                "message": json.dumps(log_data)
            }
            
            # Enviar JSON + newline
            json_data = json.dumps(log_entry) + '\n'
            self.socket.send(json_data.encode('utf-8'))
            
        except Exception as e:
            print(f"Error enviando log a Logstash: {e}")
            # Marcar socket como inválido para reconectar en el próximo intento
            self.socket = None
    
    def _get_traceback(self):
        """Obtiene el traceback actual"""
        import traceback
        return traceback.format_exc()
    
    async def process(self, context: MiddlewareContext, next_middleware: Callable) -> Any:
        """Middleware principal que loggea antes y después del procesamiento"""
        start_time = datetime.now()
        message = context.command_or_event
        
        # Log pre-procesamiento
        log_data = {
            "type": "message_processing",
            "phase": "pre_handle",
            "message_type": type(message).__name__,
            "message_id": getattr(message, 'id', 'unknown'),
            "timestamp": start_time.isoformat(),
            "message_data": message.to_json() if hasattr(message, 'to_json') else str(message)
        }
        self._send_log(log_data)
        
        try:
            # Procesar el mensaje
            result = await next_middleware(context)
            
            # Log post-procesamiento exitoso
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            log_data = {
                "type": "message_processing",
                "phase": "post_handle_success",
                "message_type": type(message).__name__,
                "message_id": getattr(message, 'id', 'unknown'),
                "timestamp": end_time.isoformat(),
                "processing_time_ms": processing_time * 1000,
                "result_type": type(result).__name__ if result else None
            }
            self._send_log(log_data)
            
            return result
            
        except Exception as e:
            # Log post-procesamiento con error
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            log_data = {
                "type": "message_processing",
                "phase": "post_handle_error",
                "message_type": type(message).__name__,
                "message_id": getattr(message, 'id', 'unknown'),
                "timestamp": end_time.isoformat(),
                "processing_time_ms": processing_time * 1000,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "error_traceback": self._get_traceback()
            }
            self._send_log(log_data)
            
            raise 