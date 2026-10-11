from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sensor_magnitud import SensorMagnitud


def get_by_id(db: Session, sm_id: int) -> Optional[SensorMagnitud]:
    return db.query(SensorMagnitud).filter(SensorMagnitud.id == sm_id).first()


def get_by_sensor(db: Session, sensor_id: int) -> List[SensorMagnitud]:
    return (db.query(SensorMagnitud)
              .filter(SensorMagnitud.sensor_id == sensor_id)
              .order_by(SensorMagnitud.id)
              .all())


def get_by_sensor_and_magnitud(
    db: Session, sensor_id: int, magnitud: str
) -> Optional[SensorMagnitud]:
    return (db.query(SensorMagnitud)
              .filter(SensorMagnitud.sensor_id == sensor_id,
                      SensorMagnitud.magnitud == magnitud)
              .first())