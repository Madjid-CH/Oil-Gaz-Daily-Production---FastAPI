from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(bind=engine)