from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_SERVER: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_ENCRYPT: str
    DB_DRIVER: str

    class Config:
        project_root = Path(__file__).resolve().parents[2]
        env_file = project_root / ".env"

settings = Settings()
