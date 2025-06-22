# Simulación de Inventario - API

Sistema de simulación de políticas de inventario basado en el modelo (r, Q) implementado como API REST con FastAPI. Permite simular diferentes políticas de abastecimiento y comparar sus resultados financieros.

## 📋 Tabla de Contenidos

- [Get Started](#get-started)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Documentation](#api-documentation)
- [Lógica de Simulación](#lógica-de-simulación)
- [Diagrama de Flujo](#diagrama-de-flujo)

## 🚀 Get Started

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd simulacion-inventario
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la API:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Acceder a la documentación:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **API Base**: http://localhost:8000

### Comandos Útiles

```bash
# Ejecutar en modo desarrollo (con auto-reload)
uvicorn main:app --reload

# Ejecutar en modo producción
uvicorn main:app --host 0.0.0.0 --port 8000

# Ejecutar con logs detallados
uvicorn main:app --log-level debug
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
                   "main:app",
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
               "program": "${workspaceFolder}/main.py",
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
   - Abrir `main.py` o `inventario.py`
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
     - **Parameters**: `main:app --reload --host 0.0.0.0 --port 8000`
     - **Working directory**: Seleccionar la carpeta del proyecto
     - **Python interpreter**: Seleccionar el intérprete correcto

3. **Configurar breakpoints:**
   - Abrir cualquier archivo `.py`
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
- `main.py`: Línea 45 (función `simular`)
- `inventario.py`: Línea 95 (inicio de `simular_politica`)
- `inventario.py`: Línea 120 (procesamiento de eventos)
- `config.py`: Línea 25 (carga de configuración)

## 📁 Estructura del Proyecto

```
simulacion-inventario/
├── main.py                 # API FastAPI y endpoints
├── inventario.py           # Lógica de simulación de 
├── config.py               # Clase Singleton para 
├── evento.py               # Clase Evento para 
├── config.yml              # Archivo de configuración 
├── requirements.txt        # Dependencias del proyecto
├── .gitignore              # Archivos ignorados por Git
├── README.md               # Documentación del proyecto
└── esquema.md              # Diagrama de flujo de la 
```

### Descripción de Archivos

- **`main.py`**: API REST con FastAPI. Define endpoints, modelos de datos y maneja las peticiones HTTP.
- **`inventario.py`**: Contiene toda la lógica de simulación del sistema de inventario, incluyendo generación de eventos y cálculos financieros.
- **`config.py`**: Implementa el patrón Singleton para cargar y gestionar la configuración desde `config.yml`.
- **`evento.py`**: Define la clase `Evento` utilizada para la simulación discreta de eventos (demandas y llegadas de pedidos).
- **`config.yml`**: Archivo de configuración centralizado con todos los parámetros de la simulación (costos, tiempos, políticas, etc.).
- **`requirements.txt`**: Lista de dependencias Python necesarias para ejecutar el proyecto.
- **`esquema.md`**: Diagrama de flujo que explica el funcionamiento de la simulación.

## 🔌 API Documentation

### Endpoints Disponibles

#### GET `/`
Endpoint de prueba que retorna información básica sobre la API.

**Response:**
```json
{
  "Esto es": "nuestro inventario"
}
```

#### POST `/simular`
Endpoint principal que ejecuta la simulación de políticas de inventario.

### Modelo SimulacionRequest

```python
class SimulacionRequest(BaseModel):
    inventario_inicial: int = Field(default=720)
    plazo_entrega_min: int = Field(default=1)
    plazo_entrega_max: int = Field(default=5)
    dias_simulacion: int = Field(default=365)
    anios_simulacion: int = Field(default=5)
    costo_almacenar: float = Field(default=150.0)
    costo_faltante: float = Field(default=380.0)
    costo_pedido_pequenio: float = Field(default=40.0)
    costo_pedido_grande: float = Field(default=30.0)
    precio_venta: float = Field(default=250.0)
    politicas_abastecimiento: List[PoliticaAbastecimiento]
    demanda: int = Field(default=200)
```

#### Parámetros del Modelo

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `inventario_inicial` | int | 720 | Inventario inicial en unidades |
| `plazo_entrega_min` | int | 1 | Plazo mínimo de entrega en días |
| `plazo_entrega_max` | int | 5 | Plazo máximo de entrega en días |
| `dias_simulacion` | int | 365 | Días por año de simulación |
| `anios_simulacion` | int | 5 | Número de años a simular |
| `costo_almacenar` | float | 150.0 | Costo por unidad por día de almacenamiento |
| `costo_faltante` | float | 380.0 | Costo por unidad de faltante |
| `costo_pedido_pequenio` | float | 40.0 | Costo por unidad para pedidos < 300 |
| `costo_pedido_grande` | float | 30.0 | Costo por unidad para pedidos ≥ 300 |
| `precio_venta` | float | 250.0 | Precio de venta por unidad |
| `politicas_abastecimiento` | List | Config | Lista de políticas (r, Q) a simular |
| `demanda` | int | 200 | Demanda media diaria (distribución Poisson) |

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

## 🧮 Lógica de Simulación

### Arquitectura de la Simulación

La simulación utiliza el **método de eventos discretos** para modelar el sistema de inventario. Los eventos principales son:
- **Eventos de Demanda**: Generación de demanda diaria con distribución Poisson
- **Eventos de Llegada de Pedidos**: Recepción de pedidos según plazos de entrega

### Método Principal: `simular_politica(r, Q, dias_simulacion, **kwargs)`

#### Parámetros de Entrada
- `r` (int): Punto de reorden (nivel de inventario que dispara un nuevo pedido)
- `Q` (int): Cantidad a pedir (tamaño del lote de reposición)
- `dias_simulacion` (int): Período total de simulación en días
- `**kwargs`: Parámetros adicionales de configuración

#### Flujo de Ejecución

1. **Inicialización:**
   ```python
   # Cargar parámetros desde configuración o kwargs
   inventario = kwargs.get("inventario_inicial", config.simulacion.get('inventario_inicial'))
   precio_venta = kwargs.get("precio_venta", config.precios.get('venta'))
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

## 📊 Diagrama de Flujo

Para una explicación visual detallada del funcionamiento de la simulación, consulta el [esquema de la simulación](esquema.md).

---

**Desarrollado para el curso de Modelos y Simulación - Trabajo Final**
