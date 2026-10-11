# Evidencia 4 — Unidad incorrecta

## Datos de entrada
Payload MQTT con unidad incorrecta para temperature:

```json
{
  "sensor_id": "AQ-003",
  "timestamp": "2026-10-08T04:45:27Z",
  "measurements": {
    "temperature": {"value": 22.68, "unit": "INVALID_UNIT"}
  }
}
