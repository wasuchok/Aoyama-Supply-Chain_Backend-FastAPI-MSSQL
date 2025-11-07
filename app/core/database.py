from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


connection_string = (
    f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_SERVER},{settings.DB_PORT}/{settings.DB_NAME}"
    f"?driver={settings.DB_DRIVER}&encrypt={settings.DB_ENCRYPT}"
)

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
