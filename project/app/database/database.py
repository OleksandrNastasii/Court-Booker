import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

load_dotenv()
#from ..config.config import DB_route
print(os.getenv("DATABASE_HOST"))
engine = create_engine("postgresql://{user}:{password}@{db_host}:5432/{database}".format(
    user = os.getenv("POSTGRESQL_USER"),
    password = os.getenv("POSTGRESQL_PASSWORD"),
    database = os.getenv("POSTGRESQL_DATABASE"),
    db_host = os.getenv("DATABASE_HOST")
))
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(engine)
    