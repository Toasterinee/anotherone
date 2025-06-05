# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://fastapi_user:053089DT@localhost/myfastapidb"

# SQLALCHEMY_DATABASE_URL = "postgresql://fastapi_user:tETCE5nErrF3dHgDel5NVD9jjbn5qaLA@dpg-d0qababe5dus739d7dug-a.oregon-postgres.render.com/myfastapidb_dbyp"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()