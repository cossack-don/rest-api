from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy import text, select, insert, delete, update
from sqlalchemy.orm import Session
from database import get_db
from models.example_join import Model_Table_ONE, Model_Table_TWO
from schems.example_join import Schema_Model_Table_ONE
from base_crud.schems.example_base_schema import Base_Schema_CRUD
from base_crud.models.example_base_model import Base_Model_CRUD

app = FastAPI()


#GET - GET_ALL_ITEMS
@app.get("/base_crud", response_model=List[Base_Schema_CRUD])
def get_all(bd: Session = Depends(get_db)):
    q = select(Base_Model_CRUD.id, Base_Model_CRUD.name, Base_Model_CRUD.age, Base_Model_CRUD.title)
    result = bd.execute(q).all()

    return result


# GET - GET_BY_ID_ITEM
@app.get("/base_crud/{item_id}")
def get_by_id(bd: Session = Depends(get_db), id=int):
    q = select(Base_Model_CRUD)
    q = q.where(Base_Model_CRUD.id == id)
    result = bd.scalar(q)

    return result


# POST - ADD NEW ITEM IN BD IN LIST
@app.post("/base_crud")
def add_item_in_list(bd: Session = Depends(get_db), name=str, age=int):
    q = insert(Base_Model_CRUD).values(name=name, age=age)
    result = bd.execute(q)
    bd.commit()

    return result


# PUT - Change data in item by ID
@app.put("/base_crud/{item_id}")
def add_item_in_list(bd: Session = Depends(get_db), id=int, name=str, age=int):
    q = update(Base_Model_CRUD).where(Base_Model_CRUD.id == id).values(name=name, age=age)
    result = bd.execute(q)
    bd.commit()

    return result

# DELETE - Delete item by ID
@app.delete("/base_crud/{item_id}")
def add_item_in_list(bd: Session = Depends(get_db), id=int):
    q = delete(Base_Model_CRUD)
    q = q.where(Base_Model_CRUD.id == id)
    result = bd.execute(q)
    bd.commit()

    return result



# example join
@app.get("/base_join",response_model=List[Schema_Model_Table_ONE])
def get_all(bd: Session = Depends(get_db)):
        q = select(Model_Table_TWO.id, Model_Table_ONE.category_name).join(Model_Table_ONE,  Model_Table_ONE.id == Model_Table_TWO.category_id)
        result = bd.execute(q).all()

        return result
        # return [
        #     dict(r._mapping) for r in result
        # ]
