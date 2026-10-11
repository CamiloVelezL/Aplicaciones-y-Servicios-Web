# Taller 2 — API IoT con FastAPI, MQTT y PostgreSQL

## 1. Información General

| Campo | Valor |
|-------|-------|
| **Nombre del proyecto** | API IoT AQ-003 |
| **Integrante** | Camilo Andrés Velez Luna |
| **Usuario GitHub** | [CamiloVelezL](https://github.com/CamiloVelezL) |
| **Asignatura** | Aplicaciones y Servicios Web |
| **Programa académico** | Tecnología en Desarrollo de Software |
| **Fecha** | 10 de octubre de 2026 |
| **Sensor asignado** | AQ-003 |
| **Tópico MQTT** | `iot/sensors/AQ-003/data` |
| **Broker MQTT** | `emqx.coriotlab.co:1883` |

---

## 2. Descripción del Sistema

### 2.1 Problema resuelto
Una infraestructura IoT dispone de sensores que publican mediciones periódicamente mediante MQTT. La aplicación desarrollada:

- Se conecta al broker MQTT.
- Se suscribe al tópico del sensor AQ-003.
- Recibe y decodifica mensajes JSON.
- Valida la estructura con Pydantic.
- Consulta la configuración del sensor mediante SQLAlchemy ORM.
- Valida sensor, magnitud, unidad y rango.
- Almacena únicamente mediciones válidas en PostgreSQL.
- Expone endpoints de consulta mediante FastAPI.

### 2.2 Arquitectura implementada

```
┌──────────┐   publica    ┌──────────────┐   entrega   ┌────────────────────┐
│  Sensor  │ ───────────▶ │ Broker MQTT  │ ──────────▶ │ App Python (FastAPI)│
│  AQ-003  │              │ emqx.cor...  │             │  + Consumidor MQTT  │
└──────────┘              └──────────────┘             └──────────┬─────────┘
                                                                  │
                                                        valida con Pydantic
                                                                  │
                                                       consulta ORM (SQLAlchemy)
                                                                  │
                                                                  ▼
                                                       ┌────────────────────┐
                                                       │    PostgreSQL      │
                                                       │      appdb         │
                                                       └────────────────────┘
                                                                  ▲
                                                                  │
                                                       ┌────────────────────┐
                                                       │  Cliente HTTP      │
                                                       │  (navegador, curl) │
                                                       └────────────────────┘
```

### 2.3 Magnitudes y unidades recibidas

| Magnitud | Unidad | Rango válido |
|----------|--------|--------------|
| `temperature` | °C | -10 a 60 |
| `humidity` | % | 0 a 100 |
| `tvoc` | ppb | 0 a 5000 |
| `eco2` | ppm | 400 a 5000 |

### 2.4 Payload real del sensor AQ-003

```json
{
  "sensor_id": "AQ-003",
  "timestamp": "2026-10-08T04:45:27Z",
  "measurements": {
    "temperature": {"value": 31.58, "unit": "C"},
    "humidity": {"value": 78.95, "unit": "%"},
    "tvoc": {"value": 285.03, "unit": "ppb"},
    "eco2": {"value": 1903.35, "unit": "ppm"}
  }
}
```

**Frecuencia**: cada ~5 segundos.
**Timestamp**: ISO 8601 en UTC (termina en `Z`).

---

## 3. Configuración del Entorno

### 3.1 Creación del entorno virtual

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/Scripts/activate  # Git Bash
```

### 3.2 Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 3.3 Variables de entorno requeridas

Crear un archivo `.env` en la raíz del proyecto (ver `.env.example` como plantilla):

```bash
# MQTT
MQTT_BROKER=emqx.coriotlab.co
MQTT_PORT=1883
MQTT_TOPIC=iot/sensors/AQ-003/data
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_KEEPALIVE=60

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=appdb
DB_USER=postgres
DB_PASSWORD=postgres123
```

**Nota**: `.env` NO se sube al repositorio (está en `.gitignore`).

---

## 4. Base de Datos

### 4.1 Conexión

- **Host**: localhost
- **Puerto**: 5432
- **Base**: appdb
- **Usuario**: postgres

Conexión implementada en `app/database/connection.py` con SQLAlchemy.

### 4.2 Tablas utilizadas

**`sensores`**

| Campo | Tipo | Restricción |
|-------|------|-------------|
| id | SERIAL | PK |
| codigo | VARCHAR(20) | UNIQUE, NOT NULL |
| nombre | VARCHAR(100) | NOT NULL |
| categoria | VARCHAR(30) | CHECK AIRE/GAS/AGUA/AMBIENTE |
| ubicacion | VARCHAR(100) | NOT NULL |
| activo | BOOLEAN | DEFAULT TRUE |
| fecha_registro | TIMESTAMPTZ | DEFAULT NOW() |

**`sensor_magnitudes`**

| Campo | Tipo | Restricción |
|-------|------|-------------|
| id | SERIAL | PK |
| sensor_id | INTEGER | FK → sensores(id) |
| magnitud | VARCHAR(50) | NOT NULL |
| unidad | VARCHAR(20) | NOT NULL |
| valor_minimo | NUMERIC(12,4) | NOT NULL |
| valor_maximo | NUMERIC(12,4) | NOT NULL |

**`mediciones`**

| Campo | Tipo | Restricción |
|-------|------|-------------|
| id | BIGSERIAL | PK |
| sensor_magnitud_id | INTEGER | FK → sensor_magnitudes(id) |
| valor | NUMERIC(12,4) | NOT NULL |
| timestamp_utc | TIMESTAMPTZ | NOT NULL |
| fecha_recepcion | TIMESTAMPTZ | DEFAULT NOW() |

### 4.3 Relaciones implementadas

```
sensores 1 ──── N sensor_magnitudes
sensor_magnitudes 1 ──── N mediciones
```

### 4.4 Correspondencia con `data-model.md`

Los modelos ORM en `app/models/` reflejan exactamente las tablas definidas en `data-model.md`.

---

## 5. Organización del Código

```
app/
├── main.py                    → App FastAPI + lifespan (startup/shutdown MQTT)
├── schemas/                   → Validación con Pydantic
│   ├── sensor.py              → SensorOut
│   ├── sensor_magnitud.py     → SensorMagnitudOut
│   └── medicion.py            → MedicionOut, MQTTMessage
├── models/                    → Modelos ORM (SQLAlchemy)
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── medicion.py
├── crud/                      → Operaciones de acceso a datos
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── medicion.py
├── api/                       → Endpoints HTTP
│   ├── sensor.py
│   ├── sensor_magnitud.py
│   └── medicion.py
├── mqtt/                      → Consumidor MQTT
│   └── client.py
└── database/                  → Conexión a PostgreSQL
    └── connection.py
```

**Responsabilidades**:
- `schemas/`: valida tipos y estructura.
- `models/`: representa tablas de la BD.
- `crud/`: encapsula las consultas SQL.
- `api/`: expone endpoints REST.
- `mqtt/`: recibe, valida y persiste mediciones.
- `database/`: gestiona la conexión y sesiones.

---

## 6. Endpoints Implementados

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Root (mensaje de bienvenida) |
| GET | `/docs` | Documentación Swagger UI |
| GET | `/sensores` | Lista todos los sensores |
| GET | `/sensores/por-codigo/{codigo}` | Sensor por código (ej: AQ-003) |
| GET | `/sensores/{id}` | Sensor por ID |
| GET | `/sensores/{id}/magnitudes` | Magnitudes del sensor |
| GET | `/sensor-magnitudes/{id}` | Sensor-magnitud por ID |
| GET | `/mediciones/{id}` | Medición por ID |
| GET | `/sensores/{id}/mediciones` | Histórico (filtros: `magnitud`, `desde`, `hasta`, `limit`) |
| GET | `/sensores/{id}/ultima-medicion` | Última medición registrada |

**Conversión de zonas horarias**: todos los timestamps se devuelven en hora local de Colombia (`America/Bogota`).

---

## 7. Evidencias de Funcionamiento

Las 18 pruebas obligatorias están documentadas en la carpeta [`evidencias/`](evidencias/):

| # | Prueba | Evidencia |
|---|--------|-----------|
| 1 | Recepción MQTT | [01_recepcion_mqtt.md](evidencias/01_recepcion_mqtt.md) |
| 2 | Medición válida | [02_medicion_valida.md](evidencias/02_medicion_valida.md) |
| 3 | Sensor inexistente | [03_sensor_inexistente.md](evidencias/03_sensor_inexistente.md) |
| 4 | Unidad incorrecta | [04_unidad_incorrecta.md](evidencias/04_unidad_incorrecta.md) |
| 5 | Tipo de dato incorrecto | [05_tipo_dato_incorrecto.md](evidencias/05_tipo_dato_incorrecto.md) |
| 6 | Magnitud incorrecta | [06_magnitud_incorrecta.md](evidencias/06_magnitud_incorrecta.md) |
| 7 | Timestamp inválido | [07_timestamp_invalido.md](evidencias/07_timestamp_invalido.md) |
| 8 | Consulta por ID existente | [08_consulta_id_existente.md](evidencias/08_consulta_id_existente.md) |
| 9 | Consulta por ID inexistente | [09_consulta_id_inexistente.md](evidencias/09_consulta_id_inexistente.md) |
| 10 | Consulta histórica | [10_consulta_historica.md](evidencias/10_consulta_historica.md) |
| 11 | Consulta por rango de fechas | [11_rango_fechas.md](evidencias/11_rango_fechas.md) |
| 12 | Rango desde > hasta | [12_desde_mayor_hasta.md](evidencias/12_desde_mayor_hasta.md) |
| 13 | Validación HTTP incorrecta | [13_validacion_http_422.md](evidencias/13_validacion_http_422.md) |
| 14 | Última medición | [14_ultima_medicion.md](evidencias/14_ultima_medicion.md) |
| 15 | Últimas N mediciones | [15_ultimas_n.md](evidencias/15_ultimas_n.md) |
| 16 | Filtro por magnitud | [16_filtro_magnitud.md](evidencias/16_filtro_magnitud.md) |
| 17 | Claves foráneas | [17_claves_foraneas.md](evidencias/17_claves_foraneas.md) |
| 18 | Separación de responsabilidades | [18_separacion_responsabilidades.md](evidencias/18_separacion_responsabilidades.md) |

**Datos recolectados**: más de **2900 mediciones** durante aproximadamente **60 minutos** continuos de recepción MQTT.

---

## 8. Control de Versiones

**Repositorio**: https://github.com/CamiloVelezL/Aplicaciones-y-Servicios-Web

**Branch**: `taller-2`

**Commits principales**:

| Commit | Descripción |
|--------|-------------|
| `feat(taller-2): setup inicial del proyecto IoT AQ-003` | Estructura base, data-model, mqtt_example, SQL scripts, requirements |
| `feat(taller-2): backend FastAPI con MQTT y persistencia` | Código completo del backend en `app/` |
| `docs(taller-2): evidencias de pruebas y README final` | Carpeta `evidencias/` + README |

**Aporte del integrante**:
- **Camilo Andrés Velez Luna** — 100% del desarrollo (proyecto individual).

---

## 9. Conclusiones

### Aprendizajes
- Integración de **FastAPI** con **SQLAlchemy ORM** y **PostgreSQL**.
- Consumo de mensajes **MQTT** con `paho-mqtt` en versión 2.x.
- Validación robusta de payloads con **Pydantic**.
- Manejo de **zonas horarias** UTC → Colombia con `zoneinfo`.
- Separación de responsabilidades en capas (`schemas`, `models`, `crud`, `api`, `mqtt`, `database`).

### Dificultades encontradas
- Instalación y configuración de `psql` en Windows.
- Problema con `tzdata` en Windows para `zoneinfo` (requirió `pip install tzdata`).
- Conflictos de intérprete entre VS Code y el `venv`.
- Manejo de mensajes inválidos publicados intencionalmente por el servicio MQTT.

### Soluciones aplicadas
- Uso de `pgAdmin` y `psql` para administrar la BD local.
- Instalación de `tzdata` como dependencia explícita en `requirements.txt`.
- Configuración de `.vscode/settings.json` con la ruta del `venv`.
- Validaciones en cascada: Pydantic (estructura) → ORM (existencia) → lógica de negocio (unidad, rango).

---

**Fin del informe.**