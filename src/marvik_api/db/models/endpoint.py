from sqlalchemy import (
    Column,
    Integer,
    String,
)
from marvik_api.db.base_class import Base


class Endpoint(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    count = Column(Integer, nullable=False, default=0)
