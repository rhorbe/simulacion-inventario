# Simulación de Inventario - API y Frontend

Sistema completo de simulación de políticas de inventario basado en el modelo (r, Q) implementado como API REST con FastAPI y frontend web interactivo.

## 📋 Tabla de Contenidos

- [Get Started](#get-started)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Arquitectura de Dominio](#arquitectura-de-dominio)
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
- `api/main.py`: Línea 30 (función `simular`)
- `api/application/inventario.py`: Línea 95 (inicio de `simular_politica`)
- `api/application/inventario.py`: Línea 120 (procesamiento de eventos)
- `api/infra/repository/yml_config_repository.py`: Línea 25 (carga de configuración)

## 📁 Estructura del Proyecto

```
simulacion-inventario/
├── api/                    # Backend - API y lógica de simulación
│   ├── src/               # Código fuente del backend
│   │   ├── domain/        # Capa de dominio - entidades y lógica de negocio
│   │   │   ├── dto/           # Data Transfer Objects
│   │   │   ├── models/        # Modelos de dominio
│   │   │   ├── value_objects/ # Value Objects del dominio
│   │   │   ├── object_mothers/ # Object Mothers para generación de valores aleatorios
│   │   │   ├── exceptions/    # Excepciones de dominio
│   │   │   ├── repository/    # Interfaces de repositorio
│   │   │   └── __init__.py
│   │   ├── application/   # Capa de aplicación - casos de uso
│   │   ├── infra/         # Capa de infraestructura - interfaces externas
│   │   │   ├── controllers/   # Controladores de la API
│   │   │   ├── repository/    # Implementaciones de repositorios
│   │   │   └── __init__.py
│   │   ├── dependency_injection.py  # Configuración de inyección de dependencias
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
│   │   └── test_object_mothers.py
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
- **`inventario.py`**: Contiene toda la lógica de simulación del sistema de inventario. Está completamente desacoplado de la configuración y recibe ValueObjects como parámetros.

##### Capa de Dominio (`api/src/domain/`)
- **`dto/`**: Data Transfer Objects para comunicación entre capas
  - **`simulacion_request.py`**: DTO para recibir requests de simulación
  - **`politica_abastecimiento.py`**: DTO para representar políticas de abastecimiento
- **`models/`**: Modelos de dominio
  - **`evento.py`**: Define la jerarquía de eventos para la simulación discreta de eventos
  - **`resultados.py`**: Define la clase ResultadosPolitica para encapsular los resultados de la simulación
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
- **`test_resultados.py`**: Tests para la clase ResultadosPolitica
- **`test_fel.py`**: Tests para la clase FEL (Future Event List)

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

Los eventos específicos se integran en la lógica de simulación:

```python
# Crear evento de demanda inicial
lista_eventos = [EventoDemanda(0, DemandaMother.random(seed=42).value(demanda_media))]

# Procesar eventos según su tipo
if evento_actual.get_tipo() == "demanda":
    # Procesar demanda
    pass
elif evento_actual.get_tipo() == "llegada_pedido":
    # Procesar llegada de pedido
    pass

# Crear nuevo evento de llegada de pedido
nuevoPedido = EventoLlegadaPedido(
    dia + TiempoEntregaMother.random(seed=42).value(plazo_min, plazo_max),
    cantidad_pedido
)
```

#### Beneficios de la Jerarquía de Eventos

1. **Tipificación Fuerte**: Cada tipo de evento tiene su propia clase con tipos específicos
2. **Mejor Legibilidad**: El código es más claro al usar `EventoDemanda` en lugar de `Evento(tipo="demanda", ...)`
3. **Extensibilidad**: Fácil agregar nuevos tipos de eventos heredando de `EventoBase`
4. **Validación de Tipos**: El compilador puede detectar errores de tipos en tiempo de compilación
5. **Polimorfismo**: Todos los eventos pueden ser tratados uniformemente a través de la interfaz común
6. **Compatibilidad**: Se mantiene la clase original para no romper código existente

### Clase ResultadosPolitica

El sistema implementa una clase `ResultadosPolitica` para encapsular y gestionar todos los resultados acumulados durante la simulación de inventario para una política específica. Esta clase proporciona una interfaz limpia para manejar costos e ingresos junto con los parámetros de la política.

#### Características de la Clase ResultadosPolitica

- **Encapsulación**: Agrupa todas las variables de resultados en un solo objeto
- **Parámetros de Política**: Incluye los atributos `r` (punto de reorden) y `Q` (cantidad de pedido)
- **Métodos de Acumulación**: Proporciona métodos específicos para agregar cada tipo de costo o ingreso
- **Cálculo Automático**: Calcula automáticamente la ganancia total
- **Conversión a Diccionario**: Convierte los resultados al formato esperado por la API

#### Implementación de la Clase

```python
@dataclass
class ResultadosPolitica:
    """
    Clase que encapsula los resultados de la simulación de inventario para una política específica.
    Contiene todos los costos e ingresos acumulados durante la simulación, junto con los parámetros de la política.
    """
    r: int
    Q: int
    costo_almacenamiento: float = 0.0
    costo_total_faltante: float = 0.0
    costo_pedidos: float = 0.0
    ingresos: float = 0.0
    
    def agregar_costo_almacenamiento(self, costo: float) -> None:
        """Agrega un costo de almacenamiento al total acumulado."""
        self.costo_almacenamiento += costo
    
    def agregar_costo_faltante(self, costo: float) -> None:
        """Agrega un costo por faltante al total acumulado."""
        self.costo_total_faltante += costo
    
    def agregar_costo_pedido(self, costo: float) -> None:
        """Agrega un costo de pedido al total acumulado."""
        self.costo_pedidos += costo
    
    def agregar_ingreso(self, ingreso: float) -> None:
        """Agrega un ingreso al total acumulado."""
        self.ingresos += ingreso
    
    def calcular_ganancia(self) -> float:
        """Calcula la ganancia total (ingresos - costos totales)."""
        costo_total = self.costo_almacenamiento + self.costo_total_faltante + self.costo_pedidos
        return self.ingresos - costo_total
    
    def to_dict(self) -> dict:
        """Convierte los resultados a un diccionario con el formato esperado por la API."""
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

#### Uso de la Clase ResultadosPolitica

```python
# Crear objeto de resultados con parámetros de política
resultados = ResultadosPolitica(r=10, Q=50)

# Acumular costos e ingresos durante la simulación
resultados.agregar_ingreso(ventas * precio_venta)
resultados.agregar_costo_faltante(faltante * costo_faltante)
resultados.agregar_costo_pedido(costo_pedido)
resultados.agregar_costo_almacenamiento(inventario * costo_almacenar)

# Obtener resultados finales
dict_resultado = resultados.to_dict()
```

#### Integración en la Simulación

La clase `ResultadosPolitica` se integra en la función principal de simulación:

```python
def simular_politica(politica: PoliticaInventario, dias_simulacion: int, configuracion: ConfiguracionSimulacion):
    # Inicializar resultados con parámetros de la política
    resultados = ResultadosPolitica(
        r=politica.get_punto_reorden(),
        Q=politica.get_cantidad_pedido()
    )
    
    # Durante la simulación, acumular resultados
    if isinstance(evento_actual, EventoDemanda):
        ventas = min(d, inventario)
        faltante = max(0, d - inventario)
        
        inventario -= ventas
        resultados.agregar_ingreso(ventas * configuracion.get_precio_venta())
        resultados.agregar_costo_faltante(faltante * configuracion.get_costo_faltante())
    
    # Al final, retornar resultados
    return resultados.to_dict()
```

#### Beneficios de la Clase ResultadosPolitica

1. **Encapsulación**: Agrupa todas las variables relacionadas en un solo objeto
2. **Parámetros de Política**: Incluye los parámetros `r` y `Q` como parte del objeto
3. **Métodos Específicos**: Cada tipo de costo/ingreso tiene su propio método de acumulación
4. **Cálculo Centralizado**: La ganancia se calcula automáticamente
5. **Mejor Legibilidad**: El código es más claro y expresivo
6. **Facilidad de Testing**: Es más fácil testear la lógica de acumulación
7. **Extensibilidad**: Fácil agregar nuevos tipos de costos o ingresos
8. **Asociación Directa**: Los resultados están directamente asociados con los parámetros de la política

### Clase FEL (Future Event List)

El sistema implementa una clase `FEL` (Future Event List) para encapsular y gestionar la lista de eventos futuros en la simulación discreta de eventos. Esta clase proporciona una interfaz limpia para manejar eventos ordenados cronológicamente.

#### Características de la Clase FEL

- **Ordenamiento Automático**: Los eventos se ordenan automáticamente por tiempo de ocurrencia
- **Gestión de Eventos**: Proporciona métodos para agregar, obtener y consultar eventos
- **Encapsulación**: Oculta la lógica de gestión de la lista de eventos
- **Interfaz Limpia**: Métodos específicos para cada operación de gestión de eventos

#### Implementación de la Clase

```python
class FEL:
    """
    Future Event List (FEL) - Lista de eventos futuros para simulación discreta de eventos.
    Encapsula la lógica de gestión de eventos ordenados por tiempo de ocurrencia.
    """
    
    def __init__(self):
        """Inicializa una lista de eventos futuros vacía."""
        self._eventos: List[EventoBase] = []
    
    def agregar_evento(self, evento: EventoBase) -> None:
        """Agrega un evento a la lista y mantiene el orden cronológico."""
        self._eventos.append(evento)
        self._ordenar_eventos()
    
    def obtener_siguiente_evento(self) -> Optional[EventoBase]:
        """Obtiene y remueve el próximo evento de la lista (el de menor tiempo)."""
        if not self._eventos:
            return None
        return self._eventos.pop(0)
    
    def hay_eventos(self) -> bool:
        """Verifica si hay eventos en la lista."""
        return len(self._eventos) > 0
    
    def hay_eventos_futuros_en_dia(self, dia: int) -> bool:
        """Verifica si hay eventos programados para un día específico o posterior."""
        return any(evento.get_dia() >= dia for evento in self._eventos)
    
    def obtener_proximo_dia_evento(self) -> Optional[int]:
        """Obtiene el día del próximo evento sin removerlo de la lista."""
        if not self._eventos:
            return None
        return self._eventos[0].get_dia()
    
    def _ordenar_eventos(self) -> None:
        """Ordena los eventos por día de ocurrencia (ascendente)."""
        self._eventos.sort(key=lambda x: x.get_dia())
```

#### Uso de la Clase FEL

```python
# Crear FEL vacía
fel = FEL()

# Agregar eventos (se ordenan automáticamente)
fel.agregar_evento(EventoDemanda(dia=3, cantidad=10))
fel.agregar_evento(EventoDemanda(dia=1, cantidad=5))
fel.agregar_evento(EventoDemanda(dia=2, cantidad=8))

# Verificar si hay eventos
if fel.hay_eventos():
    # Obtener el próximo evento (día 1)
    evento = fel.obtener_siguiente_evento()
    
# Verificar eventos futuros
if not fel.hay_eventos_futuros_en_dia(dia + 1):
    # Crear nuevo evento para el día siguiente
    nuevo_evento = EventoDemanda(dia + 1, cantidad)
    fel.agregar_evento(nuevo_evento)
```

#### Integración en la Simulación

La clase `FEL` se integra en la función principal de simulación:

```python
def simular_politica(politica: PoliticaInventario, dias_simulacion: int, configuracion: ConfiguracionSimulacion):
    # Inicializar FEL con evento inicial
    fel = FEL()
    fel.agregar_evento(EventoDemanda(0, DemandaMother.random(seed=42).value(demanda_media))]
    
    # Bucle principal de simulación
    while fel.hay_eventos():
        evento_actual = fel.obtener_siguiente_evento()
        
        # Procesar evento según su tipo
        if isinstance(evento_actual, EventoDemanda):
            # Procesar demanda
            pass
        elif isinstance(evento_actual, EventoLlegadaPedido):
            # Procesar llegada de pedido
            pass
        
        # Crear nuevos eventos si es necesario
        if nuevo_pedido:
            fel.agregar_evento(nuevo_pedido)
        
        # Verificar si necesitamos crear nueva demanda
        if not fel.hay_eventos_futuros_en_dia(dia + 1):
            nueva_demanda = EventoDemanda(dia + 1, cantidad)
            fel.agregar_evento(nueva_demanda)
```

#### Beneficios de la Clase FEL

1. **Encapsulación**: Oculta la lógica de gestión de la lista de eventos
2. **Ordenamiento Automático**: Los eventos se mantienen ordenados cronológicamente
3. **Interfaz Limpia**: Métodos específicos para cada operación
4. **Facilidad de Testing**: Es más fácil testear la lógica de gestión de eventos
5. **Extensibilidad**: Fácil agregar nuevas funcionalidades de gestión de eventos
6. **Separación de Responsabilidades**: La gestión de eventos está separada de la lógica de simulación
7. **Reutilización**: La clase puede ser reutilizada en otras simulaciones discretas de eventos

### Object Mothers

El sistema implementa el patrón **Object Mother** para encapsular la lógica de generación de valores aleatorios utilizados en la simulación. Este patrón permite separar la responsabilidad de generar datos de prueba o valores aleatorios del resto de la lógica de negocio.

#### Características de los Object Mothers

- **Herencia de Clase Base**: Todos los Object Mothers heredan de `BaseObjectMother`
- **Método de Clase `random(seed)`**: Cada Object Mother tiene un método de clase que devuelve una instancia configurada con la semilla especificada
- **Método de instancia `value(...)`**: Permite generar el valor aleatorio de forma fluida, sin necesidad de instanciar variables auxiliares
- **Generadores Independientes**: Cada Object Mother mantiene su propio generador de números aleatorios
- **Configurabilidad**: Permite cambiar semillas para reproducibilidad de resultados
- **Testabilidad**: Fácil testing de la lógica de generación de valores

#### Clase Base: BaseObjectMother

```python
class BaseObjectMother(ABC):
    """
    Clase base abstracta para todos los Object Mother del dominio.
    """
    @classmethod
    @abstractmethod
    def random(cls, seed):
        """
        Devuelve una instancia del Object Mother con la semilla indicada.
        """
        pass
```

#### Object Mothers Implementados

##### `DemandaMother`
```python
class DemandaMother(BaseObjectMother):
    def __init__(self, seed: Optional[int] = 42):
        self.generador_aleatorio = np.random.default_rng(seed=seed)
    
    def value(self, demanda_media: int) -> int:
        """Genera una demanda aleatoria usando distribución de Poisson."""
        return self.generador_aleatorio.poisson(demanda_media)
    
    @classmethod
    def random(cls, seed=42):
        return cls(seed=seed)
```

**Características:**
- Genera demandas aleatorias usando distribución de Poisson
- Utiliza `numpy.random.default_rng` para generación de números aleatorios
- Parámetro: `demanda_media` (media de la distribución Poisson)

##### `TiempoEntregaMother`
```python
class TiempoEntregaMother(BaseObjectMother):
    def __init__(self, seed: Optional[int] = 42):
        self.generador_aleatorio = random.Random(seed)
    
    def value(self, plazo_min: int, plazo_max: int) -> int:
        """Genera un tiempo de entrega aleatorio usando distribución uniforme."""
        return self.generador_aleatorio.randint(plazo_min, plazo_max)
    
    @classmethod
    def random(cls, seed=42):
        return cls(seed=seed)
```

**Características:**
- Genera tiempos de entrega aleatorios usando distribución uniforme
- Utiliza `random.Random` para generación de números aleatorios
- Parámetros: `plazo_min` y `plazo_max` (rango de la distribución uniforme)

#### Uso de Object Mothers

```python
# Llamada fluida sin necesidad de instanciar variables auxiliares
demanda = DemandaMother.random(seed=42).value(demanda_media=10)
tiempo = TiempoEntregaMother.random(seed=42).value(plazo_min=1, plazo_max=5)

# También se puede reutilizar la instancia si se desea:
demanda_gen = DemandaMother.random(seed=42)
demanda1 = demanda_gen.value(10)
demanda2 = demanda_gen.value(10)
```

#### Integración en la Simulación

Los Object Mothers se integran en la lógica de simulación de la siguiente manera:

```python
# En simular_politica()
lista_eventos = [Evento("demanda", 0, DemandaMother.random(seed=42).value(demanda_media))]

# Al procesar eventos de demanda
if not existen_eventos_pendientes(lista_eventos, dia + 1):
    nueva_demanda = Evento("demanda", dia + 1, DemandaMother.random(seed=42).value(demanda_media))
    lista_eventos.append(nueva_demanda)

# Al generar pedidos
nuevoPedido = Evento("llegada_pedido", 
                     dia + TiempoEntregaMother.random(seed=42).value(plazo_entrega_min, plazo_entrega_max), 
                     Q)
```

#### Beneficios del Patrón Object Mother

1. **Separación de Responsabilidades**: La lógica de generación de valores aleatorios está encapsulada en clases específicas
2. **Reutilización**: Los Object Mothers pueden ser usados en otros contextos (tests, diferentes simulaciones)
3. **Testabilidad**: Cada Object Mother puede ser testeado independientemente
4. **Configurabilidad**: Fácil cambio de semillas para reproducibilidad de resultados
5. **Extensibilidad**: Fácil agregar nuevos tipos de generadores heredando de `BaseObjectMother`
6. **Mantenibilidad**: Cambios en la lógica de generación solo afectan a los Object Mothers correspondientes

#### Testing de Object Mothers

```bash
# Ejecutar tests de Object Mothers
python -m pytest tests/test_object_mothers.py -v

# Tests específicos
python -m pytest tests/test_object_mothers.py::TestDemandaMother -v
python -m pytest tests/test_object_mothers.py::TestTiempoEntregaMother -v
```

### Excepciones de Dominio

```python
class DomainError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
```

**Características:**
- Excepción base para todos los errores de dominio
- Mensajes claros y descriptivos para cada validación fallida
- Facilita el debugging y la identificación de problemas

### Beneficios de la Refactorización

1. **Validaciones Centralizadas**: Todas las validaciones de negocio están encapsuladas en los Value Objects
2. **Código Más Limpio**: La capa de aplicación recibe objetos validados en lugar de tipos primitivos
3. **Mejor Mantenibilidad**: Cambios en las reglas de negocio solo requieren modificar los Value Objects
4. **Testing Mejorado**: Tests unitarios específicos para cada Value Object
5. **Documentación Viva**: Los Value Objects documentan las reglas de negocio en el código
6. **Prevención de Errores**: Validaciones tempranas evitan errores en tiempo de ejecución
7. **Configuración por Defecto**: Los Value Objects pueden configurarse con valores por defecto desde la configuración

### Ejecución de Tests

```bash
# Ejecutar todos los tests
python -m pytest api/tests/ -v

# Ejecutar tests específicos
python -m pytest api/tests/test_cantidad.py -v
python -m pytest api/tests/test_precio.py -v
python -m pytest api/tests/test_base_value_object.py -v
python -m pytest api/tests/test_object_mothers.py -v
python -m pytest api/tests/test_value_objects.py -v
python -m pytest api/tests/test_eventos.py -v
python -m pytest api/tests/test_resultados.py -v
python -m pytest api/tests/test_fel.py -v
```

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
2. **Validación de Dominio**: El controlador crea ValueObjects que validan las reglas de negocio
3. **Procesamiento**: El controlador itera sobre las políticas y llama a `simular_politica` para cada una
4. **Simulación**: Cada política se simula de forma independiente usando ValueObjects validados
5. **Resultados**: Se retornan los resultados de todas las políticas simuladas

### Método Principal: `simular_politica(politica, dias_simulacion, configuracion)`

#### Parámetros de Entrada
- `politica` (PoliticaInventario): Política de inventario (r, Q) validada
- `dias_simulacion` (int): Período total de simulación en días
- `configuracion` (ConfiguracionSimulacion): Configuración completa validada

#### Flujo de Ejecución

1. **Inicialización con ValueObjects:**
   ```python
   # Obtener valores validados desde los ValueObjects
   inventario = configuracion.get_inventario_inicial()
   precio_venta = configuracion.get_precio_venta()
   costo_almacenar = configuracion.get_costo_almacenar()
   costo_por_faltante = configuracion.get_costo_faltante()
   demanda_media = configuracion.get_demanda_media()
   plazo_entrega_min = configuracion.get_plazo_entrega_min()
   plazo_entrega_max = configuracion.get_plazo_entrega_max()
   
   # Obtener valores de la política
   r = politica.get_punto_reorden()
   Q = politica.get_cantidad_pedido()
   
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

4. **Lógica de Reposición con ValueObjects:**
   ```python
   if inventario < r:  # Si inventario cae bajo punto de reorden
       nuevoPedido = Evento("llegada_pedido", dia + generar_tiempo_entrega(plazo_entrega_min, plazo_entrega_max), Q)
       costo_pedidos += Q * configuracion.calcular_costo_unitario_pedido(Q)
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
- **Validaciones de Dominio**: Todos los parámetros son validados por ValueObjects antes de la simulación
- **Desacoplamiento**: El módulo de simulación recibe objetos validados en lugar de tipos primitivos

### Beneficios de la Refactorización en la Simulación

1. **Validaciones Tempranas**: Los ValueObjects validan los parámetros antes de iniciar la simulación
2. **Código Más Limpio**: La función `simular_politica` recibe objetos con significado semántico
3. **Prevención de Errores**: Imposible pasar parámetros inválidos a la simulación
4. **Mejor Testing**: Los ValueObjects pueden ser testeados independientemente
5. **Documentación Viva**: Las reglas de negocio están codificadas en los ValueObjects

## 📊 Diagrama de Flujo

Para una explicación visual detallada del funcionamiento de la simulación, consulta el [esquema de la simulación](esquema.md).

---

**Desarrollado para el curso de Modelos y Simulación - Trabajo Final**