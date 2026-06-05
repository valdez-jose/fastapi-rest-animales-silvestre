
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    DATABASE_URL: str
    PORT: int = 8000 

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_postgres_protocol(cls, v: str) -> str:
        # Corrige el formato de URL que entrega Render para que sea compatible con SQLAlchemy Async
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()