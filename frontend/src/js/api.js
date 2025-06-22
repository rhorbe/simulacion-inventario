// Módulo para manejar las comunicaciones con la API
class ApiService {
    constructor() {
        this.baseUrl = CONFIG.API_BASE_URL;
    }

    async simular(datos) {
        try {
            console.log('Enviando datos a la API:', datos);
            
            const response = await fetch(`${this.baseUrl}${CONFIG.API_ENDPOINTS.SIMULAR}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(datos)
            });

            console.log('Respuesta de la API:', response.status, response.statusText);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`Error HTTP: ${response.status} - ${errorText}`);
            }

            const result = await response.json();
            console.log('Resultado de la simulación:', result);
            return result;
        } catch (error) {
            console.error('Error en la simulación:', error);
            throw new Error(`Error al ejecutar la simulación: ${error.message}`);
        }
    }

    // Método para validar que la API esté disponible
    async healthCheck() {
        try {
            console.log('Verificando conectividad con la API...');
            const response = await fetch(`${this.baseUrl}/`);
            const isOk = response.ok;
            console.log('Health check result:', isOk ? 'OK' : 'FAILED');
            return isOk;
        } catch (error) {
            console.error('Error en health check:', error);
            return false;
        }
    }
}

// Instancia global del servicio API
const apiService = new ApiService(); 