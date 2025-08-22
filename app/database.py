from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings
                            #'postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_pw}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # moteur qui fait le lien entre python et pstsql

SessionLocal = sessionmaker(   # créé un session (voiture qui utilise la route de engin)
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()   # classe mere qui gere la mise en tableau / Base.metadata contient les classes filles

# dependancy pour db:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
