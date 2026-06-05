
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AnimalBase(BaseModel):
    nombre_comun: str
    nombre_cientifico: str
    habitat: str
    estado_conservacion: str

class AnimalCreate(AnimalBase):
    pass

class AnimalResponse(AnimalBase):
    id: int
    registrado_en: datetime

    # Necesario para mapear los objetos de SQLAlchemy a JSON automáticamente
    model_config = ConfigDict(from_attributes=True)