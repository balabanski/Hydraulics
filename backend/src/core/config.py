from typing import Dict, List, Optional, Union, Any
import secrets
from pydantic import AnyHttpUrl, PostgresDsn, BaseSettings, AnyUrl, validator, Field, SecretStr
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
print(BASE_DIR)


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

    DATABASE: Optional[str] = None
    # Postgres
    POSTGRES_USER: str
    # POSTGRES_PASSWORD: SecretStr =environ.get('POSTGRES', "db_password")
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    TORTOISE_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    # (see URI validator) -> it will be like postgresql://user:password@localhost:5432/db

    # SQLite
    SQLITE_FILE_NAME: Optional[str] = None

    # SQLAlchemy
    DEBUG: bool = Field(default=True, env="DEBUG")
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

    '''
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER") + ":" + values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    '''
    # database = os.environ.get("DATABASE", "sqlite")

    @property
    def POSTGRES_URL(self) -> str:
        """
        строки легче конкатенировать, чем парсить!
        Это property (свойство) пригодится нам в будущем, когда будем подключаться к БД.
        """
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


    @property
    def sqlite_url(self) -> str:
        return f"sqlite+aiosqlite:///" + settings.SQLITE_FILE_NAME

    class Config:
        local = os.environ.get("USE_LOCAL_DB", "True")
        print('local_________________________________________________', local)

        if local == "False":
            env_file = os.path.join(BASE_DIR, 'src/envs/.env_dev')
        else:
            env_file = os.path.join(BASE_DIR, 'src/envs/.env_local')

        case_sensitive = True


class TestSettings(DevelopmentSettings):
    ...


class ProductionSettings(DevelopmentSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, 'src/envs/.env_prod')


settings = DevelopmentSettings()
# settings = ProductionSettings()


