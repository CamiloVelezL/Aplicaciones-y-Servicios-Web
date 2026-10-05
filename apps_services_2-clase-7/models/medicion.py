from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Asegúrate de que tu Base esté importada correctamente desde database.py

class Medicion(Base):
    __tablename__ = "mediciones"
    __table_args__ = {"schema": "public"}  # Importante porque la tabla está en el esquema public

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("public.estudiantes.id"), nullable=False)
    variable = Column(String(50), nullable=False)
    valor = Column(Numeric, nullable=False)
    unidad = Column(String(20), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), nullable=False)

    # Relación opcional (si tienes el modelo Estudiante creado, puedes descomentar esto)
   # estudiante = relationship("Estudiante", back_populates="mediciones")