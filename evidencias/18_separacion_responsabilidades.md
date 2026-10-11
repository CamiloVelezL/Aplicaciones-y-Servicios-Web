# Evidencia 18 — Separación de responsabilidades

## Datos de entrada
Comando en PowerShell (desde la raíz del repo):

```
tree app /F
```

## Resultado obtenido

```
app/
├── main.py
├── __init__.py
├── api/
│   ├── medicion.py
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── __init__.py
├── crud/
│   ├── medicion.py
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── __init__.py
├── database/
│   ├── connection.py
│   └── __init__.py
├── models/
│   ├── medicion.py
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── __init__.py
├── mqtt/
│   ├── client.py
│   └── __init__.py
└── schemas/
    ├── medicion.py
    ├── sensor.py
    ├── sensor_magnitud.py
    └── __init__.py
```

## Código HTTP
N/A.

## Registro almacenado o rechazado
N/A.

## Archivo y función
Organización general del proyecto.

## Explicación
El código está separado en **capas con responsabilidades únicas**:

| Carpeta | Responsabilidad |
|---------|-----------------|
| `app/database/` | Conexión a PostgreSQL con SQLAlchemy (`engine`, `SessionLocal`, `get_db`). |
| `app/models/` | Modelos ORM que representan las tablas (`Sensor`, `SensorMagnitud`, `Medicion`). |
| `app/schemas/` | Schemas Pydantic para validación de entrada/salida (`SensorOut`, `MQTTMessage`, etc.). |
| `app/crud/` | Funciones de acceso a datos (consultas e inserciones). |
| `app/mqtt/` | Consumidor MQTT con validaciones de negocio y persistencia. |
| `app/api/` | Endpoints FastAPI que exponen las operaciones. |
| `app/main.py` | Punto de entrada: crea la app, registra routers y arranca el cliente MQTT. |

Esta separación permite que cada módulo sea independiente, testeable y mantenible. Por ejemplo, la capa `crud/` no sabe nada de HTTP; la capa `api/` no sabe nada de SQL; y el consumidor MQTT solo orquesta validaciones y llamadas al CRUD.