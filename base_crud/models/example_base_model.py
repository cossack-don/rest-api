from sqlalchemy.types import Integer, String
from sqlalchemy import  Column
from database import Base


class Base_Model_CRUD(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    title = Column(Integer)