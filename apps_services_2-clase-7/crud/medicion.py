from sqlalchemy.orm import Session
from models.medicion import Medicion
from schemas.medicion import MedicionCreate, MedicionUpdate

def get_mediciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicion).offset(skip).limit(limit).all()

def get_medicion(db: Session, medicion_id: int):
    return db.query(Medicion).filter(Medicion.id == medicion_id).first()

def create_medicion(db: Session, medicion: MedicionCreate):
    db_medicion = Medicion(**medicion.model_dump())
    db.add(db_medicion)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion

def update_medicion(db: Session, medicion_id: int, medicion: MedicionUpdate):
    db_medicion = db.query(Medicion).filter(Medicion.id == medicion_id).first()
    if db_medicion:
        # Excluimos los campos que no se enviaron (None) para actualización parcial
        update_data = medicion.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_medicion, key, value)
        db.commit()
        db.refresh(db_medicion)
    return db_medicion

def delete_medicion(db: Session, medicion_id: int):
    db_medicion = db.query(Medicion).filter(Medicion.id == medicion_id).first()
    if db_medicion:
        db.delete(db_medicion)
        db.commit()
    return db_medicion