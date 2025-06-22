// Módulo para manejar el formulario y la gestión de políticas
class FormManager {
    constructor() {
        this.politicaCounter = 0;
        this.initializeForm();
        this.initializeTooltips();
    }

    initializeForm() {
        this.form = document.getElementById('simulacionForm');
        this.politicasContainer = document.getElementById('politicasContainer');
        this.agregarPoliticaBtn = document.getElementById('agregarPolitica');

        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        this.agregarPoliticaBtn.addEventListener('click', this.agregarPolitica.bind(this));

        // Agregar política inicial
        this.agregarPolitica();
    }

    initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    agregarPolitica() {
        this.politicaCounter++;
        const politicaId = `politica-${this.politicaCounter}`;
        
        const politicaHtml = `
            <div class="politica-item" id="${politicaId}">
                <i class="bi bi-x-circle remove-politica" onclick="formManager.removerPolitica('${politicaId}')"></i>
                <h6 class="text-secondary mb-3">Política ${this.politicaCounter}</h6>
                <div class="row">
                    <div class="col-6">
                        <label class="form-label">
                            Punto de Reorden (r)
                            <i class="bi bi-question-circle" data-bs-toggle="tooltip" title="Nivel de inventario que dispara un nuevo pedido"></i>
                        </label>
                        <input type="number" class="form-control politica-punto-reorden" value="40" min="0">
                    </div>
                    <div class="col-6">
                        <label class="form-label">
                            Cantidad Pedido (Q)
                            <i class="bi bi-question-circle" data-bs-toggle="tooltip" title="Tamaño del lote de reposición"></i>
                        </label>
                        <input type="number" class="form-control politica-cantidad-pedido" value="140" min="1">
                    </div>
                </div>
            </div>
        `;

        this.politicasContainer.insertAdjacentHTML('beforeend', politicaHtml);
        
        // Reinicializar tooltips para los nuevos elementos
        const newTooltips = document.querySelectorAll(`#${politicaId} [data-bs-toggle="tooltip"]`);
        newTooltips.forEach(el => new bootstrap.Tooltip(el));
    }

    removerPolitica(politicaId) {
        const politicaElement = document.getElementById(politicaId);
        if (politicaElement) {
            politicaElement.remove();
        }
    }

    obtenerDatosFormulario() {
        const politicas = [];
        const politicaItems = document.querySelectorAll('.politica-item');
        
        politicaItems.forEach(item => {
            const puntoReorden = item.querySelector('.politica-punto-reorden').value;
            const cantidadPedido = item.querySelector('.politica-cantidad-pedido').value;
            
            politicas.push({
                punto_reorden: puntoReorden ? parseInt(puntoReorden) : null,
                cantidad_pedido: parseInt(cantidadPedido)
            });
        });

        return {
            inventario_inicial: parseInt(document.getElementById('inventarioInicial').value),
            demanda: parseInt(document.getElementById('demanda').value),
            dias_simulacion: parseInt(document.getElementById('diasSimulacion').value),
            anios_simulacion: parseInt(document.getElementById('aniosSimulacion').value),
            plazo_entrega_min: parseInt(document.getElementById('plazoEntregaMin').value),
            plazo_entrega_max: parseInt(document.getElementById('plazoEntregaMax').value),
            costo_almacenar: parseFloat(document.getElementById('costoAlmacenar').value),
            costo_faltante: parseFloat(document.getElementById('costoFaltante').value),
            costo_pedido_pequenio: parseFloat(document.getElementById('costoPedidoPequenio').value),
            costo_pedido_grande: parseFloat(document.getElementById('costoPedidoGrande').value),
            precio_venta: parseFloat(document.getElementById('precioVenta').value),
            politicas_abastecimiento: politicas
        };
    }

    validarFormulario(datos) {
        const errores = [];

        if (datos.inventario_inicial < CONFIG.VALIDATION.min_inventario) {
            errores.push('El inventario inicial debe ser mayor o igual a 0');
        }

        if (datos.demanda < CONFIG.VALIDATION.min_demanda) {
            errores.push('La demanda debe ser mayor a 0');
        }

        if (datos.dias_simulacion < CONFIG.VALIDATION.min_dias) {
            errores.push('Los días de simulación deben ser mayor a 0');
        }

        if (datos.anios_simulacion < CONFIG.VALIDATION.min_anios) {
            errores.push('Los años de simulación deben ser mayor a 0');
        }

        if (datos.plazo_entrega_min < CONFIG.VALIDATION.min_plazo) {
            errores.push('El plazo mínimo de entrega debe ser mayor a 0');
        }

        if (datos.plazo_entrega_max < datos.plazo_entrega_min) {
            errores.push('El plazo máximo debe ser mayor o igual al plazo mínimo');
        }

        if (datos.costo_almacenar < CONFIG.VALIDATION.min_costos) {
            errores.push('El costo de almacenamiento debe ser mayor o igual a 0');
        }

        if (datos.costo_faltante < CONFIG.VALIDATION.min_costos) {
            errores.push('El costo de faltante debe ser mayor o igual a 0');
        }

        if (datos.costo_pedido_pequenio < CONFIG.VALIDATION.min_costos) {
            errores.push('El costo de pedido pequeño debe ser mayor o igual a 0');
        }

        if (datos.costo_pedido_grande < CONFIG.VALIDATION.min_costos) {
            errores.push('El costo de pedido grande debe ser mayor o igual a 0');
        }

        if (datos.precio_venta < CONFIG.VALIDATION.min_precio) {
            errores.push('El precio de venta debe ser mayor o igual a 0');
        }

        if (datos.politicas_abastecimiento.length === 0) {
            errores.push('Debe agregar al menos una política de abastecimiento');
        }

        datos.politicas_abastecimiento.forEach((politica, index) => {
            if (politica.cantidad_pedido < 1) {
                errores.push(`La cantidad de pedido de la política ${index + 1} debe ser mayor a 0`);
            }
        });

        return errores;
    }

    async handleSubmit(event) {
        event.preventDefault();
        
        const datos = this.obtenerDatosFormulario();
        const errores = this.validarFormulario(datos);

        if (errores.length > 0) {
            alert('Errores de validación:\n' + errores.join('\n'));
            return;
        }

        // Mostrar loading
        document.getElementById('resultadosContainer').style.display = 'none';
        document.getElementById('loadingContainer').style.display = 'block';

        try {
            const resultado = await apiService.simular(datos);
            appManager.mostrarResultados(resultado.resultados);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            document.getElementById('loadingContainer').style.display = 'none';
        }
    }
}

// Instancia global del gestor de formularios
const formManager = new FormManager(); 