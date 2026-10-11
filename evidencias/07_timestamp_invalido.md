# Evidencia 7 — Timestamp inválido

## Datos de entrada
Payload MQTT con timestamp que no es una fecha válida:

```json
{
  "sensor_id": "AQ-003",
  "timestamp": "no-fecha",
  "measurements": {
    "temperature": {"value": 25.0, "unit": "C"}
  }
}
