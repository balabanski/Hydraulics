import os
import secrets
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, Field, PostgresDsn, validator


BASE_DIR = Path(__file__).resolve().parents[2]
print(BASE_DIR)


class DevelopmentSettings(BaseSettings):
    ENV: str = Field(default="dev", env="ENV")
    VERSION: str = Field(default="v1", env="VERSION")

    USE_SENTRY: bool = Field(default=False, env="USE_SENTRY")

    # SECURITY # JWT
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ACCESS_TOKEN_EXPIRE: int = 60 * 15
    REFRESH_TOKEN_EXPIRE: int = 60 * 60 * 24 * 30

    # PROJECT NAME, API PREFIX, CORS ORIGINS
    PROJECT_NAME: str
    PROJECT_VERSION: str = "2.1.0"
    API_V1_STR: str = "/api/v1"
    # SERVER_NAME: str
    DOMAIN: str
    SERVER_HOST: AnyHttpUrl
    # SERVER_HOST: AnyHttpUrl = "http://${DOMAIN?Variable not set}"
    # BACKEND_CORS_ORIGINS: Union[
    #     str, List[AnyHttpUrl]
    # ] = "http://localhost:3000,http://localhost:8001"
    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

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

    # Redis
    REDIS_HOST: str = Field(default="", env="REDIS_HOST")
    REDIS_PORT: str = Field(default="", env="REDIS_PORT")

    # SQLite
    SQLITE_FILE_NAME: Optional[str] = None

    # SQLAlchemy
    DEBUG: bool = Field(default=True, env="DEBUG")

    DB_POOL_SIZE: int = Field(default=83, env="DB_POOL_SIZE")
    WEB_CONCURRENCY: int = Field(default=9, env="WEB_CONCURRENCY")
    MAX_OVERFLOW: int = Field(default=64, env="MAX_OVERFLOW")

    POOL_SIZE: int = Field(default=None, env="POOL_SIZE")
    # POSTGRES_URL: str = Field(default=None, env="POSTGRES_URL")

    # SQLALCHEMY_POOL_RECYCLE: int = 1200
    # SQLALCHEMY_POOL_TIMEOUT: int = 5
    # SQLALCHEMY_MAX_OVERFLOW: int = 10

    # FIRST SUPERUSER
    # FIRST_SUPERUSER_EMAIL: EmailStr = "example@example.com"  # type: ignore
    FIRST_SUPERUSER_PASSWORD: str = "my_secret_password"

    # VALIDATORS

    @validator("POOL_SIZE", pre=True)  # , check_fields=False
    def build_pool(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, int):
            return v
        return max(values.get("DB_POOL_SIZE") // values.get("WEB_CONCURRENCY"), 5)  # type: ignore

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    # @validator("POSTGRES_URL", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, str]) -> str:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql+asyncpg",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER") + ":" + values.get("POSTGRES_PORT"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    # database = os.environ.get("DATABASE", "sqlite")

    SMTP_TLS: bool = True
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "backend/src/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST") and values.get("SMTP_PORT") and values.get("EMAILS_FROM_EMAIL")
        )

    @property
    def POSTGRES_URL(self) -> str:
        """
        строки легче конкатенировать, чем парсить!
        Это property (свойство) пригодится нам в будущем, когда будем подключаться к БД.
        """
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def sqlite_url(self) -> str:
        return "sqlite+aiosqlite:///" + settings.SQLITE_FILE_NAME

    # EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    # FIRST_SUPERUSER: EmailStr
    # FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = True  # False

    class Config:
        local = os.environ.get("USE_LOCAL_DB", "True")
        # local = os.environ.get("USE_LOCAL_DB", "False")
        print("local_________________________________________________", local)
        if local == "False":
            env_file = os.path.join(BASE_DIR, "src/envs/.env_dev")
        else:
            env_file = os.path.join(BASE_DIR, "src/envs/.env_local")

        case_sensitive = True


class TestSettings(DevelopmentSettings):
    ...


class ProductionSettings(DevelopmentSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, "src/envs/.env_prod")


settings = DevelopmentSettings()
# settings = ProductionSettings()

# print('settings.BACKEND_CORS_ORIGINS_______________', settings.BACKEND_CORS_ORIGINS)
# print("POOL_SIZE_________________________________", settings.POOL_SIZE)
print(settings.SECRET_KEY)
