from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session

from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# создаем базовый класс для моделей
Base = declarative_base()


# создаем модель, объекты которой будут храниться в бд
class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )


# создаем таблицы
Base.metadata.create_all(bind=engine)

# создаем сессию подключения к бд
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

# создаем объект Person для добавления в бд
# tom = Person(name="Tom", age=38)
# db.add(tom)  # добавляем в бд
# db.commit()  # сохраняем изменения

# print(tom.id)  # можно получить установленный id

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class ManTemplate(BaseModel):
    name: str
    age: float

@app.get("/")
def read_root():
    people = {
        'Robin': 24,
        'Odin': 26,
        'David': 25
    }

    return [people,people]


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/items/{item_id}")
def create_item( item: ManTemplate):
    tom = Person(name=item.name, age=item.age)
    db.add(tom)  # добавляем в бд
    db.commit()  # сохраняем изменения
    return {"item_name": item.name, "item_age": item.age}

@app.delete("/items/{item_id}")
def delete_item_by_id(item_id: int):
    try:
        delete_item = db.query(Person).filter(Person.id == item_id).first()
        db.delete(delete_item)  # добавляем в бд
        db.commit()  # сохраняем изменения
        return {"id_deleted_item": item_id}
    except:
        raise HTTPException(status_code=422, detail=f"Данная запись с id {item_id} уже удалена.")