from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# engine = create_engine("postgresql://postgres:spartaktrnava38@host.docker.internal:5432/dbs", echo=True, pool_pre_ping=True)
engine = create_engine("postgresql://postgres:spartaktrnava38@localhost:5432/dbs", echo=True, pool_pre_ping=True)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
