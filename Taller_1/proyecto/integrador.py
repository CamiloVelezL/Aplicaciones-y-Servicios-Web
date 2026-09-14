import json
import csv
import os
import requests
from datetime import datetime, timezone, timedelta


URL_BASE = "https://appsweb.quantaiot.co"
EQUIPO = "EQUIPO-01-APPSWEB"

RUTA_A = "datos/proveedor_a.json"
RUTA_B = "datos/proveedor_b.csv"
RUTA_NORMALIZADAS = "salida/normalizadas.json"
RUTA_REPORTE = "salida/reporte.json"

ORIGENES_VALIDOS = {"proveedor_a", "proveedor_b"}
MAX_INTENTOS = 3  # 1 intento inicial + 2 reintentos



# Utilidades
def asegurar_salida():
    os.makedirs("salida", exist_ok=True)


def f_a_c(f):
    """Convierte grados Fahrenheit a Celsius."""
    return (float(f) - 32) * 5 / 9


def ms_a_kmh(ms):
    """Convierte metros por segundo a kilómetros por hora."""
    return float(ms) * 3.6



# Lectura de datos
def cargar_proveedor_a(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("records", [])
    except FileNotFoundError:
        print(f"[ERROR] Archivo no encontrado: {ruta}")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] JSON no interpretable: {ruta}")
        return []


def cargar_proveedor_b(ruta):
    registros = []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for fila in reader:
                registros.append(fila)
    except FileNotFoundError:
        print(f"[ERROR] Archivo no encontrado: {ruta}")
    except csv.Error as e:
        print(f"[ERROR] CSV defectuoso: {e}")
    return registros



# Normalización

def normalizar_proveedor_a(reg, idx):
    id_interno = reg.get("provider_record_id", f"proveedor_a-{idx}")
    try:
        temp_f = reg["measurements"]["temperature_f"]
        humedad = reg["measurements"]["relative_humidity"]
        viento_ms = reg["measurements"]["wind_speed_ms"]
        lat = reg["location"]["lat"]
        lon = reg["location"]["lon"]
        ciudad = reg["station"]["city_name"]
        pais = reg["station"]["country_code"]
        fecha_str = reg["observed_at"]

        temperatura_c = f_a_c(temp_f)
        viento_kmh = ms_a_kmh(viento_ms)
        fecha_iso = datetime.fromisoformat(fecha_str).isoformat()

        contrato = {
            "ciudad": ciudad,
            "pais": pais,
            "latitud": float(lat),
            "longitud": float(lon),
            "temperatura_c": temperatura_c,
            "humedad": float(humedad),
            "viento_kmh": viento_kmh,
            "fecha_hora": fecha_iso,
            "origen": "proveedor_a",
        }
        return {"id_interno": id_interno, "contrato": contrato}
    except Exception as e:
        return {"id_interno": id_interno, "error_normalizacion": str(e)}
    
TZ_COLOMBIA = timezone(timedelta(hours=-5))
def normalizar_proveedor_b(reg, idx):
    id_interno = reg.get("record_code", f"proveedor_b-{idx}")
    try:
        fecha_str = reg["measurement_time"]
        fecha_dt = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
        fecha_dt = fecha_dt.replace(tzinfo=TZ_COLOMBIA)
        fecha_iso = fecha_dt.isoformat()

        contrato = {
            "ciudad": reg["municipality"],
            "pais": reg["country"],
            "latitud": float(reg["latitude_deg"]),
            "longitud": float(reg["longitude_deg"]),
            "temperatura_c": float(reg["temp_celsius"]),
            "humedad": float(reg["humidity_pct"]),
            "viento_kmh": float(reg["wind_kmh"]),
            "fecha_hora": fecha_iso,
            "origen": "proveedor_b",
        }
        return {"id_interno": id_interno, "contrato": contrato}
    except Exception as e:
        return {"id_interno": id_interno, "error_normalizacion": str(e)}



# Validación local según CONTRATO_API.md

def validar_local(c):
    errores = []
    if not isinstance(c.get("ciudad"), str) or not c["ciudad"].strip():
        errores.append("ciudad vacía")
    if not isinstance(c.get("pais"), str) or not c["pais"].strip():
        errores.append("pais vacío")
    if not (-90 <= c.get("latitud", 999) <= 90):
        errores.append("latitud fuera de rango")
    if not (-180 <= c.get("longitud", 999) <= 180):
        errores.append("longitud fuera de rango")
    if not (0 <= c.get("humedad", -1) <= 100):
        errores.append("humedad fuera de rango")
    if c.get("viento_kmh", -1) < 0:
        errores.append("viento_kmh negativo")
    try:
        fecha = datetime.fromisoformat(c["fecha_hora"])
        if fecha.tzinfo is None:
            errores.append("fecha_hora sin zona horaria")
    except Exception:
        errores.append("fecha_hora inválida")
    if c.get("origen") not in ORIGENES_VALIDOS:
        errores.append("origen inválido")
    return errores





# Integración HTTP

def enviar_medicion(contrato):
    url = URL_BASE.rstrip("/") + "/api/v1/mediciones"
    headers = {
        "Content-Type": "application/json",
        "X-Equipo": EQUIPO,
    }

    for intento in range(MAX_INTENTOS):
        try:
            r = requests.post(url, json=contrato, headers=headers, timeout=10)
            try:
                respuesta = r.json()
            except ValueError:
                respuesta = {"raw": r.text}

            if r.status_code == 201:
                return {
                    "estado": "aceptado_api",
                    "status": r.status_code,
                    "respuesta": respuesta,
                }

            if 400 <= r.status_code < 500:
                return {
                    "estado": "rechazado_api",
                    "status": r.status_code,
                    "respuesta": respuesta,
                }

            if r.status_code >= 500:
                if intento < MAX_INTENTOS - 1:
                    continue
                return {
                    "estado": "error_comunicacion",
                    "status": r.status_code,
                    "respuesta": respuesta,
                }

            return {
                "estado": "error_comunicacion",
                "status": r.status_code,
                "respuesta": respuesta,
            }

        except (requests.Timeout, requests.ConnectionError) as e:
            if intento < MAX_INTENTOS - 1:
                continue
            return {"estado": "error_comunicacion", "error": str(e)}

    return {"estado": "error_comunicacion"}


def consultar_mediciones():
    url = URL_BASE.rstrip("/") + "/api/v1/mediciones"
    params = {"equipo": EQUIPO}
    try:
        r = requests.get(url, params=params, timeout=10)
        try:
            return {"status": r.status_code, "respuesta": r.json()}
        except ValueError:
            return {"status": r.status_code, "respuesta": r.text}
    except Exception as e:
        return {"status": None, "error": str(e)}



# Orquestación

def main():
    asegurar_salida()

    regs_a = cargar_proveedor_a(RUTA_A)
    regs_b = cargar_proveedor_b(RUTA_B)
    procesados = len(regs_a) + len(regs_b)

    normalizados = []
    errores_normalizacion = []

    for i, reg in enumerate(regs_a):
        res = normalizar_proveedor_a(reg, i)
        if "error_normalizacion" in res:
            errores_normalizacion.append(res)
        else:
            normalizados.append(res)

    for i, reg in enumerate(regs_b):
        res = normalizar_proveedor_b(reg, i)
        if "error_normalizacion" in res:
            errores_normalizacion.append(res)
        else:
            normalizados.append(res)

    with open(RUTA_NORMALIZADAS, "w", encoding="utf-8") as f:
        json.dump(
            [n["contrato"] for n in normalizados],
            f,
            ensure_ascii=False,
            indent=2,
        )

    validos = []
    rechazados_localmente = []
    for n in normalizados:
        errs = validar_local(n["contrato"])
        if errs:
            n["errores_validacion"] = errs
            rechazados_localmente.append(n)
        else:
            validos.append(n)

    resultados_envio = []
    for v in validos:
        res = enviar_medicion(v["contrato"])
        res["id_interno"] = v["id_interno"]
        resultados_envio.append(res)

    aceptados = sum(1 for r in resultados_envio if r["estado"] == "aceptado_api")
    rechazados_api = sum(1 for r in resultados_envio if r["estado"] == "rechazado_api")
    errores_com = sum(1 for r in resultados_envio if r["estado"] == "error_comunicacion")

    consulta = consultar_mediciones()

    reporte = {
        "resumen": {
            "procesados": procesados,
            "normalizados": len(normalizados),
            "errores_normalizacion": len(errores_normalizacion),
            "validos_localmente": len(validos),
            "rechazados_localmente": len(rechazados_localmente),
            "enviados": len(validos),
            "aceptados_api": aceptados,
            "rechazados_api": rechazados_api,
            "errores_comunicacion": errores_com,
        },
        "detalle": {
            "errores_normalizacion": errores_normalizacion,
            "rechazados_localmente": rechazados_localmente,
            "envios": resultados_envio,
        },
        "consulta_final": consulta,
    }

    with open(RUTA_REPORTE, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    print("=== RESUMEN ===")
    for k, v in reporte["resumen"].items():
        print(f"{k}: {v}")
    print("=== CONSULTA FINAL ===")
    print(consulta)


if __name__ == "__main__":
    main()