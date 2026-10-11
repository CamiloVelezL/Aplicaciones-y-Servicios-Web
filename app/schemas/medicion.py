from datetime import datetime
from decimal import Decimal
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------- Schemas para responder por la API ----------

class MedicionOut(BaseModel):
    id: int
    sensor_magnitud_id: int
    valor: Decimal
    timestamp_utc: datetime
    fecha_recepcion: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Schemas para validar el payload MQTT ----------

class MeasurementItem(BaseModel):
    value: float
    unit: str


class MQTTMessage(BaseModel):
    sensor_id: str
    timestamp: datetime
    measurements: Dict[str, MeasurementItem] = Field(..., min_length=1)

    @field_validator("timestamp")
    @classmethod
    def validar_timestamp(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("timestamp debe incluir zona horaria UTC")
        return v