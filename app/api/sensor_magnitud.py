from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import sensor_magnitud as crud_sm
from app.database.connection import get_db
from app.schemas.sensor_magnitud import SensorMagnitudOut

router = APIRouter(prefix="/sensor-magnitudes", tags=["sensor-magnitudes"])


@router.get("/{sm_id}", response_model=SensorMagnitudOut)
def obtener_sensor_magnitud(sm_id: int, db: Session = Depends(get_db)):
    sm = crud_sm.get_by_id(db, sm_id)
    if not sm:
        raise HTTPException(status_code=404, detail="Sensor-magnitud no encontrado")
    return sm