from sqlmodel import create_engine, Session

from app.settings import settings

engine = create_engine(
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db}"
)
SessionLocal = Session(engine)
