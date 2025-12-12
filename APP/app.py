import streamlit as st
import requests
import os 
import sys
from dotenv import load_dotenv 
from logger_config import logger

load_dotenv()

API_DB_URL =  f"http://{os.getenv('host')}:{os.getenv('port', '8000')}"

API_ANALISE_URL = f"http://{os.getenv('host')}:{os.getenv('port2', '8001')}"

st.title("Citations")
st.subheader("Bienvenue dans notre application de gestion et d'analyse de citations. Vous pouvez créer de nouvelles citations, consulter celles existantes dans la base de données et analyser leur sentiment grâce à notre outil d'intelligence artificielle.")




