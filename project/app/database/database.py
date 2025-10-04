import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

#Loads variables from .env
load_dotenv()

#Creates database engine
engine = create_engine("postgresql://{user}:{password}@{db_host}:5432/{database}".format(
    user = os.getenv("POSTGRESQL_USER"),
    password = os.getenv("POSTGRESQL_PASSWORD"),
    database = os.getenv("POSTGRESQL_DATABASE"),
    db_host = os.getenv("DATABASE_HOST")
))

#Creates communication with database using binded engine
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

#Base model for databes models
Base = declarative_base()

#Defines collection of database tables and models for app to use
metadata = Base.metadata

#Attaches a query property to all model classes
Base.query = db_session.query_property()

#Creates tables in database using models metadata
def init_db():
    Base.metadata.create_all(engine)
    