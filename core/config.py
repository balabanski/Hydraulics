from typing import Dict, List, Optional, Union
import secrets
from pydantic import AnyHttpUrl, PostgresDsn, BaseSettings, AnyUrl, validator
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class DevelopmentSettings(BaseSettings):
    # SECURITY # JWT
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ACCESS_TOKEN_EXPIRE: int = 60 * 15
    REFRESH_TOKEN_EXPIRE: int = 60 * 60 * 24 * 30

    # PROJECT NAME, API PREFIX, CORS ORIGINS
    PROJECT_NAME: str
    PROJECT_VERSION: str = "2.1.0"
    API_STR: str = ""
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = "http://localhost:3000,http://localhost:8001"

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str = "db"
    TORTOISE_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    # (see URI validator) -> it will be like postgresql://user:password@localhost:5432/db

    #SQLite
    SQLITE_FILE_NAME: str



    # SQLAlchemy
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_POOL_RECYCLE: int = 1200
    SQLALCHEMY_POOL_TIMEOUT: int = 5
    SQLALCHEMY_MAX_OVERFLOW: int = 10

    # FIRST SUPERUSER
    # FIRST_SUPERUSER_EMAIL: EmailStr = "example@example.com"  # type: ignore
    FIRST_SUPERUSER_PASSWORD: str = "my_secret_password"

    # VALIDATORS
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins


    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER") + ":" + values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        env_file = os.path.join(BASE_DIR, 'envs/.env_dev')
        case_sensitive = True

class TestSettings(DevelopmentSettings):
    ...


class ProductionSettings(DevelopmentSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, 'envs/.env.prod')


settings = DevelopmentSettings()
# settings = ProductionSettings()
print("settings-------------", settings.SQLITE_FILE_NAME)

