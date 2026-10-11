# Evidencia 13 — Validación HTTP incorrecta

## Datos de entrada
GET `http://127.0.0.1:8000/mediciones/abc`

## Resultado obtenido

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "medicion_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "abc"
    }
  ]
}
