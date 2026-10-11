"""
Consumidor MQTT con validaciones Pydantic + ORM y persistencia en PostgreSQL.
"""
import json
import logging
import os
from datetime import timezone

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from pydantic import ValidationError

from app.crud import medicion as crud_medicion
from app.crud import sensor as crud_sensor
from app.crud import sensor_magnitud as crud_sm
from app.database.connection import SessionLocal
from app.schemas.medicion import MQTTMessage

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("mqtt")

BROKER = os.getenv("MQTT_BROKER", "emqx.coriotlab.co")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "iot/sensors/AQ-003/data")
USERNAME = os.getenv("MQTT_USERNAME") or None
PASSWORD = os.getenv("MQTT_PASSWORD") or None
KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))

_mqtt_client = None


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code != 0:
        logger.error(f"Error de conexion MQTT: {reason_code}")
        return
    logger.info(f"Conectado al broker {BROKER}:{PORT}")
    client.subscribe(TOPIC)
    logger.info(f"Suscrito al topico: {TOPIC}")


def _validar_y_guardar(payload: dict) -> None:
    db = SessionLocal()
    try:
        # 1) Validacion de estructura con Pydantic
        try:
            data = MQTTMessage(**payload)
        except ValidationError as e:
            logger.warning(f"[Pydantic] Payload invalido: {e}")
            return

        # 2) Validar sensor
        sensor = crud_sensor.get_by_codigo(db, data.sensor_id)
        if not sensor:
            logger.warning(f"Rechazado: sensor inexistente {data.sensor_id}")
            return
        if not sensor.activo:
            logger.warning(f"Rechazado: sensor inactivo {data.sensor_id}")
            return

        # 3) Validar TODAS las magnitudes antes de guardar
        items_a_guardar = []
        for nombre_mag, item in data.measurements.items():
            sm = crud_sm.get_by_sensor_and_magnitud(db, sensor.id, nombre_mag)
            if not sm:
                logger.warning(
                    f"Rechazado: magnitud {nombre_mag} no asociada al sensor"
                )
                return
            if sm.unidad != item.unit:
                logger.warning(
                    f"Rechazado: unidad incorrecta para {nombre_mag} "
                    f"(recibido {item.unit}, esperado {sm.unidad})"
                )
                return
            if not (float(sm.valor_minimo) <= item.value <= float(sm.valor_maximo)):
                logger.warning(
                    f"Rechazado: valor {item.value} fuera de rango "
                    f"para {nombre_mag} [{sm.valor_minimo}, {sm.valor_maximo}]"
                )
                return
            items_a_guardar.append((sm.id, item.value))

        # 4) Guardar todas las mediciones con el mismo timestamp
        ts = data.timestamp.astimezone(timezone.utc)
        for sm_id, valor in items_a_guardar:
            crud_medicion.create(db, sm_id, valor, ts)
        logger.info(
            f"OK: guardadas {len(items_a_guardar)} mediciones "
            f"del sensor {data.sensor_id} @ {ts.isoformat()}"
        )

    except Exception as e:
        logger.exception(f"Error procesando mensaje: {e}")
        db.rollback()
    finally:
        db.close()


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        logger.warning(f"Payload no es JSON valido: {e}")
        return

    logger.info(f"Mensaje recibido: {payload}")
    _validar_y_guardar(payload)


def start_mqtt() -> mqtt.Client:
    """Inicia el cliente MQTT en segundo plano."""
    global _mqtt_client
    if _mqtt_client is not None:
        return _mqtt_client

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD or "")

    client.on_connect = on_connect
    client.on_message = on_message

    logger.info(f"Conectando a {BROKER}:{PORT} ...")
    client.connect(BROKER, PORT, KEEPALIVE)
    client.loop_start()

    _mqtt_client = client
    return client


def stop_mqtt() -> None:
    global _mqtt_client
    if _mqtt_client is not None:
        _mqtt_client.loop_stop()
        _mqtt_client.disconnect()
        _mqtt_client = None