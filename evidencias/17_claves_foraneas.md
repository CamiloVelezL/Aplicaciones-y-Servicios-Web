# Evidencia 17 — Claves foráneas

## Datos de entrada
Comando en PostgreSQL:

```
\d mediciones
```

## Resultado obtenido

```
                                          Tabla «public.mediciones»
     Columna         |            Tipo             | Ordenamiento | Nulable | Predeterminado
---------------------+-----------------------------+--------------+---------+----------------
 id                  | bigint                      |              | not null| nextval(...)
 sensor_magnitud_id  | integer                     |              | not null|
 valor               | numeric(12,4)               |              | not null|
 timestamp_utc       | timestamp with time zone    |              | not null|
 fecha_recepcion     | timestamp with time zone    |              | not null| now()
Índices:
    "mediciones_pkey" PRIMARY KEY, btree (id)
    "idx_mediciones_sensor_magnitud" btree (sensor_magnitud_id)
    "idx_mediciones_timestamp_utc" btree (timestamp_utc)
    "idx_mediciones_magnitud_timestamp" btree (sensor_magnitud_id, timestamp_utc)
Restricciones de llave foránea:
    "fk_med_sm" FOREIGN KEY (sensor_magnitud_id)
        REFERENCES sensor_magnitudes(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
```

## Código HTTP
N/A.

## Registro almacenado o rechazado
N/A.

## Archivo y función
- `create_tables.sql` (definición de la FK)

## Explicación
La tabla `mediciones` tiene una **clave foránea** (`fk_med_sm`) que apunta a `sensor_magnitudes(id)`. Esto garantiza la integridad referencial:

- **ON UPDATE CASCADE**: si cambia el ID de `sensor_magnitudes`, se actualiza en `mediciones`.
- **ON DELETE RESTRICT**: no se puede borrar una magnitud que tenga mediciones asociadas, protegiendo el histórico.

Además, hay un índice compuesto (`idx_mediciones_magnitud_timestamp`) que optimiza las consultas por magnitud + rango de fechas.