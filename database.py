import os
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

NAME_BD = os.getenv('NAME_BD')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
SERVER_NAME = os.getenv('SERVER_NAME')


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{SERVER_NAME}/{NAME_BD}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()