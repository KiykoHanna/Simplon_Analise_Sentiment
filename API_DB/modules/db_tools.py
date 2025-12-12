# API_DB/modules/df_tools.py
from logger_config import logger 
import pandas as pd
import os 

import random
import pandas as pd
import numpy as np
from passlib.hash import argon2

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import func

from .models import Quote

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # папка API_DB
DATA_DIR = BASE_DIR.parent / "data"         # папка data на уровень выше
DATA_DIR.mkdir(exist_ok=True)               # создать, если не существует

DB_FILE_PATH = DATA_DIR / "DB_Citation.db"
DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"


# READ
def read_db(SessionLocal)->pd.DataFrame:
    session = SessionLocal()
    try:
        query = session.query(Quote)

        df = pd.read_sql(query.statement, session.bind, index_col="quote_id")
        df = df.fillna("NULL_REPLACEMENT_VALUE")
    except Exception as e:
        raise e
    finally:
        session.close()
    
    return df

# WRITE
def write_db(SessionLocal, obj: dict):
    session = SessionLocal()
    try:
        quote = Quote(quote_text=obj["text"])
        session.add(quote)  
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    

# INITTIALISATION
def initialize_db(SessionLocal):
    if os.path.exists(DB_FILE_PATH):
        logger.info("La base de données existe")
    else:
        logger.info(f"impossible de trouver le fichier {DB_FILE_PATH}")

        session = SessionLocal()

        quotes = [
            {"id": 1, "text": "La vie est belle"},
            {"id": 2, "text": "Carpe diem"}
        ]

        for q in quotes:
            write_db(SessionLocal, q)

        session.close()
        logger.info(f"le fichier {DB_FILE_PATH} a été créé")
    
# DELETE
def delete_db(SessionLocal, id: int):
    session = SessionLocal()
    try:
        quote = session.query(Quote).filter(Quote.quote_id == id).first()
        if quote:
            session.delete(quote)
            session.commit()
        else:
            raise ValueError(f"Quote with id {id} not found")
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        logger.info(f"le objet avec id: {id} a été suprimer")
