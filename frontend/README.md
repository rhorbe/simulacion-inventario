# Frontend - Simulación de Inventario

Interfaz web para el sistema de simulación de políticas de inventario basado en el modelo (r, Q).

## 🚀 Características

- **Formulario Intuitivo**: Interfaz fácil de usar con tooltips explicativos
- **Gestión Dinámica de Políticas**: Agregar/eliminar políticas de abastecimiento
- **Validación de Datos**: Validación en tiempo real de todos los parámetros
- **Visualización de Resultados**: Tabla comparativa y gráficos interactivos
- **Responsive Design**: Compatible con dispositivos móviles y desktop

## 📋 Requisitos

- Node.js (versión 14 o superior)
- Navegador web moderno
- API backend ejecutándose en `http://localhost:8000`

## 🛠️ Instalación

1. **Instalar dependencias:**
   ```bash
   npm install
   ```

2. **Ejecutar en modo desarrollo:**
   ```bash
   npm run dev
   ```

3. **Abrir en el navegador:**
   - La aplicación se abrirá automáticamente en `http://localhost:3000`
   - O navegar manualmente a la URL

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── index.html          # Página principal
│   ├── css/
│   │   └── styles.css      # Estilos personalizados
│   └── js/
│       ├── config.js       # Configuración de la aplicación
│       ├── api.js          # Comunicación con la API
│       ├── form.js         # Gestión del formulario
│       ├── charts.js       # Gráficos y visualizaciones
│       └── app.js          # Lógica principal de la aplicación
├── package.json            # Dependencias y scripts
└── README.md              # Este archivo
```

## 🎯 Uso

### 1. Configurar Parámetros
- **Inventario**: Establecer inventario inicial y demanda media
- **Tiempo**: Definir días por año y años de simulación
- **Entrega**: Configurar plazos mínimo y máximo de entrega
- **Costos**: Establecer todos los costos del sistema
- **Precios**: Definir precio de venta por unidad

### 2. Agregar Políticas
- Hacer clic en "Agregar Política" para crear nuevas políticas
- Configurar punto de reorden (r) y cantidad de pedido (Q)
- Eliminar políticas innecesarias con el botón X

### 3. Ejecutar Simulación
- Hacer clic en "Ejecutar Simulación"
- Esperar a que se procesen los resultados
- Revisar la tabla comparativa y los gráficos

### 4. Analizar Resultados
- **Tabla**: Comparar métricas entre políticas
- **Gráfico Financiero**: Visualizar ingresos, costos y ganancias
- **Gráfico de Costos**: Analizar desglose de costos por tipo

## 🎨 Tecnologías Utilizadas

- **HTML5**: Estructura semántica
- **CSS3**: Estilos y animaciones
- **JavaScript ES6+**: Lógica de la aplicación
- **Bootstrap 5**: Framework CSS responsive
- **Chart.js**: Gráficos interactivos
- **Bootstrap Icons**: Iconografía

## 🔧 Scripts Disponibles

- `npm start`: Ejecutar servidor de desarrollo
- `npm run dev`: Ejecutar con auto-apertura del navegador
- `npm run build`: Construir para producción

## 🌐 Configuración de la API

La aplicación está configurada para conectarse a la API en `http://localhost:8000`. Para cambiar la URL de la API, modificar la constante `API_BASE_URL` en `src/js/config.js`.

## 📱 Compatibilidad

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🐛 Solución de Problemas

### La API no responde
- Verificar que el backend esté ejecutándose en el puerto 8000
- Revisar la consola del navegador para errores de CORS
- Asegurar que la URL de la API sea correcta

### Los gráficos no se muestran
- Verificar que Chart.js esté cargado correctamente
- Revisar que los datos de la API tengan el formato esperado
- Limpiar la caché del navegador

### Problemas de validación
- Revisar que todos los campos numéricos tengan valores válidos
- Asegurar que los plazos de entrega sean coherentes
- Verificar que haya al menos una política configurada 