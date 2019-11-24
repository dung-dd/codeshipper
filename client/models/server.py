# coding: utf-8

from .base import Base, engine
from sqlalchemy import Sequence, Column, Integer, String
from sqlalchemy.schema import CreateSequence

CreateSequence("server_id_seq", bind=engine)

class Server(Base):
    __tablename__ = "server"

    id = Column(Integer, Sequence("server_id_seq", increment=True, start=1), primary_key=True)
    name = Column(String)
    super_secret = Column(String)
    created_time = Column(String)
    updating = Column(String)
