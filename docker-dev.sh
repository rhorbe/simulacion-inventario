#!/bin/bash

# Script para desarrollo con Docker - Simulación de Inventario

set -e

echo "🐳 Simulación de Inventario - Docker Development"
echo "================================================"

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  build     - Construir las imágenes Docker"
    echo "  up        - Levantar los servicios"
    echo "  down      - Detener los servicios"
    echo "  restart   - Reiniciar los servicios"
    echo "  logs      - Mostrar logs de los servicios"
    echo "  clean     - Limpiar contenedores e imágenes"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 build && $0 up    # Construir y levantar"
    echo "  $0 logs              # Ver logs en tiempo real"
}

# Función para construir imágenes
build_images() {
    echo "🔨 Construyendo imágenes Docker..."
    docker-compose build --no-cache
    echo "✅ Imágenes construidas exitosamente"
}

# Función para levantar servicios
start_services() {
    echo "🚀 Levantando servicios..."
    docker-compose up -d
    echo "✅ Servicios iniciados"
    echo ""
    echo "📱 URLs de acceso:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    echo ""
    echo "📊 Para ver logs: $0 logs"
}

# Función para detener servicios
stop_services() {
    echo "🛑 Deteniendo servicios..."
    docker-compose down
    echo "✅ Servicios detenidos"
}

# Función para reiniciar servicios
restart_services() {
    echo "🔄 Reiniciando servicios..."
    docker-compose restart
    echo "✅ Servicios reiniciados"
}

# Función para mostrar logs
show_logs() {
    echo "📋 Mostrando logs de los servicios..."
    docker-compose logs -f
}

# Función para limpiar
clean_docker() {
    echo "🧹 Limpiando contenedores e imágenes..."
    docker-compose down -v --rmi all
    docker system prune -f
    echo "✅ Limpieza completada"
}

# Función para verificar estado
check_status() {
    echo "📊 Estado de los servicios:"
    docker-compose ps
    echo ""
    echo "🌐 Verificando conectividad..."

    # Verificar backend
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Backend: Funcionando"
    else
        echo "❌ Backend: No responde"
    fi

    # Verificar frontend
    if curl -s http://localhost:3000 > /dev/null; then
        echo "✅ Frontend: Funcionando"
    else
        echo "❌ Frontend: No responde"
    fi
}

# Procesar argumentos
case "${1:-help}" in
    build)
        build_images
        ;;
    up)
        start_services
        ;;
    down)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_docker
        ;;
    status)
        check_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Comando desconocido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac