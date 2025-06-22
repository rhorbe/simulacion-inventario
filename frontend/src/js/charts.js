// Módulo para manejar los gráficos de resultados
class ChartsManager {
    constructor() {
        this.financieroChart = null;
        this.costosChart = null;
    }

    crearGraficoFinanciero(resultados) {
        const ctx = document.getElementById('graficoFinanciero').getContext('2d');
        
        // Destruir gráfico anterior si existe
        if (this.financieroChart) {
            this.financieroChart.destroy();
        }

        const labels = ['Ingresos', 'Costos Totales', 'Ganancia'];
        const datasets = resultados.map((resultado, index) => {
            const colors = [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
                '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
            ];
            
            return {
                label: `Política (r=${resultado.r}, Q=${resultado.Q})`,
                data: [
                    resultado.ingresos,
                    resultado.costo_alm + resultado.costo_faltante + resultado.costo_pedidos,
                    resultado.ganancia
                ],
                backgroundColor: colors[index % colors.length],
                borderColor: colors[index % colors.length],
                borderWidth: 1
            };
        });

        this.financieroChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Comparación Financiera por Política'
                    },
                    legend: {
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    crearGraficoCostos(resultados) {
        const ctx = document.getElementById('graficoCostos').getContext('2d');
        
        // Destruir gráfico anterior si existe
        if (this.costosChart) {
            this.costosChart.destroy();
        }

        const labels = ['Almacenamiento', 'Faltante', 'Pedidos'];
        const datasets = resultados.map((resultado, index) => {
            const colors = [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
                '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
            ];
            
            return {
                label: `Política (r=${resultado.r}, Q=${resultado.Q})`,
                data: [
                    resultado.costo_alm,
                    resultado.costo_faltante,
                    resultado.costo_pedidos
                ],
                backgroundColor: colors[index % colors.length],
                borderColor: colors[index % colors.length],
                borderWidth: 1
            };
        });

        this.costosChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Análisis de Costos por Política'
                    },
                    legend: {
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    actualizarGraficos(resultados) {
        this.crearGraficoFinanciero(resultados);
        this.crearGraficoCostos(resultados);
    }
}

// Instancia global del gestor de gráficos
const chartsManager = new ChartsManager(); 