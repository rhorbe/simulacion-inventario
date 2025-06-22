// Módulo principal de la aplicación
class AppManager {
    constructor() {
        this.initializeApp();
    }

    initializeApp() {
        console.log('Inicializando aplicación de simulación de inventario...');
        
        // Verificar conectividad con la API
        this.verificarAPI();
        
        // Inicializar tooltips
        this.initializeTooltips();
    }

    async verificarAPI() {
        try {
            const isAvailable = await apiService.healthCheck();
            if (!isAvailable) {
                console.warn('La API no está disponible. Asegúrese de que esté ejecutándose en http://localhost:8000');
            }
        } catch (error) {
            console.error('Error al verificar la API:', error);
        }
    }

    initializeTooltips() {
        // Inicializar tooltips de Bootstrap
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    mostrarResultados(resultados) {
        if (!resultados || resultados.length === 0) {
            alert('No se recibieron resultados de la simulación');
            return;
        }

        // Ordenar resultados por ganancia (mejor primero)
        resultados.sort((a, b) => b.ganancia - a.ganancia);

        // Mostrar tabla de resultados
        this.crearTablaResultados(resultados);

        // Actualizar gráficos
        chartsManager.actualizarGraficos(resultados);

        // Mostrar contenedor de resultados
        document.getElementById('resultadosContainer').style.display = 'block';
        document.getElementById('resultadosContainer').classList.add('fade-in');
    }

    crearTablaResultados(resultados) {
        const tablaContainer = document.getElementById('tablaResultados');
        const mejorGanancia = resultados[0].ganancia;

        let tablaHtml = `
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-light">
                        <tr>
                            <th>Política (r, Q)</th>
                            <th>Ingresos</th>
                            <th>Costo Almacenamiento</th>
                            <th>Costo Faltante</th>
                            <th>Costo Pedidos</th>
                            <th>Ganancia</th>
                            <th>Ranking</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        resultados.forEach((resultado, index) => {
            const esMejor = resultado.ganancia === mejorGanancia;
            const rowClass = esMejor ? 'resultado-row mejor-ganancia' : 'resultado-row';
            
            tablaHtml += `
                <tr class="${rowClass}">
                    <td><strong>(${resultado.r}, ${resultado.Q})</strong></td>
                    <td>$${resultado.ingresos.toLocaleString()}</td>
                    <td>$${resultado.costo_alm.toLocaleString()}</td>
                    <td>$${resultado.costo_faltante.toLocaleString()}</td>
                    <td>$${resultado.costo_pedidos.toLocaleString()}</td>
                    <td><strong>$${resultado.ganancia.toLocaleString()}</strong></td>
                    <td>
                        ${esMejor ? 
                            '<span class="badge bg-success"><i class="bi bi-trophy"></i> Mejor</span>' : 
                            `<span class="badge bg-secondary">#${index + 1}</span>`
                        }
                    </td>
                </tr>
            `;
        });

        tablaHtml += `
                    </tbody>
                </table>
            </div>
        `;

        tablaContainer.innerHTML = tablaHtml;
    }

    formatearMoneda(valor) {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS'
        }).format(valor);
    }
}

// Instancia global del gestor de la aplicación
const appManager = new AppManager(); 