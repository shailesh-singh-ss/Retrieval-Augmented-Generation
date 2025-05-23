import os
from sqlmodel import create_engine, SQLModel, Session
from contextlib import contextmanager

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./metadata.db")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_db():
    with Session(engine) as session:
        yield session