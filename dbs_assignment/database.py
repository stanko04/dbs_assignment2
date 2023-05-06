import os

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from dbs_assignment.config import settings

database_host = os.getenv("DATABASE_HOST")
database_port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")

engine = create_engine(f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}", echo=True, pool_pre_ping=True)

if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)




