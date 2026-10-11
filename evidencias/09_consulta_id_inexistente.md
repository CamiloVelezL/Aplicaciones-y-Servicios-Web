# Evidencia 9 — Consulta por ID inexistente

## Datos de entrada
GET `http://127.0.0.1:8000/sensores/99999`

## Resultado obtenido

```json
{
  "detail": "Sensor no encontrado"
}
