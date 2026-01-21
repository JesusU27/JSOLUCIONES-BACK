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

en base a la base de datos del proyecto:

```

┌─────────────────┐
│   CLIENTE/USER  │ (Usuario que compra)
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ password        │
│ first_name      │
│ last_name       │
│ documento       │
│ telefono        │
│ direccion       │
│ is_active       │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N (comprador)
         │
         ▼
┌─────────────────┐
│   PRODUCTOS     │
├─────────────────┤
│ id (PK)         │
│ codigo          │
│ nombre          │
│ descripcion     │
│ precio          │
│ stock           │
│ categoria       │
│ activo          │
│ imagen_url      │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │
         │              ┌─────────────────┐
         │              │    VENTAS       │
         │              ├─────────────────┤
         │              │ id (PK)         │
         │         ┌────│ cliente_id (FK) │
         │         │    │ fecha_venta     │
         │         │    │ total           │
         │         │    │ estado          │
         │         │    │ observaciones   │
         │         │    │ created_at      │
         │         │    │ updated_at      │
         │         │    └────────┬────────┘
         │         │             │
         └─────────┼─────────────┘
                   │             │ 1:N
                   │             │
                   │     ┌───────▼───────────┐
                   └─────► DETALLE_VENTA     │
                    N:1  ├───────────────────┤
                         │ id (PK)           │
                         │ venta_id (FK)     │
                         │ producto_id (FK)  │
                         │ cantidad          │
                         │ precio_unitario   │
                         │ subtotal          │
                         │ created_at        │
                         └───────────────────┘

```

📊 QUERIES SQL Y DJANGO ORM

1️. Calcular Ingresos TotalesSQL (MySQL):
sql-- Ingresos totales de todas las ventas completadas

```
SELECT 
    SUM(total) as ingresos_totales,
    COUNT(*) as total_ventas
FROM ventas
WHERE estado = 'COMPLETADA';
```
-- Ingresos totales por cliente específico

```
SELECT 
    c.id,
    c.first_name,
    c.last_name,
    c.email,
    SUM(v.total) as total_gastado,
    COUNT(v.id) as numero_compras
FROM clientes c
LEFT JOIN ventas v ON c.id = v.cliente_id
WHERE v.estado = 'COMPLETADA'
GROUP BY c.id, c.first_name, c.last_name, c.email;
```
-- Ingresos totales del sistema (todas las ventas completadas)
```
SELECT 
    SUM(v.total) as ingresos_totales,
    COUNT(v.id) as total_ventas,
    AVG(v.total) as promedio_venta,
    MIN(v.total) as venta_minima,
    MAX(v.total) as venta_maxima
FROM ventas v
WHERE v.estado = 'COMPLETADA';Django ORM:
pythonfrom django.db.models import Sum, Count, Avg, Min, Max
from apps.ventas.models import Venta

```

Ingresos totales del sistema:

```
ingresos = Venta.objects.filter(estado='COMPLETADA').aggregate(
    ingresos_totales=Sum('total'),
    total_ventas=Count('id'),
    promedio_venta=Avg('total'),
    venta_minima=Min('total'),
    venta_maxima=Max('total')
)

# Resultado: 
# {
#     'ingresos_totales': Decimal('15000.00'),
#     'total_ventas': 50,
#     'promedio_venta': Decimal('300.00'),
#     ...
# }
```


Ingresos totales de un cliente específico:

```
from apps.clientes.models import Cliente

cliente = Cliente.objects.get(id=1)
ingresos_cliente = cliente.compras.filter(estado='COMPLETADA').aggregate(
    total_gastado=Sum('total'),
    numero_compras=Count('id')
)
```

2️. Filtrar Transacciones por Rango de FechasSQL (MySQL):
sql-- Ventas entre dos fechas específicas

```
SELECT 
    v.id,
    v.fecha_venta,
    v.total,
    v.estado,
    c.first_name,
    c.last_name,
    c.email
FROM ventas v
INNER JOIN clientes c ON v.cliente_id = c.id
WHERE v.fecha_venta BETWEEN '2025-01-01' AND '2025-01-31'
    AND v.estado = 'COMPLETADA'
ORDER BY v.fecha_venta DESC;
```
-- Ventas con detalles en un rango de fechas

```
SELECT 
    v.id as venta_id,
    v.fecha_venta,
    v.total as total_venta,
    c.first_name,
    c.last_name,
    p.nombre as producto,
    dv.cantidad,
    dv.precio_unitario,
    dv.subtotal
FROM ventas v
INNER JOIN clientes c ON v.cliente_id = c.id
INNER JOIN detalle_ventas dv ON v.id = dv.venta_id
INNER JOIN productos p ON dv.producto_id = p.id
WHERE v.fecha_venta BETWEEN '2025-01-01 00:00:00' AND '2025-01-31 23:59:59'
ORDER BY v.fecha_venta DESC, v.id, dv.id;
```
-- Resumen de ventas por mes
```
SELECT 
    YEAR(fecha_venta) as anio,
    MONTH(fecha_venta) as mes,
    COUNT(*) as total_ventas,
    SUM(total) as ingresos_mes
FROM ventas
WHERE estado = 'COMPLETADA'
    AND fecha_venta BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY YEAR(fecha_venta), MONTH(fecha_venta)
ORDER BY anio DESC, mes DESC;
```

Django ORM:

```
pythonfrom datetime import datetime
from django.db.models import Q
from apps.ventas.models import Venta

# Filtrar ventas por rango de fechas
fecha_inicio = datetime(2025, 1, 1)
fecha_fin = datetime(2025, 1, 31, 23, 59, 59)

ventas = Venta.objects.filter(
    fecha_venta__range=[fecha_inicio, fecha_fin],
    estado='COMPLETADA'
).select_related('cliente').order_by('-fecha_venta')

# Ventas con prefetch de detalles
ventas_con_detalles = Venta.objects.filter(
    fecha_venta__range=[fecha_inicio, fecha_fin]
).select_related('cliente').prefetch_related(
    'detalles__producto'
).order_by('-fecha_venta')

# Resumen por fecha
from django.db.models.functions import TruncMonth

resumen_mensual = Venta.objects.filter(
    estado='COMPLETADA',
    fecha_venta__year=2025
).annotate(
    mes=TruncMonth('fecha_venta')
).values('mes').annotate(
    total_ventas=Count('id'),
    ingresos_mes=Sum('total')
).order_by('-mes')

# Filtrar ventas de un cliente en un rango de fechas
ventas_cliente = Venta.objects.filter(
    cliente_id=1,
    fecha_venta__gte=fecha_inicio,
    fecha_venta__lte=fecha_fin
)
```

3️. Obtener Cliente con Mayor ConsumoSQL (MySQL):
sql-- Cliente con mayor consumo (TOP 1)

```
SELECT 
    c.id,
    c.documento,
    c.first_name,
    c.last_name,
    c.email,
    COUNT(v.id) as total_compras,
    SUM(v.total) as total_gastado
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
WHERE v.estado = 'COMPLETADA'
GROUP BY c.id, c.documento, c.first_name, c.last_name, c.email
ORDER BY total_gastado DESC
LIMIT 1;
```

-- Top 10 clientes con mayor consumo

```
SELECT 
    c.id,
    CONCAT(c.first_name, ' ', c.last_name) as nombre_completo,
    c.email,
    c.documento,
    COUNT(v.id) as total_compras,
    SUM(v.total) as total_gastado,
    AVG(v.total) as promedio_compra,
    MAX(v.fecha_venta) as ultima_compra
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
WHERE v.estado = 'COMPLETADA'
GROUP BY c.id, c.first_name, c.last_name, c.email, c.documento
ORDER BY total_gastado DESC
LIMIT 10;
```

-- Clientes con más de X compras

```
SELECT 
    c.id,
    CONCAT(c.first_name, ' ', c.last_name) as nombre_completo,
    COUNT(v.id) as total_compras,
    SUM(v.total) as total_gastado
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
WHERE v.estado = 'COMPLETADA'
GROUP BY c.id, c.first_name, c.last_name
HAVING COUNT(v.id) >= 5
ORDER BY total_gastado DESC;Django ORM:
pythonfrom django.db.models import Sum, Count, Avg, Max
from apps.clientes.models import Cliente
```

 Cliente con mayor consumo (TOP 1):

```
cliente_top = Cliente.objects.filter(
    compras__estado='COMPLETADA'
).annotate(
    total_compras=Count('compras'),
    total_gastado=Sum('compras__total'),
    promedio_compra=Avg('compras__total'),
    ultima_compra=Max('compras__fecha_venta')
).order_by('-total_gastado').first()
```

Top 10 clientes:

```
top_clientes = Cliente.objects.filter(
    compras__estado='COMPLETADA'
).annotate(
    total_compras=Count('compras'),
    total_gastado=Sum('compras__total'),
    promedio_compra=Avg('compras__total')
).order_by('-total_gastado')[:10]
```

Clientes con más de 5 compras:

```
clientes_frecuentes = Cliente.objects.filter(
    compras__estado='COMPLETADA'
).annotate(
    total_compras=Count('compras'),
    total_gastado=Sum('compras__total')
).filter(
    total_compras__gte=5
).order_by('-total_gastado')

```

Producto más vendido:

```
from apps.productos.models import Producto

producto_top = Producto.objects.filter(
    detalleventa__venta__estado='COMPLETADA'
).annotate(
    veces_vendido=Count('detalleventa'),
    unidades_vendidas=Sum('detalleventa__cantidad'),
    ingresos_generados=Sum('detalleventa__subtotal')
).order_by('-unidades_vendidas').first()4️⃣ Manejo de Errores de Datos InválidosSQL (MySQL) - Validaciones:
sql-- Verificar ventas con total = 0 o negativo (datos inválidos)
SELECT 
    v.id,
    v.total,
    v.fecha_venta,
    c.email
FROM ventas v
INNER JOIN clientes c ON v.cliente_id = c.id
WHERE v.total <= 0;

-- Verificar detalles de venta con cantidades inválidas
SELECT 
    dv.id,
    dv.venta_id,
    dv.cantidad,
    dv.precio_unitario,
    dv.subtotal,
    (dv.cantidad * dv.precio_unitario) as subtotal_calculado
FROM detalle_ventas dv
WHERE dv.cantidad <= 0 
    OR dv.precio_unitario <= 0
    OR dv.subtotal != (dv.cantidad * dv.precio_unitario);

-- Verificar ventas sin detalles (huérfanas)
SELECT v.*
FROM ventas v
LEFT JOIN detalle_ventas dv ON v.id = dv.venta_id
WHERE dv.id IS NULL;

-- Verificar productos con stock negativo
SELECT 
    p.id,
    p.codigo,
    p.nombre,
    p.stock
FROM productos p
WHERE p.stock < 0;

-- Verificar clientes inactivos con ventas pendientes
SELECT 
    c.id,
    c.email,
    c.is_active,
    COUNT(v.id) as ventas_pendientes
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
WHERE c.is_active = 0
    AND v.estado = 'PENDIENTE'
GROUP BY c.id, c.email, c.is_active;

```
Django ORM - Validaciones:

```
pythonfrom django.db.models import F, Q, Count
from django.core.exceptions import ValidationError
from apps.ventas.models import Venta, DetalleVenta
from apps.productos.models import Producto
from apps.clientes.models import Cliente

# 1. Verificar ventas con total inválido
ventas_invalidas = Venta.objects.filter(total__lte=0)

# 2. Verificar detalles con cálculos incorrectos
detalles_invalidos = DetalleVenta.objects.exclude(
    subtotal=F('cantidad') * F('precio_unitario')
)

# 3. Verificar ventas sin detalles
ventas_sin_detalles = Venta.objects.annotate(
    num_detalles=Count('detalles')
).filter(num_detalles=0)

# 4. Verificar productos con stock negativo
productos_stock_negativo = Producto.objects.filter(stock__lt=0)

# 5. Verificar clientes inactivos con ventas
clientes_inactivos_con_ventas = Cliente.objects.filter(
    is_active=False,
    compras__estado='PENDIENTE'
).distinct()

```

# Función de validación completa

```
def validar_datos_sistema():
    """
    Valida la integridad de los datos del sistema.
    Retorna un diccionario con los errores encontrados.
    """
    errores = {}
    
    # Validar ventas
    ventas_invalidas = Venta.objects.filter(total__lte=0).count()
    if ventas_invalidas > 0:
        errores['ventas_total_invalido'] = ventas_invalidas
    
    # Validar detalles
    detalles_invalidos = DetalleVenta.objects.exclude(
        subtotal=F('cantidad') * F('precio_unitario')
    ).count()
    if detalles_invalidos > 0:
        errores['detalles_calculo_incorrecto'] = detalles_invalidos
    
    # Validar productos
    productos_invalidos = Producto.objects.filter(stock__lt=0).count()
    if productos_invalidos > 0:
        errores['productos_stock_negativo'] = productos_invalidos
    
    # Validar ventas huérfanas
    ventas_huerfanas = Venta.objects.annotate(
        num_detalles=Count('detalles')
    ).filter(num_detalles=0).count()
    if ventas_huerfanas > 0:
        errores['ventas_sin_detalles'] = ventas_huerfanas
    
    return errores

# Uso:
errores = validar_datos_sistema()
if errores:
    print("Se encontraron errores:", errores)
else:
    print("Datos válidos")

```


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

Las clases son plantillas para crear objetos que agrupan datos (atributos) y comportamientos (métodos), modelando entidades complejas, mientras que las funciones son bloques de código independientes que realizan tareas específicas y reutilizables, sin estar atadas a una clase, aunque dentro de una clase una función se convierte en un método. La clave es que las clases definen la estructura (el "qué" es algo), y las funciones/métodos son las acciones (el "qué hace"). 


### 3. Refactorizar código desordenado (se entregará ejemplo).

(no se entregó el código para esta sección)

### 4. Aplicar principios básicos de SOLID.

Con esta estructura del proyecto ya se están aplicando los principios SOLID porque el sistema está organizado por responsabilidades claras y desacopladas: los modelos, serializers, vistas y servicios están separados, lo que cumple el Principio de Responsabilidad Única (SRP) al evitar que una sola clase o archivo haga demasiadas cosas. 

La división por módulos (clientes, productos, ventas) permite extender funcionalidades sin modificar código existente, favoreciendo el Principio Abierto/Cerrado (OCP). El uso de herencia controlada (por ejemplo, modelos base en core) respeta el Principio de Sustitución de Liskov (LSP), ya que las clases hijas pueden usarse sin romper el comportamiento esperado. La separación de serializers, permisos y mixins evita depender de métodos innecesarios, alineándose con el Principio de Segregación de Interfaces (ISP). 

Finalmente, la presencia de una capa de servicios y utilidades reduce el acoplamiento directo entre vistas y modelos, sentando las bases para el Principio de Inversión de Dependencias (DIP), haciendo el sistema más mantenible y escalable.


## SECCIÓN 4 – PROYECTO PRÁCTICO (30%)

## (código realizado en la ubicación de este archivo)

#### 1. CRUD de productos y clientes. [hecho]
#### 2. Registro de ventas. [hecho]
#### 3. Persistencia de datos (SQLite o archivos). [hecho]
#### 4. Separación por capas (servicios, modelos). [hecho]
#### 5. Manejo de errores y validaciones. [hecho]


## SECCIÓN 5 – CRITERIO PROFESIONAL (5%)
### 1. ¿Cómo manejas bugs en producción?

En producción priorizo impacto y urgencia. Primero identifico si el bug afecta datos, seguridad o disponibilidad; si es crítico, aplico mitigaciones inmediatas como rollback, feature flags o hotfixes. Luego analizo logs, métricas y trazas para encontrar la causa raíz, reproduzco el problema en un entorno controlado y aplico una solución definitiva acompañada de tests para evitar regresiones. Finalmente, documento el incidente y, si es necesario, ajusto procesos para prevenir fallos similares en el futuro.

### 2. ¿Cómo estimas tiempos de desarrollo?

Divido el trabajo en tareas pequeñas y estimables, evaluando complejidad técnica, dependencias y riesgos. Utilizo referencias de trabajos anteriores y agrego un margen para imprevistos. Prefiero estimaciones por rangos en lugar de fechas rígidas y las valido con el equipo. A medida que el proyecto avanza, reviso y ajusto las estimaciones basándome en el progreso real.


### 3. ¿Qué buenas prácticas aplicas siempre?

Aplico principios como SOLID, DRY y KISS, mantengo separación clara de responsabilidades y escribo código legible y testeable. Uso control de versiones con commits pequeños y descriptivos, revisiones de código, manejo adecuado de errores y validaciones. Además, priorizo la automatización (tests, linters, CI/CD) y documentación clara, especialmente en decisiones técnicas relevantes.

### 4. ¿Cómo aseguras escalabilidad?

Diseño el sistema pensando en el crecimiento desde el inicio: arquitectura modular, bajo acoplamiento y capas bien definidas. Evito cuellos de botella, uso caching, paginación y asincronía cuando es necesario, y me apoyo en métricas para tomar decisiones basadas en datos. La escalabilidad no es solo técnica, también implica que el código sea fácil de extender y que el equipo pueda trabajar en paralelo sin fricciones.


# CONSIDERACIONES PARA LA EJECUCIÓN DE LAS APLICACIONES EN MODO LOCAL

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

1. Variables de entorno:

crea un .env en el root del proyecto y usa

```
VITE_API_BASE_URL=http://127.0.0.1:8000/api/
```

2. Ejecución 

- npm install
- npm run dev


# CASO CONTRARIO SI SE QUIERE PROBAR EN INTERNET


LINK DE DESPLIEGUE DE SERVICIO WEB (DOCUMENTACION) A INTERNET: https://jsoluciones-back.onrender.com/api/docs
LINK DE DESPLIEGUE DE FRONT END A INTERNET: https://jsolucionesfront.vercel.app

la base de datos esta integrada en el despliegue (sqlite),por lo que en un redeploy se pueden borrar los datos. Por ello es mejor verificar en el front end si el login funciona con cualquiera de estos datos:

ADMIN: adminJS@gmail.com | JSsoluciones4848
USER (cliente): clienteJS@gmail.com | JSsoluciones2121

si no hay cuentas, quiere decir que los datos se han borrado debido a un re-despliegue, entonces procederemos a crear los datos desde la documentación del despliegue del backend.

Caso contrario si deje iniciar sesión, podemos usar normalmente el front end.

A continuación se detallaran los pasos para hacer solo las cuentas, posteriormente a esto, podemos regresar al login del front end y utilizarlo normalmente.


(usar el link de despliegue para crear los datos)
https://jsoluciones-back.onrender.com/api/docs

y dirigirse al apartado api/auth/registro, el primer usuario creado siempre sera admin, para demostración
puede usar para este dato:

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

luego genere los datos del usuario para un cliente:

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

Como mencioné anteriormente, si el front end ya valida estos datos quiere decir que la base de datos no ha sido reiniciada y se puede utilizar de manera normal.