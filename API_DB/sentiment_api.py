# Simplon/API_DB/sentiment_api.py

from fastapi import FastAPI, HTTPException
import uvicorn
import os 
import pandas as pd
from dotenv import load_dotenv 
from pydantic import BaseModel, Field

from .modules.db_tools import read_db, write_db, initialize_db
from typing import List, Annotated

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import func



from pathlib import Path

# Папка, где лежит sentiment_api.py
BASE_DIR = Path(__file__).resolve().parent  # API_DB

# Папка data внутри API_DB
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # создаём папку, если нет

# Полный путь к файлу базы
DB_FILE_PATH = DATA_DIR / "DB_Citation.db"
DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"


import random
load_dotenv()

# modèles pydantic
class QuoteRequest(BaseModel):
    text : str = Field(min_length=1, description="donnez un texte pour la citation")

class QuoteResponse(BaseModel):
    id : int
    text : str



# --- SQLAlchemy models ---
Base = declarative_base()

# --- Database initialization ---
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# creation si besoin de la base de données
initialize_db(SessionLocal)

# --- Configuration ---
app = FastAPI(title="API")

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

@app.post("/insert/", response_model= QuoteResponse)
def insert_quote(quote : QuoteRequest):
    """Insère une nouvelle citation"""

    # 1. trouver le dernier id dans le csv
    df = read_db(SessionLocal)

    # 2. donne un id a ma citation
    if df.empty :
        new_id = 1
    elif df.index.max() <= 0 :
        new_id = 1
    else :
        new_id = 1 + df.index.max()

    obj = {"id": new_id, "text": quote.text}

    # 3.1 créer la nouvelle ligne
    write_db(SessionLocal, obj)

    # 4. pour la confirmation je vais envoyer à l'application
    # la citation avec son id
    return obj

@app.get("/read/", response_model=List[QuoteResponse])
def read_all_quotes():
    df = read_db(SessionLocal)
    df = df.reset_index().rename(columns={
    'quote_id': 'id',
    'quote_text': 'text'
})
    return df.to_dict('records')


@app.get("/read/{id}", response_model=QuoteResponse)
def read_specific_quotes(id : int):
    # il me faut toutes les citations pour les connaitres
    df = read_db(SessionLocal)
    # filtre par l'id concerné
    if id not in df.index:
        raise HTTPException(status_code=404, detail=f"Citation avec ID {id} non trouvée")
    quote_data = {}
    quote_data["text"] = df.loc[id]["quote_text"]
    quote_data['id'] = id
    # retourne les résultats
    
    return quote_data

@app.get("/read/random/", response_model=QuoteResponse)
def read_random_quotes():
    # il me faut toutes les citations pour les connaitres
    df = read_db(SessionLocal)
    # filtre par l'id concerné  
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Citation avec aléatoire non trouvée")
    
    random_id = random.choice(df.index)
    quote_data = {}
    quote_data["text"] = df.loc[random_id]["quote_text"]
    quote_data['id'] = random_id
    # retourne les résultats
    return quote_data

if __name__ == "__main__":
    # 1 - on récupère le port de l'API
    try:
        print("Hello")
        port_str: str = os.getenv("FAST_API_PORT", "8000")
        url: str = os.getenv("API_BASE_URL", "127.0.0.1")
        port: int = int(port_str)
        print(port)
    except ValueError:
        print("ERREUR")
        port = 8080

    # 2 - On lance uvicorn
    uvicorn.run(
        "main:app", 
        host = url,
        port = port, 
        reload = True
    )


engine.dispose()