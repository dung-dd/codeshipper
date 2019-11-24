# coding: utf-8

from .base import Base, engine
from sqlalchemy import Sequence, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.schema import CreateSequence


class Updating (Base):
    __tablename__ = "updating"

    id = Column(Integer, Sequence("updating_id_seq", increment=True, start=1), primary_key=True)
    project_id = Column(String)
    project_name = Column(String)
    version = Column(String, unique=True)
    updating_type = Column(String) # config, source_code
    update_change = Column(String)
    created_time = Column(String)
