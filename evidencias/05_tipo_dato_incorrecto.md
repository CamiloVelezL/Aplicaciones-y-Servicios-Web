# Evidencia 5 — Tipo de dato incorrecto

## Datos de entrada
Payload MQTT con `value` como string en vez de número:

```json
{
  "sensor_id": "AQ-003",
  "timestamp": "2026-10-08T04:45:27Z",
  "measurements": {
    "temperature": {"value": "abc", "unit": "C"}
  }
}
