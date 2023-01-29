from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database

DATABASE_PATH = database.__file__.replace("__init__.py", "database.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db
