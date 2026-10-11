# Evidencia 3 — Sensor inexistente

## Datos de entrada
Payload con sensor_id = NOEXISTE-999.

## Resultado obtenido
Rechazado. Log:
Rechazado: sensor inexistente NOEXISTE-999

## Código HTTP
N/A.

## Registro almacenado o rechazado
Rechazado.

## Archivo y función
- app/mqtt/client.py :: _validar_y_guardar()
- app/crud/sensor.py :: get_by_codigo()

## Explicación
Se busca el sensor en la BD; si no existe, el mensaje se descarta sin guardar.
