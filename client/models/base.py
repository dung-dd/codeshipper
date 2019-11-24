from sqlalchemy import create_engine, Sequence, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSequence
from os import path
from tunnel.tunnel import app

Base = declarative_base()

# db_file_path = path.join( path.dirname(path.realpath(__file__)), "database", "db.sqlite" )
# engine = create_engine("sqlite:///"+db_file_path, echo=False)
engine = create_engine(app.config.get("SQLALCHEMY_DATABASE_URI"), echo=False)
