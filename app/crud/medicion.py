from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.medicion import Medicion
from app.models.sensor_magnitud import SensorMagnitud


def create(
    db: Session,
    sensor_magnitud_id: int,
    valor: float,
    timestamp_utc: datetime,
) -> Medicion:
    m = Medicion(
        sensor_magnitud_id=sensor_magnitud_id,
        valor=valor,
        timestamp_utc=timestamp_utc,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def get_by_id(db: Session, medicion_id: int) -> Optional[Medicion]:
    return db.query(Medicion).filter(Medicion.id == medicion_id).first()


def get_by_sensor(
    db: Session,
    sensor_id: int,
    magnitud: Optional[str] = None,
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    limit: Optional[int] = None,
) -> List[Medicion]:
    q = (db.query(Medicion)
           .join(SensorMagnitud)
           .filter(SensorMagnitud.sensor_id == sensor_id))

    if magnitud:
        q = q.filter(SensorMagnitud.magnitud == magnitud)
    if desde:
        q = q.filter(Medicion.timestamp_utc >= desde)
    if hasta:
        q = q.filter(Medicion.timestamp_utc <= hasta)

    q = q.order_by(Medicion.timestamp_utc.desc())

    if limit:
        q = q.limit(limit)

    return q.all()


def get_ultima(db: Session, sensor_id: int) -> Optional[Medicion]:
    return (db.query(Medicion)
              .join(SensorMagnitud)
              .filter(SensorMagnitud.sensor_id == sensor_id)
              .order_by(Medicion.timestamp_utc.desc())
              .first())