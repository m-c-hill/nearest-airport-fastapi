"""
Configuration class for the app, with settings retrieved from environment variables, set using the .env 
file in the root directory.
"""

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(".env")


class Settings(BaseSettings):
    environment: str = Field(..., env="ENV")
    secret_key: str = Field(..., env="SECRET_KEY")
    db_url: str = Field(..., env="DATABASE_URL")
    test_db_url: str = Field(..., env="TEST_DATABASE_URL")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
