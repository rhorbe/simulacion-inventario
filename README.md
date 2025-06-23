# Simulación de Inventario - API y Frontend

Sistema completo de simulación de políticas de inventario basado en el modelo (r, Q) implementado como API REST con FastAPI y frontend web interactivo.

## 📋 Tabla de Contenidos

- [Get Started](#get-started)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Documentation](#api-documentation)
- [Frontend](#frontend)
- [Lógica de Simulación](#lógica-de-simulación)
- [Diagrama de Flujo](#diagrama-de-flujo)

## 🚀 Get Started

### Prerrequisitos

- Python 3.8 o superior
- Node.js 20 o superior (para el frontend)
- pip (gestor de paquetes de Python)
- npm (gestor de paquetes de Node.js)

### Instalación y Ejecución

#### 1. Backend (API)

1. **Instalar dependencias Python:**
   ```bash
   pip install -r api/requirements.txt
   ```

2. **Ejecutar la API:**
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verificar la API:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **API Base**: http://localhost:8000

#### 2. Frontend

1. **Navegar al directorio frontend:**
   ```bash
   cd frontend
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Ejecutar el frontend:**
   ```bash
   npm run dev
   ```

4. **Acceder al frontend:**
   - **URL**: http://localhost:3000
   - Se abrirá automáticamente en el navegador

### Comandos Útiles

#### Backend
```bash
# Ejecutar en modo desarrollo (con auto-reload)
uvicorn api.main:app --reload

# Ejecutar en modo producción
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Ejecutar con logs detallados
uvicorn api.main:app --log-level debug
```

#### Frontend
```bash
# Ejecutar en modo desarrollo
npm run dev

# Ejecutar en modo producción
npm start

# Construir para producción
npm run build
```

### 🔧 Debugging

#### Cursor / VS Code

1. **Crear archivo de configuración de debug:**
   - Crear carpeta `.vscode` en la raíz del proyecto
   - Crear archivo `.vscode/launch.json` con el siguiente contenido:

   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "FastAPI Debug",
               "type": "python",
               "request": "launch",
               "module": "uvicorn",
               "args": [
                   "api.main:app",
                   "--reload",
                   "--host",
                   "0.0.0.0",
                   "--port",
                   "8000"
               ],
               "console": "integratedTerminal",
               "cwd": "${workspaceFolder}",
               "env": {
                   "PYTHONPATH": "${workspaceFolder}"
               }
           },
           {
               "name": "FastAPI Debug (Simple)",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}/api/main.py",
               "console": "integratedTerminal",
               "cwd": "${workspaceFolder}",
               "env": {
                   "PYTHONPATH": "${workspaceFolder}"
               }
           }
       ]
   }
   ```

2. **Configurar breakpoints:**
   - Abrir `api/main.py` o `api/application/inventario.py`
   - Hacer clic en el margen izquierdo para establecer breakpoints
   - Los breakpoints se marcan con puntos rojos

3. **Ejecutar en modo debug:**
   - Presionar `F5` o ir a `Run and Debug` (Ctrl+Shift+D)
   - Seleccionar "FastAPI Debug" de la lista desplegable
   - Hacer clic en el botón de play verde

4. **Usar el debugger:**
   - **F5**: Continuar ejecución
   - **F10**: Step Over (siguiente línea)
   - **F11**: Step Into (entrar en función)
   - **Shift+F11**: Step Out (salir de función)
   - **F9**: Toggle Breakpoint

#### PyCharm

1. **Configurar el proyecto:**
   - Abrir PyCharm y seleccionar "Open"
   - Navegar a la carpeta del proyecto y seleccionarla
   - PyCharm detectará automáticamente el entorno Python

2. **Crear configuración de debug:**
   - Ir a `Run` → `Edit Configurations...`
   - Hacer clic en el botón `+` y seleccionar "Python"
   - Configurar los siguientes parámetros:
     - **Name**: `FastAPI Debug`
     - **Script path**: Dejar vacío
     - **Module name**: `uvicorn`
     - **Parameters**: `api.main:app --reload --host 0.0.0.0 --port 8000`
     - **Working directory**: Seleccionar la carpeta del proyecto
     - **Python interpreter**: Seleccionar el intérprete correcto

3. **Configurar breakpoints:**
   - Abrir cualquier archivo `.py` en las carpetas `api/domain/`, `api/application/` o `api/infra/`
   - Hacer clic en el margen izquierdo para establecer breakpoints
   - Los breakpoints aparecen como círculos rojos

4. **Ejecutar en modo debug:**
   - Seleccionar "FastAPI Debug" en la barra de herramientas
   - Hacer clic en el botón de debug (insecto verde)
   - O usar `Shift+F9`

5. **Herramientas de debug:**
   - **F8**: Step Over
   - **F7**: Step Into
   - **Shift+F8**: Step Out
   - **F9**: Resume Program
   - **Ctrl+F8**: Toggle Breakpoint

#### Configuración Adicional para Debug

**Variables de entorno útiles:**
```bash
# Para logs detallados
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export UVICORN_LOG_LEVEL=debug

# Para desarrollo
export FASTAPI_ENV=development
```

**Archivo `.env` (opcional):**
```env
PYTHONPATH=.
UVICORN_LOG_LEVEL=debug
FASTAPI_ENV=development
```

**Puntos de debug recomendados:**
- `api/main.py`: Línea 30 (función `simular`)
- `api/application/inventario.py`: Línea 95 (inicio de `simular_politica`)
- `api/application/inventario.py`: Línea 120 (procesamiento de eventos)
- `api/infra/repository/yml_config_repository.py`: Línea 25 (carga de configuración)

## 📁 Estructura del Proyecto

```
simulacion-inventario/
├── api/                    # Backend - API y lógica de simulación
│   ├── domain/            # Capa de dominio - entidades y lógica de negocio
│   │   ├── dto/           # Data Transfer Objects
│   │   │   ├── __init__.py
│   │   │   ├── simulacion_request.py  # DTO para requests de simulación
│   │   │   └── politica_abastecimiento.py  # DTO para políticas
│   │   ├── models/        # Modelos de dominio
│   │   │   ├── __init__.py
│   │   │   └── evento.py  # Clase Evento para simulación discreta
│   │   ├── repository/    # Interfaces de repositorio
│   │   │   ├── __init__.py
│   │   │   └── config.py  # Interfaz Config (contrato de configuración)
│   │   └── __init__.py    # Paquete Domain
│   ├── application/       # Capa de aplicación - casos de uso
│   │   ├── __init__.py    # Paquete Application
│   │   └── inventario.py  # Lógica de simulación de inventario (desacoplada)
│   ├── infra/             # Capa de infraestructura - interfaces externas
│   │   ├── controllers/   # Controladores de la API
│   │   │   ├── __init__.py
│   │   │   ├── health_controller.py  # Endpoint de health check
│   │   │   └── simulacion_controller.py  # Endpoint de simulación
│   │   ├── repository/    # Implementaciones de repositorios
│   │   │   ├── __init__.py
│   │   │   ├── yml_config_repository.py  # Implementación YAML de Config
│   │   │   └── config.yml  # Archivo de configuración centralizado
│   │   └── __init__.py    # Paquete Infrastructure
│   ├── dependency_injection.py  # Configuración de inyección de dependencias
│   ├── main.py            # Punto de entrada de la aplicación FastAPI
│   ├── requirements.txt   # Dependencias del proyecto
│   └── Dockerfile         # Configuración Docker para el backend
├── frontend/              # Frontend - Interfaz web interactiva
│   ├── src/               # Código fuente del frontend
│   │   ├── index.html     # Página principal
│   │   ├── css/
│   │   │   └── styles.css # Estilos personalizados
│   │   └── js/
│   │       ├── config.js  # Configuración de la aplicación
│   │       ├── api.js     # Comunicación con la API
│   │       ├── form.js    # Gestión del formulario
│   │       ├── charts.js  # Gráficos y visualizaciones
│   │       └── app.js     # Lógica principal de la aplicación
│   ├── package.json       # Dependencias y scripts del frontend
│   ├── Dockerfile         # Configuración Docker para containerizar el frontend
│   └── nginx.conf         # Configuración de Nginx
├── docker-compose.yml     # Orquestación de servicios Docker
├── .gitignore             # Archivos ignorados por Git
├── README.md              # Documentación del proyecto
└── esquema.md             # Diagrama de flujo de la simulación
```

### Descripción de Archivos

#### Backend (`api/`)

##### Punto de Entrada (`api/`)
- **`main.py`**: Punto de entrada de la aplicación FastAPI. Configura la aplicación, middleware CORS, inyección de dependencias y registra los controladores.
- **`dependency_injection.py`**: Configuración de inyección de dependencias. Define la función `get_config()` que proporciona la implementación concreta de la interfaz Config.

##### Capa de Infraestructura (`api/infra/`)
- **`controllers/`**: Controladores de la API REST
  - **`health_controller.py`**: Endpoint de health check (`/health`)
  - **`simulacion_controller.py`**: Endpoint principal de simulación (`/simular`) con inyección de dependencias
- **`repository/`**: Implementaciones concretas de repositorios
  - **`yml_config_repository.py`**: Implementación concreta de la interfaz Config que carga configuración desde archivos YAML
  - **`config.yml`**: Archivo de configuración centralizado con todos los parámetros de la simulación

##### Capa de Aplicación (`api/application/`)
- **`inventario.py`**: Contiene toda la lógica de simulación del sistema de inventario. Está completamente desacoplado de la configuración y recibe todos los parámetros como argumentos de función.

##### Capa de Dominio (`api/domain/`)
- **`dto/`**: Data Transfer Objects para comunicación entre capas
  - **`simulacion_request.py`**: DTO para recibir requests de simulación
  - **`politica_abastecimiento.py`**: DTO para representar políticas de abastecimiento
- **`models/`**: Modelos de dominio
  - **`evento.py`**: Define la clase `Evento` utilizada para la simulación discreta de eventos
- **`repository/`**: Interfaces de repositorio
  - **`config.py`**: Interfaz abstracta Config que define el contrato para las fuentes de configuración

##### Configuración (`api/`)
- **`requirements.txt`**: Lista de dependencias Python necesarias para ejecutar el proyecto
- **`Dockerfile`**: Configuración Docker para containerizar el backend

#### Frontend (`frontend/`)

##### Código Fuente (`frontend/src/`)
- **`index.html`**: Página principal con formulario de simulación y área de resultados
- **`css/styles.css`**: Estilos personalizados para la interfaz
- **`js/config.js`**: Configuración de la aplicación (URLs, colores, validaciones)
- **`js/api.js`**: Módulo para comunicaciones con la API backend
- **`js/form.js`**: Gestión del formulario y validaciones
- **`js/charts.js`**: Generación de gráficos con Chart.js
- **`js/app.js`**: Lógica principal y coordinación de módulos

##### Configuración (`frontend/`)
- **`package.json`**: Dependencias y scripts de Node.js
- **`Dockerfile`**: Configuración Docker para containerizar el frontend
- **`nginx.conf`**: Configuración de Nginx para servir el frontend

#### Orquestación
- **`docker-compose.yml`**: Orquestación de servicios Docker (backend + frontend + nginx)

#### Documentación
- **`esquema.md`**: Diagrama de flujo que explica el funcionamiento de la simulación.

## 🔌 API Documentation

### Endpoints Disponibles

#### GET `/health`
Endpoint de health check para verificar que la API está funcionando.

**Response:**
```json
{
  "status": "ok",
  "message": "API de Simulación de Inventario funcionando correctamente"
}
```

#### POST `/simular`
Endpoint principal que ejecuta la simulación de políticas de inventario.

### Modelo SimulacionRequest

```python
class SimulacionRequest(BaseModel):
    inventario_inicial: Optional[int] = None
    plazo_entrega_min: Optional[int] = None
    plazo_entrega_max: Optional[int] = None
    dias_simulacion: Optional[int] = None
    anios_simulacion: Optional[int] = None
    costo_almacenar: Optional[float] = None
    costo_faltante: Optional[float] = None
    costo_pedido_pequenio: Optional[float] = None
    costo_pedido_grande: Optional[float] = None
    precio_venta: Optional[float] = None
    politicas_abastecimiento: Optional[List[PoliticaAbastecimiento]] = None
    demanda: Optional[int] = None
```

#### Parámetros del Modelo

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `inventario_inicial` | int | Config | Inventario inicial en unidades |
| `plazo_entrega_min` | int | Config | Plazo mínimo de entrega en días |
| `plazo_entrega_max` | int | Config | Plazo máximo de entrega en días |
| `dias_simulacion` | int | Config | Días por año de simulación |
| `anios_simulacion` | int | Config | Número de años a simular |
| `costo_almacenar` | float | Config | Costo por unidad por día de almacenamiento |
| `costo_faltante` | float | Config | Costo por unidad de faltante |
| `costo_pedido_pequenio` | float | Config | Costo por unidad para pedidos < 300 |
| `costo_pedido_grande` | float | Config | Costo por unidad para pedidos ≥ 300 |
| `precio_venta` | float | Config | Precio de venta por unidad |
| `politicas_abastecimiento` | List | Config | Lista de políticas (r, Q) a simular |
| `demanda` | int | Config | Demanda media diaria (distribución Poisson) |

#### Modelo PoliticaAbastecimiento

```python
class PoliticaAbastecimiento(BaseModel):
    punto_reorden: Optional[int] = None  # Nivel de reposición (r)
    cantidad_pedido: int                 # Tamaño del lote (Q)
```

### Ejemplo de Request

```json
{
  "inventario_inicial": 720,
  "dias_simulacion": 365,
  "anios_simulacion": 5,
  "politicas_abastecimiento": [
    {"punto_reorden": 40, "cantidad_pedido": 140},
    {"punto_reorden": 30, "cantidad_pedido": 140},
    {"punto_reorden": 60, "cantidad_pedido": 140}
  ],
  "demanda": 200
}
```

### Ejemplo de Response

```json
{
  "resultados": [
    {
      "r": 40,
      "Q": 140,
      "ingresos": 91250000.0,
      "costo_alm": 5400000.0,
      "costo_faltante": 190000.0,
      "costo_pedidos": 4200000.0,
      "ganancia": 81550000.0
    },
    {
      "r": 30,
      "Q": 140,
      "ingresos": 91250000.0,
      "costo_alm": 5400000.0,
      "costo_faltante": 285000.0,
      "costo_pedidos": 4200000.0,
      "ganancia": 81365000.0
    }
  ]
}
```

## 🖥️ Frontend

### Características

- **Formulario Intuitivo**: Interfaz fácil de usar con tooltips explicativos
- **Gestión Dinámica de Políticas**: Agregar/eliminar políticas de abastecimiento
- **Validación de Datos**: Validación en tiempo real de todos los parámetros
- **Visualización de Resultados**: Tabla comparativa y gráficos interactivos
- **Responsive Design**: Compatible con dispositivos móviles y desktop

### Tecnologías Utilizadas

- **HTML5**: Estructura semántica
- **CSS3**: Estilos y animaciones
- **JavaScript ES6+**: Lógica de la aplicación
- **Bootstrap 5**: Framework CSS responsive
- **Chart.js**: Gráficos interactivos
- **Bootstrap Icons**: Iconografía

### Uso del Frontend

#### 1. Configurar Parámetros
- **Inventario**: Establecer inventario inicial y demanda media
- **Tiempo**: Definir días por año y años de simulación
- **Entrega**: Configurar plazos mínimo y máximo de entrega
- **Costos**: Establecer todos los costos del sistema
- **Precios**: Definir precio de venta por unidad

#### 2. Agregar Políticas
- Hacer clic en "Agregar Política" para crear nuevas políticas
- Configurar punto de reorden (r) y cantidad de pedido (Q)
- Eliminar políticas innecesarias con el botón X

#### 3. Ejecutar Simulación
- Hacer clic en "Ejecutar Simulación"
- Esperar a que se procesen los resultados
- Revisar la tabla comparativa y los gráficos

#### 4. Analizar Resultados
- **Tabla**: Comparar métricas entre políticas
- **Gráfico Financiero**: Visualizar ingresos, costos y ganancias
- **Gráfico de Costos**: Analizar desglose de costos por tipo

### Configuración de la API

La aplicación está configurada para conectarse a la API en `http://localhost:8000`. Para cambiar la URL de la API, modificar la constante `API_BASE_URL` en `frontend/src/js/config.js`.

## 🧮 Lógica de Simulación

### Arquitectura de la Simulación

La simulación utiliza el **método de eventos discretos** para modelar el sistema de inventario. Los eventos principales son:
- **Eventos de Demanda**: Generación de demanda diaria con distribución Poisson
- **Eventos de Llegada de Pedidos**: Recepción de pedidos según plazos de entrega

### Flujo de Ejecución

1. **Punto de Entrada**: La API recibe una petición POST en `/simular` con los parámetros de simulación
2. **Procesamiento**: El controlador en `simulacion_controller.py` itera sobre las políticas y llama a `simular_politica` para cada una
3. **Simulación**: Cada política se simula de forma independiente y desacoplada
4. **Resultados**: Se retornan los resultados de todas las políticas simuladas

### Método Principal: `simular_politica(r, Q, dias_simulacion, **kwargs)`

#### Parámetros de Entrada
- `r` (int): Punto de reorden (nivel de inventario que dispara un nuevo pedido)
- `Q` (int): Cantidad a pedir (tamaño del lote de reposición)
- `dias_simulacion` (int): Período total de simulación en días
- `**kwargs`: Parámetros adicionales de configuración (todos los valores de costos, tiempos, etc.)

#### Flujo de Ejecución

1. **Inicialización:**
   ```python
   # Recibir parámetros desde kwargs (sin dependencia de configuración)
   inventario = kwargs.get("inventario_inicial")
   precio_venta = kwargs.get("precio_venta")
   costo_almacenar = kwargs.get("costo_almacenar")
   # ... otros parámetros
   
   # Crear primer evento de demanda
   lista_eventos = [Evento("demanda", 0, generar_demanda(demanda_media))]
   ```

2. **Bucle Principal de Eventos:**
   ```python
   while lista_eventos:
       evento_actual = lista_eventos.pop(0)  # Procesar próximo evento
       
       if dia >= dias_simulacion: 
           break  # Finalizar simulación
   ```

3. **Procesamiento de Eventos:**
   - **Evento "demanda"**: Calcular ventas y faltantes, actualizar inventario
   - **Evento "llegada_pedido"**: Recibir pedido y actualizar inventario

4. **Lógica de Reposición:**
   ```python
   if inventario < r:  # Si inventario cae bajo punto de reorden
       nuevoPedido = Evento("llegada_pedido", dia + generar_tiempo_entrega(), Q)
       costo_pedidos += Q * costo_unitario_pedido(Q, costo_pedido_pequeno, costo_pedido_grande)
   ```

5. **Cálculo de Costos Diarios:**
   ```python
   costo_almacenamiento += inventario * costo_almacenar  # Costo de almacenamiento diario
   ```

6. **Generación de Nuevos Eventos:**
   ```python
   if not existen_eventos_pendientes(lista_eventos, dia + 1):
       nueva_demanda = Evento("demanda", dia + 1, generar_demanda(demanda_media))
       lista_eventos.append(nueva_demanda)
   ```

#### Funciones de Soporte

- **`generar_demanda(demanda_media)`**: Genera demanda aleatoria con distribución Poisson
- **`generar_tiempo_entrega(plazo_min, plazo_max)`**: Genera plazo de entrega uniforme
- **`costo_unitario_pedido(q, costo_pequeno, costo_grande)`**: Calcula costo según tamaño del pedido
- **`calcular_resultados_diarios(demanda, inventario)`**: Calcula ventas y faltantes
- **`existen_eventos_pendientes(lista_eventos, dia)`**: Verifica eventos futuros

#### Cálculo de Resultados

```python
# Costos totales
costo_total = costo_almacenamiento + costo_total_faltante + costo_pedidos

# Ganancia neta
ganancia = ingresos - costo_total

return {
    "r": r,
    "Q": Q,
    "ingresos": ingresos,
    "costo_alm": costo_almacenamiento,
    "costo_faltante": costo_total_faltante,
    "costo_pedidos": costo_pedidos,
    "ganancia": ganancia,
}
```

### Características de la Simulación

- **Simulación Discreta**: Basada en eventos, no en intervalos de tiempo fijos
- **Política (r, Q)**: Sistema de revisión continua con punto de reorden
- **Demanda Estocástica**: Distribución Poisson para modelar variabilidad
- **Plazos de Entrega Variables**: Distribución uniforme entre mínimo y máximo
- **Costos Dinámicos**: Diferentes costos según tamaño de pedido
- **Múltiples Políticas**: Comparación simultánea de diferentes estrategias
- **Desacoplamiento**: El módulo de simulación no depende de configuración externa

## 📊 Diagrama de Flujo

Para una explicación visual detallada del funcionamiento de la simulación, consulta el [esquema de la simulación](esquema.md).

---

**Desarrollado para el curso de Modelos y Simulación - Trabajo Final**
