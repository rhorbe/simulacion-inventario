# Simulación de Inventario - API y Frontend

Sistema completo de simulación de políticas de inventario basado en el modelo (r, Q) implementado como API REST con FastAPI y frontend web interactivo, siguiendo principios de Domain-Driven Design (DDD) y arquitectura limpia.

## 📋 Tabla de Contenidos

- [Get Started](#get-started)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Arquitectura de Dominio](#arquitectura-de-dominio)
- [Patrón CQRS](#patrón-cqrs)
- [Sistema de Eventos](#sistema-de-eventos)
- [Inyección de Dependencias](#inyección-de-dependencias)
- [Sistema de Middlewares en los Buses](#sistema-de-middlewares-en-los-buses)
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
   uvicorn api.src.main:app --reload --host 0.0.0.0 --port 8000
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
uvicorn api.src.main:app --reload

# Ejecutar en modo producción
uvicorn api.src.main:app --host 0.0.0.0 --port 8000

# Ejecutar con logs detallados
uvicorn api.src.main:app --log-level debug

# Ejecutar tests
python -m pytest api/tests/ -v
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
                   "api.src.main:app",
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
               "program": "${workspaceFolder}/api/src/main.py",
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
   - Abrir `api/src/main.py` o `api/src/application/inventario.py`
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
     - **Parameters**: `api.src.main:app --reload --host 0.0.0.0 --port 8000`
     - **Working directory**: Seleccionar la carpeta del proyecto
     - **Python interpreter**: Seleccionar el intérprete correcto

3. **Configurar breakpoints:**
   - Abrir cualquier archivo `.py` en las carpetas `api/src/domain/`, `api/src/application/` o `api/src/infra/`
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
- `api/src/main.py`: Línea 30 (inicialización de buses)
- `api/src/application/inventario.py`: Línea 15 (clase `SimulacionInventario`)
- `api/src/application/inventario.py`: Línea 45 (método `ejecutar`)
- `api/src/infra/repository/yml_config_repository.py`: Línea 25 (carga de configuración)

## 📁 Estructura del Proyecto

```
simulacion-inventario/
├── api/                    # Backend - API y lógica de simulación
│   ├── src/               # Código fuente del backend
│   │   ├── domain/        # Capa de dominio - entidades y lógica de negocio
│   │   │   ├── bus/           # Interfaces de buses (CommandBus, EventBus)
│   │   │   ├── dto/           # Data Transfer Objects
│   │   │   ├── handlers/      # Interfaces de handlers
│   │   │   ├── models/        # Modelos de dominio
│   │   │   ├── value_objects/ # Value Objects del dominio
│   │   │   ├── object_mothers/ # Object Mothers para generación de valores aleatorios
│   │   │   ├── exceptions/    # Excepciones de dominio
│   │   │   ├── repository/    # Interfaces de repositorio
│   │   │   └── __init__.py
│   │   ├── application/   # Capa de aplicación - casos de uso
│   │   │   ├── commands/      # Comandos CQRS
│   │   │   ├── handlers/      # Handlers de comandos y eventos
│   │   │   ├── inventario.py  # Clase principal de simulación
│   │   │   └── __init__.py
│   │   ├── infra/         # Capa de infraestructura - interfaces externas
│   │   │   ├── bus/           # Implementaciones de buses
│   │   │   ├── controllers/   # Controladores de la API
│   │   │   ├── repository/    # Implementaciones de repositorios
│   │   │   └── __init__.py
│   │   ├── dependency_injection/ # Configuración de inyección de dependencias
│   │   │   ├── config_factory.py
│   │   │   ├── command_bus_factory.py
│   │   │   ├── event_bus_factory.py
│   │   │   ├── simulacion_factory.py
│   │   │   └── __init__.py
│   │   ├── main.py            # Punto de entrada de la aplicación FastAPI
│   │   └── __init__.py
│   ├── tests/             # Tests unitarios
│   │   ├── __init__.py
│   │   ├── test_cantidad.py
│   │   ├── test_precio.py
│   │   ├── test_plazo_de_entrega.py
│   │   ├── test_costo_pedido.py
│   │   ├── test_politica_inventario.py
│   │   ├── test_configuracion_simulacion.py
│   │   ├── test_object_mothers.py
│   │   ├── test_command_bus.py
│   │   ├── test_event_bus.py
│   │   ├── test_event_handlers.py
│   │   ├── test_eventos.py
│   │   ├── test_fel.py
│   │   ├── test_inventario.py
│   │   └── test_resultados.py
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

##### Punto de Entrada (`api/src/`)
- **`main.py`**: Punto de entrada de la aplicación FastAPI. Configura la aplicación, middleware CORS, inicializa buses y registra handlers y controladores.
- **`dependency_injection/`**: Configuración modular de inyección de dependencias
  - **`config_factory.py`**: Factory para configuración
  - **`command_bus_factory.py`**: Factory para CommandBus
  - **`event_bus_factory.py`**: Factory para EventBus
  - **`simulacion_factory.py`**: Factory para simulación (actualmente vacío)

##### Capa de Infraestructura (`api/src/infra/`)
- **`bus/`**: Implementaciones concretas de buses
  - **`in_memory_command_bus.py`**: Implementación en memoria del CommandBus
  - **`in_memory_event_bus.py`**: Implementación en memoria del EventBus
- **`controllers/`**: Controladores de la API REST
  - **`health_controller.py`**: Endpoint de health check (`/health`)
  - **`simulacion_controller.py`**: Endpoint principal de simulación (`/simular`) con inyección de dependencias
- **`repository/`**: Implementaciones concretas de repositorios
  - **`yml_config_repository.py`**: Implementación concreta de la interfaz Config que carga configuración desde archivos YAML
  - **`config.yml`**: Archivo de configuración centralizado con todos los parámetros de la simulación

##### Capa de Aplicación (`api/src/application/`)
- **`commands/`**: Comandos CQRS
  - **`simular_command.py`**: Comando para ejecutar simulación
- **`handlers/`**: Handlers de comandos y eventos
  - **`simular_command_handler.py`**: Handler que procesa el comando de simulación
  - **`demanda_handler.py`**: Handler para eventos de demanda
  - **`llegada_pedido_handler.py`**: Handler para eventos de llegada de pedidos
- **`inventario.py`**: Contiene la clase `SimulacionInventario` que encapsula toda la lógica de simulación del sistema de inventario.

##### Capa de Dominio (`api/src/domain/`)
- **`bus/`**: Interfaces de buses
  - **`command_bus.py`**: Interfaz del CommandBus
  - **`event_bus.py`**: Interfaz del EventBus
- **`handlers/`**: Interfaces de handlers
  - **`command_handler.py`**: Interfaz para handlers de comandos
  - **`event_handler.py`**: Interfaz para handlers de eventos
- **`dto/`**: Data Transfer Objects para comunicación entre capas
  - **`simulacion_request.py`**: DTO para recibir requests de simulación
  - **`politica_abastecimiento.py`**: DTO para representar políticas de abastecimiento
- **`models/`**: Modelos de dominio
  - **`evento.py`**: Define la jerarquía de eventos para la simulación discreta de eventos
  - **`simulation_context.py`**: Contexto de simulación unificado que encapsula resultados, configuración y política
  - **`fel.py`**: Define la clase FEL (Future Event List) para gestionar eventos futuros en la simulación
- **`value_objects/`**: Value Objects del dominio con validaciones de negocio
  - **`cantidad.py`**: Value Object para cantidades con validación de no negatividad
  - **`precio.py`**: Value Object para precios con validación de no negatividad
  - **`plazo_de_entrega.py`**: Value Object que encapsula plazo mínimo y máximo con validaciones
  - **`costo_pedido.py`**: Value Object que encapsula costos de pedido pequeño y grande
  - **`politica_inventario.py`**: Value Object para políticas de inventario (r, Q)
  - **`configuracion_simulacion.py`**: Value Object que encapsula toda la configuración
- **`object_mothers/`**: Object Mothers para generación de valores aleatorios
  - **`base_object_mother.py`**: Clase base abstracta para todos los Object Mothers
  - **`demanda_mother.py`**: Object Mother para generar demandas aleatorias (distribución Poisson)
  - **`tiempo_entrega_mother.py`**: Object Mother para generar tiempos de entrega aleatorios (distribución uniforme)
- **`exceptions/`**: Excepciones de dominio
  - **`domain_error.py`**: Excepción base para errores de dominio con mensajes claros
- **`repository/`**: Interfaces de repositorio
  - **`config.py`**: Interfaz abstracta Config que define el contrato para las fuentes de configuración

##### Tests (`api/tests/`)
- **`test_cantidad.py`**: Tests para el Value Object Cantidad
- **`test_precio.py`**: Tests para el Value Object Precio
- **`test_plazo_de_entrega.py`**: Tests para el Value Object PlazoDeEntrega
- **`test_costo_pedido.py`**: Tests para el Value Object CostoPedido
- **`test_politica_inventario.py`**: Tests para el Value Object PoliticaInventario
- **`test_configuracion_simulacion.py`**: Tests para el Value Object ConfiguracionSimulacion
- **`test_object_mothers.py`**: Tests para los Object Mothers (DemandaMother y TiempoEntregaMother)
- **`test_value_objects_with_defaults.py`**: Tests para Value Objects con valores por defecto
- **`test_eventos.py`**: Tests para la jerarquía de eventos (EventoBase, EventoDemanda, EventoLlegadaPedido)
- **`test_resultados.py`**: Tests para la clase SimulationContext (anteriormente ResultadosPolitica)
- **`test_fel.py`**: Tests para la clase FEL (Future Event List)
- **`test_command_bus.py`**: Tests para el CommandBus y handlers de comandos
- **`test_event_bus.py`**: Tests para el EventBus y handlers de eventos
- **`test_event_handlers.py`**: Tests para handlers de eventos específicos
- **`test_inventario.py`**: Tests para la clase SimulacionInventario

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

## 🏗️ Arquitectura de Dominio

### Patrón CQRS (Command Query Responsibility Segregation)

El sistema implementa un patrón CQRS simplificado para separar las operaciones de lectura y escritura:

#### CommandBus

```python
class CommandBus(ABC):
    @abstractmethod
    def register_handler(self, command_type: Type[T], handler: CommandHandler[T]) -> None:
        pass
    
    @abstractmethod
    def execute(self, command: T) -> Any:
        pass
```

**Características:**
- **Inyección de dependencias**: Los handlers reciben sus dependencias en el constructor
- **Registro dinámico**: Los handlers se registran en el arranque de la aplicación
- **Ejecución tipada**: Cada comando tiene su handler específico

#### Comandos

```python
@dataclass
class SimularCommand:
    politicas: List[PoliticaInventario]
    configuracion: ConfiguracionSimulacion
```

#### Handlers de Comandos

```python
class SimularCommandHandler(CommandHandler[SimularCommand]):
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    def handle(self, command: SimularCommand) -> List[dict]:
        resultados = []
        for politica in command.politicas:
            simulacion = SimulacionInventario(politica, command.configuracion, self.event_bus)
            resultados.append(simulacion.ejecutar())
        return resultados
```

### Sistema de Eventos

El sistema implementa un patrón de eventos para la simulación discreta de eventos:

#### EventBus

```python
class EventBus(ABC):
    @abstractmethod
    def register_handler(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        pass
    
    @abstractmethod
    def dispatch(self, evento: Evento, context: SimulationContext) -> None:
        pass
```

#### Handlers de Eventos

```python
class DemandaEventHandler(EventHandler[EventoDemanda]):
    def handle(self, evento: EventoDemanda, context: SimulationContext) -> None:
        cantidad = evento.get_cantidad()
        inventario_actual = context.obtener_inventario()
        precio_venta = context.configuracion.get_precio_venta()
        if inventario_actual >= cantidad:
            context.actualizar_inventario(-cantidad)
            context.agregar_ingreso(cantidad * precio_venta)
        else:
            context.agregar_ingreso(inventario_actual * precio_venta)
            context.agregar_costo_faltante((cantidad - inventario_actual) * context.configuracion.get_costo_faltante())
            context.establecer_inventario(0)

class LlegadaPedidoEventHandler(EventHandler[EventoLlegadaPedido]):
    def handle(self, evento: EventoLlegadaPedido, context: SimulationContext) -> None:
        cantidad = evento.get_cantidad()
        context.actualizar_inventario(cantidad)
```

### Inyección de Dependencias

El sistema utiliza inyección de dependencias para desacoplar componentes:

#### Factories

```python
# dependency_injection/command_bus_factory.py
def get_command_bus() -> CommandBus:
    return InMemoryCommandBus()

# dependency_injection/event_bus_factory.py
def get_event_bus() -> EventBus:
    return InMemoryEventBus()
```

#### Configuración en main.py

```python
# Inicialización y registro de handlers en los buses (singleton)
command_bus = get_command_bus()
event_bus = get_event_bus()

# Registrar handlers del EventBus
event_bus.register_handler(EventoDemanda, DemandaEventHandler())
event_bus.register_handler(EventoLlegadaPedido, LlegadaPedidoEventHandler())

# Registrar handler del CommandBus con EventBus como dependencia
command_bus.register_handler(SimularCommand, SimularCommandHandler(event_bus))
```

---

### Sistema de Middlewares en los Buses

Los buses (`CommandBus` y `EventBus`) soportan una cadena de middlewares que permite ejecutar lógica adicional antes y/o después de cada comando o evento. Esto es útil para logging, métricas, validación, manejo de errores, etc.

#### ¿Cómo funciona?

- Cada bus mantiene una lista de middlewares que se ejecutan en orden antes de llegar al handler final.
- Los middlewares implementan la interfaz `Middleware` y reciben un contexto y una función `next_middleware` para continuar la cadena.
- El contexto (`MiddlewareContext`) permite compartir información entre middlewares y el handler.
- Si no hay middlewares, el comando/evento se ejecuta directamente en el handler.

#### Ejemplo de registro de middlewares

```python
from api.src.domain.bus.middleware import Middleware

class LoggingMiddleware(Middleware):
    async def process(self, context, next_middleware):
        print(f"Ejecutando: {context.command_or_event}")
        result = await next_middleware(context)
        print(f"Finalizado: {context.command_or_event}")
        return result

# Crear el bus
command_bus = InMemoryCommandBus()

# Agregar el middleware
command_bus.add_middleware(LoggingMiddleware())

# Registrar handlers como siempre
command_bus.register_handler(SimularCommand, SimularCommandHandler(event_bus))
```

#### Orden de ejecución

1. El comando/evento entra al primer middleware.
2. Cada middleware puede ejecutar lógica antes y después de llamar a `await next_middleware(context)`.
3. Al final de la cadena, se ejecuta el handler correspondiente.

#### ¿Dónde agregar los middlewares?

- Los middlewares deben agregarse al bus antes de registrar los handlers y antes de ejecutar comandos/eventos.
- Se recomienda hacerlo en la inicialización de la aplicación (`main.py`).

#### Ejemplo de MiddlewareContext

```python
from api.src.domain.bus.middleware import MiddlewareContext

context = MiddlewareContext(command_or_event=mi_comando)
context.metadata["usuario"] = "admin"
```

#### Tests

El archivo `api/tests/test_middleware_chain.py` contiene ejemplos y tests unitarios que verifican el funcionamiento de la cadena de middlewares.

---

### Value Objects

El sistema implementa una capa de Value Objects siguiendo principios de Domain-Driven Design (DDD) para encapsular la lógica de negocio y validaciones de dominio.

#### Características de los Value Objects

- **Inmutabilidad**: Todos los Value Objects son inmutables (frozen dataclasses)
- **Validaciones de Dominio**: Cada Value Object valida sus reglas de negocio en el naming constructor
- **Naming Constructors**: Métodos `from_*` que actúan como constructores con nombres descriptivos
- **Excepciones de Dominio**: Errores de validación arrojan `DomainError` con mensajes claros
- **Configuración por Defecto**: Todos los Value Objects heredan de `BaseValueObject` que permite configurar valores por defecto

#### Clase Base: BaseValueObject

```python
class BaseValueObject(ABC):
    _default_config: Optional[Config] = None
    
    @classmethod
    def with_config(cls, config: Config) -> Type[T]:
        """Configura los valores por defecto para este tipo de Value Object."""
        cls._default_config = config
        return cls
    
    @classmethod
    def get_default_config(cls) -> Optional[Config]:
        """Obtiene la configuración por defecto establecida."""
        return cls._default_config
    
    @classmethod
    def clear_default_config(cls) -> None:
        """Limpia la configuración por defecto establecida."""
        cls._default_config = None
```

#### Uso de Configuración por Defecto

Los Value Objects pueden configurarse con valores por defecto usando el método `with_config`:

```python
# Configurar Value Objects con configuración por defecto
PoliticaInventarioConConfig = PoliticaInventario.with_config(config)
ConfiguracionSimulacionConConfig = ConfiguracionSimulacion.with_config(config)

# Usar los Value Objects configurados
politica = PoliticaInventarioConConfig.from_valores(20, 100)
configuracion = ConfiguracionSimulacionConConfig.from_parametros(...)

# Limpiar configuración cuando ya no se necesite
PoliticaInventarioConConfig.clear_default_config()
ConfiguracionSimulacionConConfig.clear_default_config()
```

#### Value Objects Implementados

##### `Cantidad`
```python
@dataclass(frozen=True)
class Cantidad(BaseValueObject):
    valor: int
    
    @classmethod
    def from_int(cls, valor: int) -> 'Cantidad':
        if valor < 0:
            raise DomainError("La cantidad no puede ser negativa")
        return cls(valor)
```

**Validaciones:**
- No puede ser negativa

##### `Precio`
```python
@dataclass(frozen=True)
class Precio(BaseValueObject):
    valor: float
    
    @classmethod
    def from_float(cls, valor: float) -> 'Precio':
        if valor < 0:
            raise DomainError("El precio no puede ser negativo")
        return cls(valor)
```

**Validaciones:**
- No puede ser negativo

##### `PlazoDeEntrega`
```python
@dataclass(frozen=True)
class PlazoDeEntrega(BaseValueObject):
    plazo_minimo: int
    plazo_maximo: int
    
    @classmethod
    def from_plazos(cls, plazo_minimo: int, plazo_maximo: int) -> 'PlazoDeEntrega':
        if plazo_minimo < 0:
            raise DomainError("El plazo mínimo de entrega no puede ser negativo")
        if plazo_maximo < 0:
            raise DomainError("El plazo máximo de entrega no puede ser negativo")
        if plazo_maximo < plazo_minimo:
            raise DomainError("El plazo máximo de entrega no puede ser menor al plazo mínimo")
        return cls(plazo_minimo, plazo_maximo)
```

**Validaciones:**
- Plazo mínimo no puede ser negativo
- Plazo máximo no puede ser negativo
- Plazo máximo no puede ser menor al plazo mínimo

##### `CostoPedido`
```python
@dataclass(frozen=True)
class CostoPedido(BaseValueObject):
    costo_pedido_pequeno: float
    costo_pedido_grande: float
    
    @classmethod
    def from_costos(cls, costo_pedido_pequeno: float, costo_pedido_grande: float) -> 'CostoPedido':
        if costo_pedido_pequeno < 0:
            raise DomainError("El costo de pedido pequeño no puede ser negativo")
        if costo_pedido_grande < 0:
            raise DomainError("El costo de pedido grande no puede ser negativo")
        if costo_pedido_pequeno <= costo_pedido_grande:
            raise DomainError("El costo de pedido pequeño debe ser mayor al costo de pedido grande")
        return cls(costo_pedido_pequeno, costo_pedido_grande)
    
    def calcular_costo_unitario(self, cantidad: int) -> float:
        return self.costo_pedido_pequeno if cantidad < 300 else self.costo_pedido_grande
```

**Validaciones:**
- Costo de pedido pequeño no puede ser negativo
- Costo de pedido grande no puede ser negativo
- Costo de pedido pequeño debe ser mayor al costo de pedido grande

**Comportamiento:**
- Calcula automáticamente el costo unitario según el tamaño del pedido (< 300: pequeño, ≥ 300: grande)

##### `PoliticaInventario`
```python
@dataclass(frozen=True)
class PoliticaInventario(BaseValueObject):
    punto_reorden: Cantidad
    cantidad_pedido: Cantidad
    
    @classmethod
    def from_valores(cls, punto_reorden: int, cantidad_pedido: int) -> 'PoliticaInventario':
        punto_reorden_vo = Cantidad.from_int(punto_reorden)
        cantidad_pedido_vo = Cantidad.from_int(cantidad_pedido)
        return cls(punto_reorden_vo, cantidad_pedido_vo)
```

**Validaciones:**
- Ambos valores deben ser no negativos (validado por `Cantidad`)

##### `ConfiguracionSimulacion`
```python
@dataclass(frozen=True)
class ConfiguracionSimulacion(BaseValueObject):
    inventario_inicial: Cantidad
    precio_venta: Precio
    costo_almacenar: Precio
    costo_faltante: Precio
    costo_pedido: CostoPedido
    plazo_entrega: PlazoDeEntrega
    demanda_media: Cantidad
    
    @classmethod
    def from_parametros(cls, inventario_inicial: int, precio_venta: float, ...) -> 'ConfiguracionSimulacion':
        return cls(
            inventario_inicial=Cantidad.from_int(inventario_inicial),
            precio_venta=Precio.from_float(precio_venta),
            # ... otros parámetros
        )
```

**Características:**
- Encapsula todos los parámetros de configuración
- Valida cada parámetro usando los Value Objects correspondientes
- Proporciona métodos getter para acceder a los valores primitivos

### Jerarquía de Eventos

El sistema implementa una jerarquía de clases para representar los diferentes tipos de eventos que ocurren durante la simulación discreta de eventos. Esta jerarquía permite una mejor tipificación y separación de responsabilidades.

#### Características de la Jerarquía de Eventos

- **Clase Base Abstracta**: `EventoBase` define la interfaz común para todos los eventos
- **Tipificación Específica**: Cada tipo de evento tiene su propia clase que hereda de `EventoBase`
- **Compatibilidad**: Se mantiene la clase `Evento` original para compatibilidad con código existente
- **Polimorfismo**: Todos los eventos pueden ser tratados de manera uniforme a través de la interfaz común

#### Clase Base: EventoBase

```python
class EventoBase(ABC):
    """
    Clase base abstracta para todos los eventos de la simulación.
    Define la interfaz común que deben implementar todos los eventos.
    """
    
    @abstractmethod
    def get_dia(self) -> int:
        """Retorna el día en que ocurre el evento."""
        pass
    
    @abstractmethod
    def get_tipo(self) -> str:
        """Retorna el tipo del evento."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Representación en string del evento."""
        pass
```

#### Eventos Específicos Implementados

##### `EventoDemanda`
```python
@dataclass
class EventoDemanda(EventoBase):
    """
    Evento que representa una demanda de productos.
    """
    dia: int
    cantidad: int
    
    def get_tipo(self) -> str:
        return "demanda"
```

**Características:**
- Representa una demanda de productos en un día específico
- Contiene la cantidad demandada
- Tipo fijo: "demanda"

##### `EventoLlegadaPedido`
```python
@dataclass
class EventoLlegadaPedido(EventoBase):
    """
    Evento que representa la llegada de un pedido.
    """
    dia: int
    cantidad: int
    
    def get_tipo(self) -> str:
        return "llegada_pedido"
```

**Características:**
- Representa la llegada de un pedido en un día específico
- Contiene la cantidad que llega
- Tipo fijo: "llegada_pedido"

#### Clase de Compatibilidad: Evento

```python
@dataclass
class Evento(EventoBase):
    """
    Clase de compatibilidad que mantiene la interfaz original.
    Se recomienda usar las clases específicas EventoDemanda y EventoLlegadaPedido.
    """
    tipo: str
    dia: int
    cantidad: int = 0
```

**Características:**
- Mantiene la interfaz original para compatibilidad
- Permite especificar el tipo de evento dinámicamente
- Se recomienda migrar al uso de clases específicas

#### Uso de la Jerarquía de Eventos

```python
# Crear eventos específicos (recomendado)
evento_demanda = EventoDemanda(dia=5, cantidad=10)
evento_llegada = EventoLlegadaPedido(dia=10, cantidad=50)

# Los eventos pueden ser tratados de manera uniforme
eventos = [evento_demanda, evento_llegada]
for evento in eventos:
    print(f"Evento {evento.get_tipo()} en día {evento.get_dia()}")

# Ordenar eventos por día
eventos_ordenados = sorted(eventos, key=lambda x: x.get_dia())
```

#### Integración en la Simulación

Los Object Mothers se integran en la lógica de simulación de la siguiente manera:

```python
# En SimulacionInventario
class SimulacionInventario:
    def _inicializar_fel(self) -> FEL:
        return FEL([
            (EventoDemanda(
                0,
                DemandaMother.random(seed=42).value(self.configuracion.get_demanda_media())
            ))
        ])
    
    def _calcular_dia_entrega(self, evento: Evento) -> int:
        return evento.get_dia() + TiempoEntregaMother.random(seed=42).value(
            self.configuracion.get_plazo_entrega_min(),
            self.configuracion.get_plazo_entrega_max()
        )
```

#### Beneficios del Nuevo Diseño

- **Extensibilidad**: Agregar nuevos tipos de eventos o lógica es tan simple como crear un nuevo handler.
- **Testabilidad**: Cada componente puede ser testeado de forma aislada.
- **Desacoplamiento**: La lógica de eventos, resultados y configuración está separada y desacoplada.
- **Claridad**: El flujo de la simulación es explícito y fácil de seguir.
- **Reutilización**: El mismo ciclo de simulación puede ser usado para diferentes políticas y configuraciones.

#### Ejemplo de Handler de Evento

```python
@dataclass
class DemandaEventHandler:
    def can_handle(self, evento):
        return evento.__class__.__name__ == 'EventoDemanda'
    def handle(self, evento, context):
        cantidad = evento.get_cantidad()
        inventario_actual = context.obtener_inventario()
        precio_venta = context.configuracion.get_precio_venta()
        if inventario_actual >= cantidad:
            context.actualizar_inventario(-cantidad)
            context.agregar_ingreso(cantidad * precio_venta)
        else:
            context.agregar_ingreso(inventario_actual * precio_venta)
            context.agregar_costo_faltante((cantidad - inventario_actual) * context.configuracion.get_costo_faltante())
            context.establecer_inventario(0)
```

#### Ejemplo de uso del EventBus

```python
event_bus = InMemoryEventBus()
event_bus.register_handler(EventoDemanda, DemandaEventHandler())
event_bus.register_handler(EventoLlegadaPedido, LlegadaPedidoEventHandler())
event_bus.dispatch(evento, context)
```

### SimulationContext Unificado

El sistema utiliza una clase `SimulationContext` unificada que combina la funcionalidad anterior de `ResultadosPolitica` y `SimulationContext`. Esta clase encapsula:

- **Atributos de la política**: `r` (punto de reorden), `Q` (cantidad de pedido), `inventario`
- **Atributos de costos e ingresos**: `costo_almacenamiento`, `costo_total_faltante`, `costo_pedidos`, `ingresos`
- **Referencias**: `politica`, `configuracion`

#### Características de SimulationContext

```python
@dataclass
class SimulationContext:
    # Atributos de la política
    r: int
    Q: int
    inventario: int
    
    # Atributos de costos e ingresos
    costo_almacenamiento: float = 0.0
    costo_total_faltante: float = 0.0
    costo_pedidos: float = 0.0
    ingresos: float = 0.0
    
    # Referencias a la política y configuración
    politica: PoliticaInventario = None
    configuracion: ConfiguracionSimulacion = None
    
    @classmethod
    def from_politica_and_config(cls, politica: PoliticaInventario, configuracion: ConfiguracionSimulacion) -> 'SimulationContext':
        return cls(
            r=politica.get_punto_reorden(),
            Q=politica.get_cantidad_pedido(),
            inventario=configuracion.get_inventario_inicial(),
            politica=politica,
            configuracion=configuracion
        )
    
    def agregar_costo_almacenamiento(self, costo: float) -> None:
        self.costo_almacenamiento += costo
    
    def agregar_costo_faltante(self, costo: float) -> None:
        self.costo_total_faltante += costo
    
    def agregar_costo_pedido(self, costo: float) -> None:
        self.costo_pedidos += costo
    
    def agregar_ingreso(self, ingreso: float) -> None:
        self.ingresos += ingreso
    
    def actualizar_inventario(self, cantidad: int) -> None:
        self.inventario += cantidad
    
    def establecer_inventario(self, cantidad: int) -> None:
        self.inventario = cantidad
    
    def obtener_inventario(self) -> int:
        return self.inventario
    
    def calcular_ganancia(self) -> float:
        costo_total = self.costo_almacenamiento + self.costo_total_faltante + self.costo_pedidos
        return self.ingresos - costo_total
    
    def to_dict(self) -> dict:
        return {
            "r": self.r,
            "Q": self.Q,
            "ingresos": self.ingresos,
            "costo_alm": self.costo_almacenamiento,
            "costo_faltante": self.costo_total_faltante,
            "costo_pedidos": self.costo_pedidos,
            "ganancia": self.calcular_ganancia(),
        }
```

**Beneficios de la unificación:**
- **Simplicidad**: Una sola clase maneja tanto el contexto como los resultados
- **Cohesión**: Todos los datos relacionados están en un solo lugar
- **Acceso directo**: No hay necesidad de acceder a `context.resultados`
- **Mantenibilidad**: Menos clases para mantener y entender

---

El resto de la documentación sobre Value Objects, Object Mothers y FEL sigue siendo válida y complementa la arquitectura orientada a objetos.

Para más detalles, consulta la sección de tests y los ejemplos de código en `api/tests/`.

## 📊 Diagrama de Flujo

Para una explicación visual detallada del funcionamiento de la simulación, consulta el [esquema de la simulación](esquema.md).

---

**Desarrollado para el curso de Modelos y Simulación - Trabajo Final**