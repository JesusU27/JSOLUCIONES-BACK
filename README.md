# PRUEBA TÉCNICA (JESÚS URIBE)

## SECCIÓN 1 – PYTHON AVANZADO (25%)

### 1. Explicar la diferencia entre lista, tupla, set y diccionario (con ejemplos).

#### **Lista (list)**

- Ordenada

- Mutable (se puede modificar)

- Permite elementos duplicados

```
numeros = [1, 2, 3, 3]
numeros.append(4)
print(numeros)

```

**Uso común:** colecciones que cambian (carrito de compras, resultados, etc.)

#### **Tupla (tuple)**

- Ordenada

- Inmutable (no se puede modificar)

- Permite duplicados

```
coordenadas = (10, 20)
print(coordenadas[0])
```

**Uso común:** datos que no deben cambiar (configuraciones, coordenadas).

#### **Set (set)**

- No ordenado

- No permite duplicados

- Mutable

```
valores = {1, 2, 3, 3}
print(valores)  # {1, 2, 3}

```


**Uso común:** eliminar duplicados, operaciones matemáticas (uniones, intersecciones).

#### **Diccionario (dict)**

- Colección de clave : valor

- Mutable

- Claves únicas

```
persona = {
    "nombre": "Ana",
    "edad": 25
}
print(persona["nombre"])

```

**Uso común:** representar entidades (usuarios, productos, configuraciones).


### 2. ¿Qué es una comprensión de listas y cuándo usarla?

Es una forma corta y legible de crear listas a partir de otra secuencia.

Ejemplo tradicional:

```
cuadrados = []
for i in range(5):
    cuadrados.append(i ** 2)

```
Con comprensión de listas:
```
cuadrados = [i ** 2 for i in range(5)]

```

Se usa cuando:

- la lógica es simple

- Se quiere mejorar legibilidad y reducir líneas de código

- Se quiere evitar bucles largos innecesarios


### 3. Crear una función que use *args y **kwargs.

***args:** Permite recibir n cantidad de argumentos posicionales.

****kwargs:** Permite recibir n cantidad de argumentos con nombre.

```
def ejemplo(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

ejemplo(1, 2, 3, nombre="Carlos", edad=30)

```

Salida:

```
Args: (1, 2, 3)
Kwargs: {'nombre': 'Carlos', 'edad': 30}
```

**Uso común:** funciones genéricas, frameworks, wrappers.

### 4. Explicar qué es un decorador

Un decorador es una función que modifica o extiende el comportamiento de otra función sin cambiar su código original.

Se usan mucho para:

- Autenticación

- Logs

- Medición de tiempo

- Validaciones

**Ejemplo conceptual (sin implementación):**

```
@mi_decorador
def funcion():
    pass

```

**(Python ejecuta primero el decorador y luego la función decorada)**


## SECCIÓN 2 – LÓGICA Y MANEJO DE DATOS (20%)

### 1. Calculen ingresos totales.
### 2. Filtren transacciones por rango de fechas.
### 3. Obtengan el cliente con mayor consumo.
### 4. Manejen errores de datos inválidos.


## SECCIÓN 3 – DISEÑO Y BUENAS PRÁCTICAS (20%)

### 1. Diseñar la estructura de carpetas de un proyecto Python.

Para la realización del proyecto solicitado en la sección 4, se usará esta arquitectura:

```
erp_ventas/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py                # TimeStampedModel base
│   │   ├── permissions.py           # IsOwner permission
│   │   ├── exceptions.py
│   │   └── mixins.py
│   │
│   ├── clientes/                    # Módulo de Usuarios/Clientes
│   │   ├── __init__.py
│   │   ├── models.py                # Cliente (extends AbstractUser)
│   │   ├── serializers.py           # Register, Login, Profile
│   │   ├── views.py                 # Register, Login, Profile, MyPurchases
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── productos/
│   │   ├── __init__.py
│   │   ├── models.py                # Producto
│   │   ├── serializers.py
│   │   ├── views.py                 # Listar productos (público/autenticado)
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   └── ventas/
│       ├── __init__.py
│       ├── models.py                # Venta, DetalleVenta
│       ├── serializers.py
│       ├── views.py                 # Crear venta, Mis compras, Estadísticas
│       ├── services.py              # Lógica de compra
│       ├── urls.py
│       └── tests.py
│
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   ├── responses.py
│   └── exceptions.py
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

```


Esta arquitectura plantea una separación por módulos y usando el patrón MVT (Model View Template)

#### ARQUITECTURA POR CAPAS
1. Capa de Presentación (API)

- ViewSets (DRF): Manejo de peticiones HTTP
- Serializers: Validación y transformación de datos
- URLs/Routers: Definición de endpoints

2. Capa de Lógica de Negocio (Services)

- Validaciones complejas
- Cálculos (totales, stock, etc.)
- Orquestación de operaciones
- Transacciones

3. Capa de Acceso a Datos (Models)

- Modelos Django ORM
- Managers personalizados
- Métodos del modelo

4. Capa de Utilidades

- Validadores
- Helpers
- Excepciones personalizadas


### 2. Explicar cuándo usar clases vs funciones.

Aunque las 2 estructuras se usan para lo mismo, la cual es reutilizar código a partir de una estructura ya definida, las clases se usan para estructurar una entidad, mientras que las funciones se usan para realizar ciertas acciones.


### 3. Refactorizar código desordenado (se entregará ejemplo).

(no se entregó el código para esta sección)

### 4. Aplicar principios básicos de SOLID.

Con esta estructura del proyecto ya se están aplicando los principios SOLID porque el sistema está organizado por responsabilidades claras y desacopladas: los modelos, serializers, vistas y servicios están separados, lo que cumple el Principio de Responsabilidad Única (SRP) al evitar que una sola clase o archivo haga demasiadas cosas. 

La división por módulos (clientes, productos, ventas) permite extender funcionalidades sin modificar código existente, favoreciendo el Principio Abierto/Cerrado (OCP). El uso de herencia controlada (por ejemplo, modelos base en core) respeta el Principio de Sustitución de Liskov (LSP), ya que las clases hijas pueden usarse sin romper el comportamiento esperado. La separación de serializers, permisos y mixins evita depender de métodos innecesarios, alineándose con el Principio de Segregación de Interfaces (ISP). 

Finalmente, la presencia de una capa de servicios y utilidades reduce el acoplamiento directo entre vistas y modelos, sentando las bases para el Principio de Inversión de Dependencias (DIP), haciendo el sistema más mantenible y escalable.


## SECCIÓN 4 – PROYECTO PRÁCTICO (30%)

## (código realizado en la ubicación de este archivo)

#### 1. CRUD de productos y clientes.
#### 2. Registro de ventas.
#### 3. Persistencia de datos (SQLite o archivos).
#### 4. Separación por capas (servicios, modelos).
#### 5. Manejo de errores y validaciones.


## SECCIÓN 5 – CRITERIO PROFESIONAL (5%)
### 1. ¿Cómo manejas bugs en producción?

En producción priorizo impacto y urgencia. Primero identifico si el bug afecta datos, seguridad o disponibilidad; si es crítico, aplico mitigaciones inmediatas como rollback, feature flags o hotfixes. Luego analizo logs, métricas y trazas para encontrar la causa raíz, reproduzco el problema en un entorno controlado y aplico una solución definitiva acompañada de tests para evitar regresiones. Finalmente, documento el incidente y, si es necesario, ajusto procesos para prevenir fallos similares en el futuro.

### 2. ¿Cómo estimas tiempos de desarrollo?

Divido el trabajo en tareas pequeñas y estimables, evaluando complejidad técnica, dependencias y riesgos. Utilizo referencias de trabajos anteriores y agrego un margen para imprevistos. Prefiero estimaciones por rangos en lugar de fechas rígidas y las valido con el equipo. A medida que el proyecto avanza, reviso y ajusto las estimaciones basándome en el progreso real.


### 3. ¿Qué buenas prácticas aplicas siempre?

Aplico principios como SOLID, DRY y KISS, mantengo separación clara de responsabilidades y escribo código legible y testeable. Uso control de versiones con commits pequeños y descriptivos, revisiones de código, manejo adecuado de errores y validaciones. Además, priorizo la automatización (tests, linters, CI/CD) y documentación clara, especialmente en decisiones técnicas relevantes.

### 4. ¿Cómo aseguras escalabilidad?

Diseño el sistema pensando en el crecimiento desde el inicio: arquitectura modular, bajo acoplamiento y capas bien definidas. Evito cuellos de botella, uso caching, paginación y asincronía cuando es necesario, y me apoyo en métricas para tomar decisiones basadas en datos. La escalabilidad no es solo técnica, también implica que el código sea fácil de extender y que el equipo pueda trabajar en paralelo sin fricciones.


# CONSIDERACIONES PARA LA EJECUCIÓN DE LAS APLICACIONES

## BACKEND:

1. crear variables de entorno (archivo .env):

variables de ejemplo:

```
DEBUG=True (desarrollo o producción)
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

```

2. entorno de desarrollo:

Ejecutar (en el cmd de la raiz del proyecto):

- python -m venv venv
- venv\Scripts\activate

- pip install -r requirements.txt (instala las dependencias en el entorno virtual)


3. Ejecución de la aplicación (en el cmd de la raiz del proyecto):

- python manage.py makemigrations (crea migraciones a partir de los modelos)

- python manage.py migrate (aplica la migracion a la base de datos)

- python manage.py runserver (ejecuta el programa)


documentación: http://127.0.0.1:8000/api/docs (si esta en ejecución)



## FRONT END:

1. Ejecución 

- npm install
- npm run dev




LINK DE DESPLIEGUE DE SERVICIO WEB (DOCUMENTACION) A INTERNET: https://jsoluciones-back.onrender.com/api/docs
LINK DE DESPLIEGUE DE FRONT END A INTERNET: https://jsolucionesfront.vercel.app

(la base de datos esta integrada en el despliegue,por lo que en un redeploy se pueden borrar los datos)

EL PRIMER USUARIO CREADO EN api/auth/registro siempre sera admin, para demostración

puede usar para un administrador:

```
{
  "email": "adminJS@gmail.com",
  "username": "ForemannNI19",
  "password": "JSsoluciones4848",
  "password2": "JSsoluciones4848",
  "first_name": "Erick",
  "last_name": "Foremann",
  "documento": "38024803",
  "telefono": "38297566",
  "direccion": "example"
}

```

para un cliente

```
{
  "email": "clienteJS@gmail.com",
  "username": "Cliente1234",
  "password": "JSsoluciones2121",
  "password2": "JSsoluciones2121",
  "first_name": "Robert",
  "last_name": "Chase",
  "documento": "45458100",
  "telefono": "466188900",
  "direccion": "example"
}
```