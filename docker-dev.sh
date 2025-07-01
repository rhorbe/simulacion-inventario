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
    echo "  logs-elk  - Mostrar logs solo del stack ELK"
    echo "  clean     - Limpiar contenedores e imágenes"
    echo "  status    - Verificar estado de todos los servicios"
    echo "  elastic   - Verificar estado de Elasticsearch"
    echo "  kibana    - Abrir Kibana en el navegador"
    echo "  indices   - Listar índices de Elasticsearch"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 build && $0 up    # Construir y levantar"
    echo "  $0 logs              # Ver logs en tiempo real"
    echo "  $0 logs-elk          # Ver logs del stack ELK"
    echo "  $0 kibana            # Abrir Kibana"
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
    echo "  Kibana: http://localhost:5601"
    echo "  Elasticsearch: http://localhost:9200"
    echo "  Logstash API: http://localhost:9600"
    echo ""
    echo "📊 Para ver logs: $0 logs"
    echo "🔍 Para ver logs del ELK: $0 logs-elk"
    echo "📈 Para abrir Kibana: $0 kibana"
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

# Función para mostrar logs del stack ELK
show_elk_logs() {
    echo "📋 Mostrando logs del stack ELK..."
    docker-compose logs -f elasticsearch kibana logstash
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

    # Verificar Elasticsearch
    if curl -s http://localhost:9200/_cluster/health > /dev/null; then
        echo "✅ Elasticsearch: Funcionando"
    else
        echo "❌ Elasticsearch: No responde"
    fi

    # Verificar Kibana
    if curl -s http://localhost:5601/api/status > /dev/null; then
        echo "✅ Kibana: Funcionando"
    else
        echo "❌ Kibana: No responde"
    fi

    # Verificar Logstash
    if curl -s http://localhost:9600/_node/stats > /dev/null; then
        echo "✅ Logstash: Funcionando"
    else
        echo "❌ Logstash: No responde"
    fi
}

# Función para verificar estado de Elasticsearch
check_elasticsearch() {
    echo "🔍 Verificando estado de Elasticsearch..."
    
    if curl -s http://localhost:9200/_cluster/health > /dev/null; then
        echo "✅ Elasticsearch está funcionando"
        echo ""
        echo "📊 Información del cluster:"
        curl -s http://localhost:9200/_cluster/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:9200/_cluster/health
        echo ""
        echo "📈 Estadísticas del nodo:"
        curl -s http://localhost:9200/_nodes/stats | python3 -m json.tool 2>/dev/null || curl -s http://localhost:9200/_nodes/stats
    else
        echo "❌ Elasticsearch no responde"
        echo "💡 Verifica que el servicio esté iniciado: $0 up"
    fi
}

# Función para abrir Kibana
open_kibana() {
    echo "🌐 Abriendo Kibana..."
    
    # Detectar el sistema operativo
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open http://localhost:5601
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v xdg-open > /dev/null; then
            xdg-open http://localhost:5601
        else
            echo "🌐 Abre manualmente: http://localhost:5601"
        fi
    else
        # Windows u otros
        echo "🌐 Abre manualmente: http://localhost:5601"
    fi
    
    echo "✅ Kibana abierto en el navegador"
}

# Función para listar índices de Elasticsearch
list_indices() {
    echo "📚 Listando índices de Elasticsearch..."
    
    if curl -s http://localhost:9200/_cat/indices > /dev/null; then
        echo "📋 Índices disponibles:"
        curl -s http://localhost:9200/_cat/indices?v
        echo ""
        echo "📊 Información detallada de índices:"
        curl -s http://localhost:9200/_cat/indices?format=json | python3 -m json.tool 2>/dev/null || curl -s http://localhost:9200/_cat/indices?format=json
    else
        echo "❌ No se puede conectar a Elasticsearch"
        echo "💡 Verifica que el servicio esté iniciado: $0 up"
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
    logs-elk)
        show_elk_logs
        ;;
    clean)
        clean_docker
        ;;
    status)
        check_status
        ;;
    elastic)
        check_elasticsearch
        ;;
    kibana)
        open_kibana
        ;;
    indices)
        list_indices
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