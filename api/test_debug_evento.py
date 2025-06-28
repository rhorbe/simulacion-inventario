#!/usr/bin/env python3

from src.domain.models.evento import Evento, EventoDemanda, EventoLlegadaPedido

def test_crear_eventos():
    """Test de debug para verificar cómo crear instancias de eventos."""
    
    print("Probando diferentes formas de crear EventoDemanda:")
    
    try:
        # Forma 1: Con argumentos posicionales
        evento1 = EventoDemanda(1, 10)
        print("✓ EventoDemanda(1, 10) funciona")
        print(f"  dia: {evento1.dia}, cantidad: {evento1.cantidad}")
    except Exception as e:
        print(f"✗ EventoDemanda(1, 10) falló: {e}")
    
    try:
        # Forma 2: Con argumentos nombrados
        evento2 = EventoDemanda(dia=1, cantidad=10)
        print("✓ EventoDemanda(dia=1, cantidad=10) funciona")
        print(f"  dia: {evento2.dia}, cantidad: {evento2.cantidad}")
    except Exception as e:
        print(f"✗ EventoDemanda(dia=1, cantidad=10) falló: {e}")
    
    try:
        # Forma 3: Solo con dia
        evento3 = EventoDemanda(1)
        print("✓ EventoDemanda(1) funciona")
        print(f"  dia: {evento3.dia}, cantidad: {evento3.cantidad}")
    except Exception as e:
        print(f"✗ EventoDemanda(1) falló: {e}")
    
    print("\nProbando diferentes formas de crear EventoLlegadaPedido:")
    
    try:
        # Forma 1: Con argumentos posicionales
        evento4 = EventoLlegadaPedido(2, 20)
        print("✓ EventoLlegadaPedido(2, 20) funciona")
        print(f"  dia: {evento4.dia}, cantidad: {evento4.cantidad}")
    except Exception as e:
        print(f"✗ EventoLlegadaPedido(2, 20) falló: {e}")
    
    try:
        # Forma 2: Con argumentos nombrados
        evento5 = EventoLlegadaPedido(dia=2, cantidad=20)
        print("✓ EventoLlegadaPedido(dia=2, cantidad=20) funciona")
        print(f"  dia: {evento5.dia}, cantidad: {evento5.cantidad}")
    except Exception as e:
        print(f"✗ EventoLlegadaPedido(dia=2, cantidad=20) falló: {e}")

if __name__ == "__main__":
    test_crear_eventos() 