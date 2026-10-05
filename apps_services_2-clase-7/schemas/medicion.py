from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal

# Esquema base con los campos comunes
class MedicionBase(BaseModel):
    estudiante_id: int
    variable: str
    valor: Decimal
    unidad: str
    fecha_hora: datetime

# Esquema para crear (lo que recibimos del usuario)
class MedicionCreate(MedicionBase):
    pass

# Esquema para actualizar (todos los campos opcionales)
class MedicionUpdate(BaseModel):
    estudiante_id: int | None = None
    variable: str | None = None
    valor: Decimal | None = None
    unidad: str | None = None
    fecha_hora: datetime | None = None

# Esquema de respuesta (lo que devolvemos, incluye el ID generado por la BD)
class MedicionResponse(MedicionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)