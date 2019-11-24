from .base import Base, engine
from sqlalchemy import Sequence, Column, Integer, String
from sqlalchemy.schema import CreateSequence

CreateSequence("project_id_seq", bind=engine)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, Sequence("project_id_seq", increment=True, start=1), primary_key=True, index=True)
    name = Column(String)
    code = Column(String, index=True, unique=True)
    version = Column(String)
    server = Column(String)
    data_path = Column(String)
    config_file_path = Column(String)
    source_code_path = Column(String)
    created_time = Column(String)
    updated_time = Column(String)
