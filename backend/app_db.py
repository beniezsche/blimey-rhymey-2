from curses import echo
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL, echo = True, future = True, connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
