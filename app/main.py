
from fastapi import FastAPI, Depends, HTTPException, status
# 1. Agregamos la importación del middleware de CORS aquí arriba:
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Importaciones de tus otros archivos modulares
from app.database import engine, Base, get_db
from app.schemas import AnimalCreate, AnimalResponse
from app import crud

# 2. Inicialización de la aplicación FastAPI
app = FastAPI(
    title="API de Animales Silvestres",
    description="CRUD asíncrono listo para producción en Render."
)

# 3. Configuración de CORS (Pégalo justo aquí)
origins = [
    "http://127.0.0.1:5500",  # Tu Live Server local (VS Code)
    "http://localhost:5500",   # Por si acaso usas localhost en lugar de la IP
     "*" # Permite cualquier origen (útil para desarrollo, pero ten cuidado en producción)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],      # Permite todas las cabeceras (headers)
)

# --- De aquí para abajo tu código se queda exactamente igual ---

# Ruta raíz para verificar el estado de la API
@app.get("/")
async def raiz():
    return {
        "status": "online",
        "mensaje": "API de Animales Silvestres corriendo perfectamente"
    }

# El bloque de arranque automático (Startup)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.get_context() if hasattr(engine, 'get_context') else None 
        await conn.run_sync(Base.metadata.create_all)


# Tus Endpoints / Rutas del CRUD

# Ruta para CREAR un animal
@app.post("/animales/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
async def crear_animal(animal: AnimalCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_animal(db=db, animal=animal)

# Ruta para LEER todos los animales
@app.get("/animales/", response_model=List[AnimalResponse])
async def listar_animales(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_animales(db=db, skip=skip, limit=limit)

# Ruta para LEER un solo animal por su ID
@app.get("/animales/{animal_id}", response_model=AnimalResponse)
async def obtener_animal(animal_id: int, db: AsyncSession = Depends(get_db)):
    db_animal = await crud.get_animal_by_id(db=db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return db_animal

# Ruta para ELIMINAR un animal por su ID
@app.delete("/animales/{animal_id}", response_model=AnimalResponse)
async def eliminar_animal(animal_id: int, db: AsyncSession = Depends(get_db)):
    db_animal = await crud.delete_animal(db=db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return db_animal

# Ruta para ACTUALIZAR un animal por su ID
@app.put("/animales/{animal_id}", response_model=AnimalResponse)
async def actualizar_animal(animal_id: int, animal: AnimalCreate, db: AsyncSession = Depends(get_db)):
    db_animal = await crud.update_animal(db=db, animal_id=animal_id, animal_data=animal)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return db_animal