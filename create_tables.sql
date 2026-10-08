-- ============================================================
-- Taller 2 - IoT AQ-003
-- Script de creación de tablas (según data-model.md)
-- Base: appdb - Esquema: public
-- ============================================================

DROP TABLE IF EXISTS mediciones CASCADE;
DROP TABLE IF EXISTS sensor_magnitudes CASCADE;
DROP TABLE IF EXISTS sensores CASCADE;

-- ------------------------------------------------------------
-- Tabla: sensores
-- ------------------------------------------------------------
CREATE TABLE sensores (
    id              SERIAL PRIMARY KEY,
    codigo          VARCHAR(20)  NOT NULL UNIQUE,
    nombre          VARCHAR(100) NOT NULL,
    categoria       VARCHAR(30)  NOT NULL
                    CHECK (categoria IN ('AIRE', 'GAS', 'AGUA', 'AMBIENTE')),
    ubicacion       VARCHAR(100) NOT NULL,
    activo          BOOLEAN      NOT NULL DEFAULT TRUE,
    fecha_registro  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Tabla: sensor_magnitudes
-- ------------------------------------------------------------
CREATE TABLE sensor_magnitudes (
    id              SERIAL PRIMARY KEY,
    sensor_id       INTEGER       NOT NULL,
    magnitud        VARCHAR(50)   NOT NULL,
    unidad          VARCHAR(20)   NOT NULL,
    valor_minimo    NUMERIC(12,4) NOT NULL,
    valor_maximo    NUMERIC(12,4) NOT NULL,
    CONSTRAINT fk_sm_sensor
        FOREIGN KEY (sensor_id) REFERENCES sensores(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT uq_sensor_magnitud UNIQUE (sensor_id, magnitud),
    CONSTRAINT ck_rango CHECK (valor_minimo < valor_maximo)
);

-- ------------------------------------------------------------
-- Tabla: mediciones
-- ------------------------------------------------------------
CREATE TABLE mediciones (
    id                    BIGSERIAL     PRIMARY KEY,
    sensor_magnitud_id    INTEGER       NOT NULL,
    valor                 NUMERIC(12,4) NOT NULL,
    timestamp_utc         TIMESTAMPTZ   NOT NULL,
    fecha_recepcion       TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_med_sm
        FOREIGN KEY (sensor_magnitud_id) REFERENCES sensor_magnitudes(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- Índices
-- ------------------------------------------------------------
CREATE INDEX idx_mediciones_sensor_magnitud
    ON mediciones (sensor_magnitud_id);

CREATE INDEX idx_mediciones_timestamp_utc
    ON mediciones (timestamp_utc);

CREATE INDEX idx_mediciones_magnitud_timestamp
    ON mediciones (sensor_magnitud_id, timestamp_utc);