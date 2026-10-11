# Evidencia 1 — Recepción MQTT

## Datos de entrada
Suscriptor MQTT al tópico iot/sensors/AQ-003/data.

## Resultado obtenido
Mensaje recibido del sensor AQ-003 cada ~5 segundos.

Log:
2026-10-07 23:45:24 [INFO] Conectado al broker emqx.coriotlab.co:1883
2026-10-07 23:45:24 [INFO] Suscrito al topico: iot/sensors/AQ-003/data
2026-10-07 23:45:27 [INFO] Mensaje recibido: {'sensor_id': 'AQ-003', ...}

## Código HTTP
N/A (proceso MQTT).

## Registro almacenado o rechazado
Almacenado.

## Archivo y función
- app/mqtt/client.py :: on_connect(), on_message(), _validar_y_guardar()

## Explicación
El cliente MQTT se conecta al broker y se suscribe al tópico. Al recibir un mensaje, lo decodifica y lo pasa al validador.
