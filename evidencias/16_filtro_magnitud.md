# Evidencia 16 — Filtro por magnitud

## Datos de entrada
GET `http://127.0.0.1:8000/sensores/1/mediciones?magnitud=temperature`

## Resultado obtenido
Solo las mediciones de la magnitud `temperature` del sensor AQ-003. Ejemplo parcial:

```json
[
  {
    "id": 537,
    "sensor_magnitud_id": 1,
    "valor": "19.5100",
    "timestamp_utc": "2026-10-07T23:57:52-05:00",
    "fecha_recepcion": "2026-10-07T23:57:52.302684-05:00"
  },
  {
    "id": 533,
    "sensor_magnitud_id": 1,
    "valor": "28.7300",
    "timestamp_utc": "2026-10-07T23:57:47-05:00",
    "fecha_recepcion": "2026-10-07T23:57:47.305112-05:00"
  }
]
