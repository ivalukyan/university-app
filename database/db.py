"""
Database module
"""

from uuid import uuid4

from sqlalchemy import Column, Integer, String, DateTime, UUID, Boolean, LargeBinary, BIGINT

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#from env import Postgres

import os
from dotenv import load_dotenv


load_dotenv()


class Postgres:
    def __init__(self) -> None:
        self.db = os.getenv('POSGRES_DB')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')


postgres = Postgres()

db_url = f"postgresql://{postgres.user}:{postgres.password}@{postgres.host}:{postgres.port}/{postgres.db}"

engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)

# engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()



class User(Base):
    __tablename__ = 'user'

    id = Column(UUID, primary_key=True, default=uuid4)
    fullname = Column(String, nullable=False)
    telegram_id = Column(BIGINT, nullable=False)
    auth = Column(Boolean, nullable=False)
    superuser = Column(Boolean, nullable=False)


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(UUID, primary_key=True, default=uuid4)
    subject = Column(String, nullable=False)
    type = Column(String, nullable=False)
    task = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)


Base.metadata.create_all(engine)