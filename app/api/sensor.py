from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import sensor as crud_sensor
from app.crud import sensor_magnitud as crud_sm
from app.database.connection import get_db
from app.schemas.sensor import SensorOut
from app.schemas.sensor_magnitud import SensorMagnitudOut

router = APIRouter(prefix="/sensores", tags=["sensores"])


@router.get("", response_model=List[SensorOut])
def listar_sensores(db: Session = Depends(get_db)):
    return crud_sensor.get_all(db)


@router.get("/por-codigo/{codigo}", response_model=SensorOut)
def obtener_por_codigo(codigo: str, db: Session = Depends(get_db)):
    s = crud_sensor.get_by_codigo(db, codigo)
    if not s:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return s


@router.get("/{sensor_id}", response_model=SensorOut)
def obtener_sensor(sensor_id: int, db: Session = Depends(get_db)):
    s = crud_sensor.get_by_id(db, sensor_id)
    if not s:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return s


@router.get("/{sensor_id}/magnitudes", response_model=List[SensorMagnitudOut])
def magnitudes_del_sensor(sensor_id: int, db: Session = Depends(get_db)):
    if not crud_sensor.get_by_id(db, sensor_id):
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return crud_sm.get_by_sensor(db, sensor_id)