# Evidencia 12 — Rango desde > hasta

## Datos de entrada
GET `http://127.0.0.1:8000/sensores/1/mediciones?desde=2026-12-01T00:00:00&hasta=2026-10-01T00:00:00`

## Resultado obtenido

```json
{
  "detail": "'desde' no puede ser mayor que 'hasta'"
}
