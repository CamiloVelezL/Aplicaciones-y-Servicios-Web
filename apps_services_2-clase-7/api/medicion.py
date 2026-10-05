from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db 
from schemas.medicion import MedicionCreate, MedicionResponse, MedicionUpdate
from crud import medicion as crud_medicion

router = APIRouter(prefix="/mediciones", tags=["mediciones"])

@router.get("/", response_model=List[MedicionResponse])
def read_mediciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_medicion.get_mediciones(db, skip=skip, limit=limit)

@router.get("/{medicion_id}", response_model=MedicionResponse)
def read_medicion(medicion_id: int, db: Session = Depends(get_db)):
    db_medicion = crud_medicion.get_medicion(db, medicion_id=medicion_id)
    if db_medicion is None:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return db_medicion

@router.post("/", response_model=MedicionResponse, status_code=status.HTTP_201_CREATED)
def create_medicion(medicion: MedicionCreate, db: Session = Depends(get_db)):
    return crud_medicion.create_medicion(db=db, medicion=medicion)

@router.put("/{medicion_id}", response_model=MedicionResponse)
def update_medicion(medicion_id: int, medicion: MedicionUpdate, db: Session = Depends(get_db)):
    db_medicion = crud_medicion.update_medicion(db, medicion_id=medicion_id, medicion=medicion)
    if db_medicion is None:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return db_medicion

@router.delete("/{medicion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicion(medicion_id: int, db: Session = Depends(get_db)):
    db_medicion = crud_medicion.delete_medicion(db, medicion_id=medicion_id)
    if db_medicion is None:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return None