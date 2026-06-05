
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AnimalBase(BaseModel):
    nombre_comun: str
    nombre_cientifico: str
    habitat: str
    estado_conservacion: str
    imagen_url: str

class AnimalCreate(AnimalBase):
    pass

class AnimalResponse(AnimalBase):
    id: int
    registrado_en: datetime

    model_config = ConfigDict(from_attributes=True)