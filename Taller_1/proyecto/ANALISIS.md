# Análisis final — Taller 1

## 1. Diferencias entre los contratos de los proveedores

Los dos proveedores representan la misma información meteorológica pero con estructuras totalmente distintas.

Proveedor A (`proveedor_a.json`) entrega los datos como un objeto JSON con anidamiento:

- `station.city_name` y `station.country_code` para ciudad y país.
- `location.lat` y `location.lon` para coordenadas.
- `measurements.temperature_f`, `measurements.relative_humidity` y `measurements.wind_speed_ms` para las mediciones.
- `observed_at` en formato ISO 8601 con offset.
- `provider_record_id` como identificador.

Proveedor B (`proveedor_b.csv`) entrega los datos como CSV plano con delimitador `;`:

- `municipality` y `country` para ciudad y país.
- `latitude_deg` y `longitude_deg` para coordenadas.
- `temp_celsius`, `humidity_pct` y `wind_kmh` para las mediciones.
- `measurement_time` en formato `DD/MM/YYYY HH:MM` sin zona horaria.
- `record_code` como identificador.

El contrato institucional (`CONTRATO_API.md`) exige nombres planos en inglés-español mezclados:

- `ciudad`, `pais`, `latitud`, `longitud`, `temperatura_c`, `humedad`, `viento_kmh`, `fecha_hora`, `origen`.

Ningún proveedor se parece al contrato institucional, así que ambos requieren transformación completa.

## 2. Transformaciones necesarias

- **Temperatura:** Proveedor A entrega grados Fahrenheit. Se convierte con `(F - 32) * 5 / 9`. Proveedor B ya entrega Celsius.
- **Viento:** Proveedor A entrega m/s. Se convierte a km/h con `* 3.6`. Proveedor B ya entrega km/h.
- **Humedad:** ambos entregan porcentaje. Se usa directo.
- **Fechas:** Proveedor A ya usa ISO 8601 con offset, se normaliza con `datetime.fromisoformat`. Proveedor B usa `DD/MM/YYYY HH:MM` sin zona horaria, se parsea con `datetime.strptime(..., "%d/%m/%Y %H:%M")` y se le asigna `-05:00` porque Colombia es UTC-5.
- **Renombrado de campos:** `station.city_name` → `ciudad`, `municipality` → `ciudad`, `temp_celsius` → `temperatura_c`, etc.
- **`origen`:** se asigna `proveedor_a` o `proveedor_b` según la fuente.

## 3. Tipos de errores encontrados antes de enviar

### Errores de normalización (9)

Datos que no se pueden convertir al tipo o formato del contrato:

| ID interno | Motivo                            |
|            |                                   |
| A-0040     | falta `observed_at`               |
| A-0082     | `temperature_f` es `"N/A"`        |
| A-0150     | falta `country_code`              |
| A-0173     | `temperature_f` es `null`         |
| A-0174     | fecha inválida `09-XX-2026 25:61` |
| B-0076     | `measurement_time` vacío          |
| B-0114     | `temp_celsius` es `"error"`       |
| B-0146     | `temp_celsius` vacío              |
| B-0171     | fecha inválida `31/13/2026 28:75` |

### Rechazos locales (11)

Registros que se normalizaron bien pero incumplen reglas del contrato:

| ID interno | Motivo           |
|            |                  |
| A-0015     | humedad 108.4    |
| A-0031     | latitud 95.245   |
| A-0088     | viento -2.4      |
| A-0136     | ciudad vacía     |
| A-0175     | longitud -190.75 |
| B-0004     | humedad 117.5    |
| B-0006     | latitud -94.22   |
| B-0115     | viento -7.40     |
| B-0128     | municipio vacío  |
| B-0135     | país vacío       |
| B-0190     | longitud 188.45  |

## 4. Diferencias entre validación local y validación del servidor

La validación local aplica las reglas escritas en `CONTRATO_API.md` antes de enviar: ciudad no vacía, país no vacío, latitud entre -90 y 90, 
longitud entre -180 y 180, humedad entre 0 y 100, viento mayor o igual a 0, fecha válida con zona horaria, origen permitido.

El servidor valida de forma independiente y con reglas que el contrato no explicita del todo. En la práctica encontramos:

- El servidor rechaza con `409` cuando la medición ya existe. Nos pasó con todos los registros de Proveedor A en la segunda ejecución: 
  se habían guardado en la primera corrida.
- El servidor rechaza con `422` cuando la fecha no incluye zona horaria. Al inicio, Proveedor B enviaba `2026-09-01T06:00:00` y el servidor lo rechazaba. 
  La validación local no detectaba eso hasta que la ajustamos.
- El servidor devuelve `201` cuando acepta.

Conclusión: la validación local reduce los errores enviados, pero no reemplaza al servidor. Hay reglas que solo se descubren al leer las respuestas.

## 5. Decisión de implementación más importante

Separar **error de normalización** de **rechazo local**.

Se exige que los errores de normalización no vayan a `salida/normalizadas.json`, mientras que los rechazados localmente sí deben permanecer ahí.
 Mantener esa separación:

- Garantiza que `normalizadas.json` contenga exactamente lo que pudo representarse con el contrato institucional.
- Permite distinguir entre problemas de conversión y problemas de reglas de negocio.
- Deja trazabilidad completa en `salida/reporte.json` para auditar cada registro y su resultado.

Otra decisión clave fue **no reintentar respuestas 4xx**. Se exige y además evita sobrecargar al servidor con envíos que ya sabemos que fallarán.

## 6. Evidencia de ejecución real

Comando: `python integrador.py`

### Resumen del reporte

| Métrica                     | Valor                                       |
|                             |                                             |
| Procesados                  | 400                                         |
| Normalizados                | 391                                         |
| Errores de normalización    | 9                                           |
| Válidos localmente          | 380                                         |
| Rechazados localmente       | 11                                          |
| Enviados                    | 380                                         |
| Aceptados por la API        | 0 en la última corrida; 190 en la primera   |
| Rechazados por la API       | 380 en la última corrida; 190 en la primera |
| Errores de comunicación     | 0                                           |

En la primera ejecución del programa se registraron 190 mediciones correctamente (código 201). 
En ejecuciones posteriores la API rechazó con código 409 ("La medición ya existe") los registros que ya estaban almacenados, 
por lo que en la última corrida `aceptados_api` aparece como 0 y `rechazados_api` como 380. Este comportamiento es esperado:
el cliente interpreta correctamente la respuesta del servidor y no reintenta las respuestas 4xx.


### Ejemplo de error de normalización

```json
{
  "id_interno": "A-0040",
  "error_normalizacion": "'observed_at'"
}

### Ejemplo de rechazo local

{
  "id_interno": "A-0015",
  "contrato": {
    "ciudad": "Barranquilla",
    "pais": "CO",
    "latitud": 10.969955,
    "longitud": -74.762201,
    "temperatura_c": 28.666666666666668,
    "humedad": 108.4,
    "viento_kmh": 10.008,
    "fecha_hora": "2026-09-01T07:00:00-05:00",
    "origen": "proveedor_a"
  },
  "errores_validacion": ["humedad fuera de rango"]
}

### Ejemplo de respuesta de la API

{
  "estado": "rechazado_api",
  "status": 409,
  "respuesta": {
    "detail": "La medición ya existe"
  },
  "id_interno": "A-0001"
}

### Resultado de la consulta final mediante GET

status: 200
equipo: EQUIPO-01-APPSWEB
total: 380

### Primeras dos mediciones registradas:

[
  {
    "id": 5143,
    "ciudad": "Medellin",
    "pais": "CO",
    "latitud": 6.242282,
    "longitud": -75.595933,
    "temperatura_c": 18.944444444444443,
    "humedad": 81.3,
    "viento_kmh": 30.492000000000004,
    "fecha_hora": "2026-09-01T00:00:00-05:00",
    "origen": "proveedor_a",
    "fecha_recepcion": "2026-09-14T01:51:32.183300+00:00"
  },
  {
    "id": 5144,
    "ciudad": "Medellin",
    "pais": "CO",
    "latitud": 6.24089,
    "longitud": -75.602515,
    "temperatura_c": 21.333333333333336,
    "humedad": 84.8,
    "viento_kmh": 18.36,
    "fecha_hora": "2026-09-01T00:30:00-05:00",
    "origen": "proveedor_a",
    "fecha_recepcion": "2026-09-14T01:51:33.441769+00:00"
  }
]

### Pruebas automatizadas

6 passed in 0.39s
