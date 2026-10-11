# Evidencia 10 — Consulta histórica

## Datos de entrada
GET `http://127.0.0.1:8000/sensores/1/mediciones`

## Resultado obtenido
Lista completa de mediciones del sensor AQ-003, ordenadas por `timestamp_utc` descendente (las más recientes primero). Ejemplo parcial:

```json
[
  {
    "id": 540,
    "sensor_magnitud_id": 4,
    "valor": "537.5600",
    "timestamp_utc": "2026-10-07T23:57:52-05:00",
    "fecha_recepcion": "2026-10-07T23:57:52.324070-05:00"
  },
  {
    "id": 539,
    "sensor_magnitud_id": 3,
    "valor": "562.0200",
    "timestamp_utc": "2026-10-07T23:57:52-05:00",
    "fecha_recepcion": "2026-10-07T23:57:52.319833-05:00"
  }
]
