# Evidencia 11 — Consulta por rango de fechas

## Datos de entrada
GET `http://127.0.0.1:8000/sensores/1/mediciones?desde=2026-10-07T00:00:00&hasta=2026-10-08T23:59:59`

## Resultado obtenido
Solo se retornan las mediciones cuyo `timestamp_utc` cae dentro del rango especificado. Ejemplo parcial:

```json
[
  {
    "id": 540,
    "sensor_magnitud_id": 4,
    "valor": "537.5600",
    "timestamp_utc": "2026-10-07T23:57:52-05:00",
    "fecha_recepcion": "2026-10-07T23:57:52.324070-05:00"
  }
]
