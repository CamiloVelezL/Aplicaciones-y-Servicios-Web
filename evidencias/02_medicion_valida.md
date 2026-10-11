# Evidencia 2 — Medición válida

## Datos de entrada
Payload MQTT con todas las magnitudes válidas del sensor AQ-003.

## Resultado obtenido
Se guardan 4 mediciones en PostgreSQL con el mismo timestamp.

Log:
2026-10-07 23:45:27 [INFO] OK: guardadas 4 mediciones del sensor AQ-003 @ 2026-10-08T04:45:27+00:00

Consulta SQL:
SELECT id, sensor_magnitud_id, valor, timestamp_utc FROM mediciones ORDER BY id DESC LIMIT 4;

## Código HTTP
N/A.

## Registro almacenado o rechazado
Almacenado: 4 registros.

## Archivo y función
- app/mqtt/client.py :: _validar_y_guardar()
- app/crud/medicion.py :: create()

## Explicación
Cada mensaje válido genera 4 registros, uno por magnitud, compartiendo el timestamp_utc del payload.
