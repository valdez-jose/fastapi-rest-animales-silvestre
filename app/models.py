
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class Animal(Base):
    __tablename__ = "animales"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_comun = Column(String, nullable=False)
    nombre_cientifico = Column(String, nullable=False)
    habitat = Column(String, nullable=False)
    estado_conservacion = Column(String, nullable=False)
    registrado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))