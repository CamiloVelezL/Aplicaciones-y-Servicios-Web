-- ============================================================
-- Taller 2 - IoT AQ-003
-- Catalogo inicial: sensor AQ-003 + sus 4 magnitudes
-- ============================================================

INSERT INTO sensores (codigo, nombre, categoria, ubicacion, activo)
VALUES ('AQ-003',
        'Sensor de calidad del aire AQ-003',
        'AIRE',
        'Laboratorio DevOps',
        TRUE);

INSERT INTO sensor_magnitudes (sensor_id, magnitud, unidad, valor_minimo, valor_maximo)
SELECT id, 'temperature', 'C',   -10,   60   FROM sensores WHERE codigo = 'AQ-003'
UNION ALL
SELECT id, 'humidity',    '%',     0,  100   FROM sensores WHERE codigo = 'AQ-003'
UNION ALL
SELECT id, 'tvoc',        'ppb',   0, 5000   FROM sensores WHERE codigo = 'AQ-003'
UNION ALL
SELECT id, 'eco2',        'ppm', 400, 5000   FROM sensores WHERE codigo = 'AQ-003';

-- Verificacion
SELECT s.id AS sensor_id, s.codigo, sm.id AS sm_id, sm.magnitud, sm.unidad,
       sm.valor_minimo, sm.valor_maximo
FROM sensores s
JOIN sensor_magnitudes sm ON sm.sensor_id = s.id
WHERE s.codigo = 'AQ-003'
ORDER BY sm.id;