# Evidencia 15 — Últimas N mediciones

## Datos de entrada
GET `http://127.0.0.1:8000/sensores/1/mediciones?limit=5`

## Resultado obtenido
Lista con las **5 mediciones más recientes** del sensor AQ-003:

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
  },
  {
    "id": 538,
    "sensor_magnitud_id": 2,
    "valor": "45.1900",
    "timestamp_utc": "2026-10-07T23:57:52-05:00",
    "fecha_recepcion": "2026-10-07T23:57:52.315521-05:00"
  },
  {
    "id": 537,
    "sensor_magnitud_id": 1,
    "valor": "19.5100",
    "timestamp_utc": "2026-10-07T23:57:52-05:00",
    "fecha_recepcion": "2026-10-07T23:57:52.302684-05:00"
  },
  {
    "id": 536,
    "sensor_magnitud_id": 4,
    "valor": "1709.4400",
    "timestamp_utc": "2026-10-07T23:57:47-05:00",
    "fecha_recepcion": "2026-10-07T23:57:47.325114-05:00"
  }
]
