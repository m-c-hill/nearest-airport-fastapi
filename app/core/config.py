from pydantic import BaseSettings, Field


class Development(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    db_url: str = Field(..., env="DATABASE_URL")


class Testing(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    db_url: str = Field(..., env="DATABASE_URL")


config = {"development": Development(), "testing": Testing()}
