from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_URL
from app.models.base import Base

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
