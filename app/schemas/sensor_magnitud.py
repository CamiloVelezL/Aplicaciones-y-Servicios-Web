from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class SensorMagnitudOut(BaseModel):
    id: int
    sensor_id: int
    magnitud: str
    unidad: str
    valor_minimo: Decimal
    valor_maximo: Decimal

    model_config = ConfigDict(from_attributes=True)