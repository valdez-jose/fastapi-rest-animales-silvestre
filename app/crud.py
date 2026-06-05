
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Animal
from app.schemas import AnimalCreate

async def get_animales(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Animal).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_animal_by_id(db: AsyncSession, animal_id: int):
    query = select(Animal).where(Animal.id == animal_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_animal(db: AsyncSession, animal: AnimalCreate):
    # .model_dump() es el reemplazo moderno de .dict() en Pydantic v2
    db_animal = Animal(**animal.model_dump())
    db.add(db_animal)
    await db.commit()
    await db.refresh(db_animal)
    return db_animal

async def delete_animal(db: AsyncSession, animal_id: int):
    db_animal = await get_animal_by_id(db, animal_id)
    if db_animal:
        await db.delete(db_animal)
        await db.commit()
    return db_animal

from sqlalchemy.future import select # Asegúrate de tener esta importación arriba

async def update_animal(db: AsyncSession, animal_id: int, animal_data: AnimalCreate):
    # 1. Buscar el animal existente por su ID
    result = await db.execute(select(Animal).filter(Animal.id == animal_id)) # Cambia 'Animal' por el nombre de tu modelo si es diferente
    db_animal = result.scalars().first()
    
    if db_animal:
        # 2. Convertir los datos entrantes en un diccionario
        update_data = animal_data.dict(exclude_unset=True)
        
        # 3. Iterar sobre los campos y actualizar el modelo de la BD
        for key, value in update_data.items():
            setattr(db_animal, key, value)
        
        # 4. Guardar cambios y refrescar el objeto
        await db.commit()
        await db.refresh(db_animal)
        
    return db_animal