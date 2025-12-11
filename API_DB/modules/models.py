#API_DB/modules/models.py

# import
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


# Creation structure de base
Base = declarative_base()

#Class Sitation
class Quote(Base):
    __tablename__ = "quotes"
    quote_id = Column(Integer, primary_key=True)
    quote_text = Column(String)