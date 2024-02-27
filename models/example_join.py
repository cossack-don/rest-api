from database import Base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String


class Model_Table_ONE(Base):
    __tablename__ = "core_join"

    id = Column(Integer, primary_key=True)
    category_name = Column(String)


class Model_Table_TWO(Base):
    __tablename__ = "join_1"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer)