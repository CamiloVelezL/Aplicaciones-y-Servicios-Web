from datetime import datetime
from typing import List, Optional
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud import medicion as crud_medicion
from app.crud import sensor as crud_sensor
from app.database.connection import get_db
from app.schemas.medicion import MedicionOut

router = APIRouter(tags=["mediciones"])

COLOMBIA_TZ = ZoneInfo("America/Bogota")


def _to_colombia(dt: datetime) -> datetime:
    return dt.astimezone(COLOMBIA_TZ)


@router.get("/mediciones/{medicion_id}", response_model=MedicionOut)
def obtener_medicion(medicion_id: int, db: Session = Depends(get_db)):
    m = crud_medicion.get_by_id(db, medicion_id)
    if not m:
        raise HTTPException(status_code=404, detail="Medicion no encontrada")
    return MedicionOut(
        id=m.id,
        sensor_magnitud_id=m.sensor_magnitud_id,
        valor=m.valor,
        timestamp_utc=_to_colombia(m.timestamp_utc),
        fecha_recepcion=_to_colombia(m.fecha_recepcion),
    )


@router.get("/sensores/{sensor_id}/mediciones", response_model=List[MedicionOut])
def mediciones_del_sensor(
    sensor_id: int,
    magnitud: Optional[str] = Query(None),
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
    limit: Optional[int] = Query(None, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    if not crud_sensor.get_by_id(db, sensor_id):
        raise HTTPException(status_code=404, detail="Sensor no encontrado")

    if desde and hasta and desde > hasta:
        raise HTTPException(
            status_code=400,
            detail="'desde' no puede ser mayor que 'hasta'",
        )

    datos = crud_medicion.get_by_sensor(
        db, sensor_id, magnitud=magnitud, desde=desde, hasta=hasta, limit=limit
    )
    return [
        MedicionOut(
            id=m.id,
            sensor_magnitud_id=m.sensor_magnitud_id,
            valor=m.valor,
            timestamp_utc=_to_colombia(m.timestamp_utc),
            fecha_recepcion=_to_colombia(m.fecha_recepcion),
        )
        for m in datos
    ]


@router.get("/sensores/{sensor_id}/ultima-medicion", response_model=MedicionOut)
def ultima_medicion(sensor_id: int, db: Session = Depends(get_db)):
    if not crud_sensor.get_by_id(db, sensor_id):
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    m = crud_medicion.get_ultima(db, sensor_id)
    if not m:
        raise HTTPException(status_code=404, detail="No hay mediciones para el sensor")
    return MedicionOut(
        id=m.id,
        sensor_magnitud_id=m.sensor_magnitud_id,
        valor=m.valor,
        timestamp_utc=_to_colombia(m.timestamp_utc),
        fecha_recepcion=_to_colombia(m.fecha_recepcion),
    )