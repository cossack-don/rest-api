from typing import List, Optional
from fastapi import FastAPI, Depends
from sqlalchemy.types import Integer, String
from sqlalchemy import text, Column, select, insert, delete, update, join
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Base

#
# with engine.connect() as connection:
#     sql = text('SELECT * FROM test')
#     result = connection.execute(sql)
    # # print(result)
    # for row in result:
    #     print(row)

app = FastAPI()

# /////
class core_join(Base):
    __tablename__ = "core_join"

    id = Column(Integer, primary_key=True)
    category_name = Column(String)

class join_1(Base):
    __tablename__ = "join_1"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer)

# ///////

class ItemsTwo(Base):
    __tablename__ = "test2"

    id = Column(Integer, primary_key=True)
    options = Column(String)
    title = Column(Integer)

class Items(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    title = Column(Integer)


class SchemaItems(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    age: Optional[int] = None
    title: Optional[int] = None

    class Config:
        orm_mode = True

class SchemaItemsTwo(BaseModel):
    id: int
    options: Optional[str] = None
    title: Optional[str] = None

    class Config:
        orm_mode = True


class Test1(BaseModel):
    id: int
    category_name: Optional[str] = None

    class Config:
        orm_mode = True

#GET - GET_ALL_ITEMS
@app.get("/test", response_model=List[SchemaItems])
def get_all(bd: Session = Depends(get_db)):

    q = select(Items.id)

    result = bd.execute(q).all()


    # with engine.connect() as connection:
    #     sql = text('SELECT * FROM test')
    #     result = connection.execute(sql).all()
    #     print(result)
    return result


# GET - GET_BY_ID_ITEM
@app.get("/test/{item_id}")
def get_by_id(bd: Session = Depends(get_db), id=int):
    q = select(Items)
    q = q.where(Items.id == id)

    result = bd.scalar(q)
    print(result)
    return result


# POST - ADD NEW ITEM IN BD IN LIST
@app.post("/test")
def add_item_in_list(bd: Session = Depends(get_db), name=str, age=int):
    q = insert(Items).values(name=name, age=age)
    result = bd.execute(q)
    bd.commit()

    return result


# PUT - Change data in item by ID
@app.put("/test/{item_id}")
def add_item_in_list(bd: Session = Depends(get_db), id=int, name=str, age=int):
    q = update(Items).where(Items.id == id).values(name=name, age=age)
    result = bd.execute(q)
    print(result)
    bd.commit()

    return result

# DELETE - Delete item by ID
@app.delete("/test/{item_id}")
def add_item_in_list(bd: Session = Depends(get_db), id=int):
    q = delete(Items)
    q = q.where(Items.id == id)
    result = bd.execute(q)
    bd.commit()

    return result



# ///////////
@app.get("/test2",response_model=List[Test1])
def get_all(bd: Session = Depends(get_db)):

        q = select(join_1.id, core_join.category_name).join(core_join,  core_join.id == join_1.category_id)
        result = bd.execute(q).all()

        return result
        # return [
        #     dict(r._mapping) for r in result
        # ]
