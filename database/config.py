from functools import lru_cache
from os import getenv

from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class DatabaseSettings(BaseSettings):
    DEV_MODE:          bool | None = None

    POSTGRES_DB:       str | None = None
    POSTGRES_USER:     str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST:     str | None = None
    POSTGRES_PORT:     str | None = None

    SQLALCHEMY_URL:    str | None = None

    @field_validator('DEV_MODE')
    @classmethod
    def validate_debug(cls, value: bool | None, info: ValidationInfo):    
        if value is not None:
            return value
        
        load_dotenv(".env.dev")

        if (new_value := getenv("DEV_MODE")) is None:
            raise EnvironmentError("miss at least .env.dev")
        
        value = new_value.lower() != "false"

        return value
    
    @field_validator("POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT")
    @classmethod
    def get_lost_variables(cls, value, info: ValidationInfo):
        if not info.data["DEV_MODE"]:
            return value

        return getenv(info.field_name)


    @field_validator('SQLALCHEMY_URL')
    @classmethod
    def validate_sqlalchemy_url(cls, value: str | None, info: ValidationInfo):
        if isinstance(value, str):
            return value

        return str(PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=info.data["POSTGRES_USER"],
            password=info.data["POSTGRES_PASSWORD"],
            host=info.data["POSTGRES_HOST"],
            port=int(info.data["POSTGRES_PORT"]),
            path=info.data["POSTGRES_DB"],
        ))


@lru_cache
def get_settings() -> DatabaseSettings:
    return DatabaseSettings()
