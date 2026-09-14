from datetime import timezone, timedelta

from integrador import (
    f_a_c,
    ms_a_kmh,
    validar_local,
    normalizar_proveedor_b,
    TZ_COLOMBIA,
)


def test_conversion_fahrenheit_a_celsius():
    assert abs(f_a_c(32) - 0) < 1e-9
    assert abs(f_a_c(212) - 100) < 1e-9


def test_conversion_ms_a_kmh():
    assert abs(ms_a_kmh(1) - 3.6) < 1e-9
    assert abs(ms_a_kmh(10) - 36.0) < 1e-9


def test_registro_valido():
    c = {
        "ciudad": "Medellin",
        "pais": "CO",
        "latitud": 6.2,
        "longitud": -75.5,
        "temperatura_c": 20,
        "humedad": 80,
        "viento_kmh": 10,
        "fecha_hora": "2026-09-01T00:00:00-05:00",
        "origen": "proveedor_a",
    }
    assert validar_local(c) == []


def test_registro_invalido_humedad():
    c = {
        "ciudad": "Medellin",
        "pais": "CO",
        "latitud": 6.2,
        "longitud": -75.5,
        "temperatura_c": 20,
        "humedad": 117.5,
        "viento_kmh": 10,
        "fecha_hora": "2026-09-01T00:00:00-05:00",
        "origen": "proveedor_a",
    }
    errores = validar_local(c)
    assert "humedad fuera de rango" in errores


def test_caso_limite_fecha_sin_zona_horaria():
    c = {
        "ciudad": "Medellin",
        "pais": "CO",
        "latitud": 6.2,
        "longitud": -75.5,
        "temperatura_c": 20,
        "humedad": 80,
        "viento_kmh": 10,
        "fecha_hora": "2026-09-01T00:00:00",
        "origen": "proveedor_a",
    }
    errores = validar_local(c)
    assert "fecha_hora sin zona horaria" in errores


def test_normalizar_b_incluye_zona_horaria():
    reg = {
        "record_code": "B-TEST",
        "municipality": "Medellin",
        "country": "CO",
        "latitude_deg": "6.2",
        "longitude_deg": "-75.5",
        "temp_celsius": "20",
        "humidity_pct": "50",
        "wind_kmh": "10",
        "measurement_time": "01/09/2026 06:00",
        "origin_code": "PB",
    }
    res = normalizar_proveedor_b(reg, 0)
    assert "error_normalizacion" not in res
    assert res["contrato"]["fecha_hora"] == "2026-09-01T06:00:00-05:00"