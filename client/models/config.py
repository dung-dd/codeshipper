from .base import Base, engine
from sqlalchemy import Column, String

class Config(Base):
    __tablename__ = "config"

    key = Column(String, primary_key=True)
    value = Column(String)
