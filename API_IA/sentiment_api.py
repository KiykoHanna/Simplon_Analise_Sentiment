# Simplon/API_IA/sentiment_api.py

#import
from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger

app = FastAPI()
sia = SentimentIntensityAnalyzer()

class Texte(BaseModel):
    texte: str
    
class SentimentOutput(BaseModel):
    neg: float
    neu: float
    pos: float
    compound: float

class Response(BaseModel):
    response: SentimentOutput


@app.post("/analyse/", response_model=Response)
async def analyse(texte_obj: Texte):
    logger.info(f"Analyse du texte: {texte_obj.texte}")
    try:
        sentiment = sia.polarity_scores(texte_obj.texte)
        logger.info(f"Résultats: {sentiment}")

        # ОБЯЗАТЕЛЬНО возвращаем dict с ключом "response"
        return {"response": sentiment}

    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))