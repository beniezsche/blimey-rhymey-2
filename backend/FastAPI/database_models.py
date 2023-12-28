from sqlalchemy import Column, Integer, String

from app_db import Base

class Headlines(Base):
    __tablename__ = "headlines"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, unique=False, index=True)
    rhyme = Column(String)

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(String, index = True)
    token = Column(String, unique=False)

class Tokens(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key = True, index = True)
    token = Column(String, unique=False)