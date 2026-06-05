
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings

# Motor asíncrono configurado con la URL validada
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Fábrica de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False
)

Base = declarative_base()

# Dependencia inyectable para los endpoints de FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session