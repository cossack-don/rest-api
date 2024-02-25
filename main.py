from typing import List, Optional
from fastapi import FastAPI, Depends
from sqlalchemy.types import Integer, String
from sqlalchemy import create_engine, text, Column, select, insert, delete, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

NAME_BD = os.getenv('NAME_BD')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
SERVER_NAME = os.getenv('SERVER_NAME')




SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{SERVER_NAME}/{NAME_BD}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#
# with engine.connect() as connection:
#     sql = text('SELECT * FROM test')
#     result = connection.execute(sql)
    # # print(result)
    # for row in result:
    #     print(row)

app = FastAPI()

class Items(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class SchemaItems(BaseModel):
    id: int
    name: Optional[str] = None
    age: Optional[int] = None

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



#
# mydb = mysql.connector.connect(
#   host="server228.hosting.reg.ru",
#   user="u1704954_fastapi",
#   password="u1704954_fastapi",
#   database="u1704954_fastapi",
# )


#
# @app.get("/test")
# def get_list_items():
#     cursor = mydb.cursor()
#     cursor.execute("SELECT * FROM test")
#     result = cursor.fetchall()
#     return {"test": result}
#
# @app.get("/test/{id}")
# def get_one_item(id: int):
#     cursor = mydb.cursor()
#     cursor.execute(f"SELECT * FROM test WHERE id = {id}")
#
#     result = cursor.fetchone()
#     return {"test": result}
#
# @app.put("/test/{id}")
# def update_item(id:int, name:str, age:int):
#     print(type(age))
#     cursor = mydb.cursor()
#     # почему то число принимает в name норм а стрингу нет
#
#     # sql = "UPDATE test SET name = {d} WHERE id = 2"
#
#     sql = "UPDATE test SET age = %s, name = %s WHERE id = %s"
#     values = (age, name, id)
#
#     cursor.execute(sql, values)
#     mydb.commit()
#     return {"test": f"update {id}"}
#
# # Add a new item
# @app.post("/test")
# def add_item(name: str, age: int):
#     cursor = mydb.cursor()
#     sql = "INSERT INTO test (name, age) VALUES (%s, %s)"
#     val = (name, age)
#     cursor.execute(sql, val)
#     mydb.commit()
#     return {"message": "Item added successfully"}
#
# @app.delete("/test/{id}")
# def delete_item(id: int):
#     cursor = mydb.cursor()
#     cursor.execute(f"DELETE FROM test WHERE id = {id}")
#     mydb.commit()
#     return {"message": "Item deleted successfully"}
#