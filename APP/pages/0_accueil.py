import streamlit as st
import requests
import os 
import sys
from dotenv import load_dotenv 

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

from logger_config import logger

load_dotenv()

API_DB_URL =  f"http://{os.getenv('host')}:{os.getenv('port', '8000')}"

API_ANALISE_URL = f"http://{os.getenv('host')}:{os.getenv('port2', '8001')}"


st.subheader("Vérification de l'API")

# --- Le Bouton 1---
if st.button("Ping l'API (Route / API_DB_URL)"):
    try:
        # 1. Requête GET vers la route principale
        response = requests.get(API_DB_URL)

        # 2. Si il y a un résultat alors l'afficher
        if response.status_code == 200:
            st.success("Connexion réussie à l'API FastAPI !")
            st.code(f"Statut HTTP : {response.status_code}")

            st.json(response.json())
        else:
            st.error(f"L'API a répondu avec une erreur. Statut : {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error(f"ERREUR : Impossible de se connecter à l'API à {API_DB_URL}")
        st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")

# --- Le Bouton 2 ---
if st.button("Ping l'API (Route /analyse/)"):
    try:
        test_payload = {"texte": "Bonjour"}  # petit texte de test
        
        response = requests.post(f"{API_ANALISE_URL}/analyse/", json=test_payload)

        if response.status_code == 200:
            st.success("Connexion réussie à l'API d'analyse !")
            st.code(f"Statut HTTP : {response.status_code}")
            st.json(response.json())
        else:
            st.error(f"L'API a répondu avec une erreur. Statut : {response.status_code}")
            st.text(response.text)

    except requests.exceptions.ConnectionError:
        st.error(f"ERREUR : Impossible de se connecter à l'API à {API_ANALISE_URL}")
        st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        st.error(f"Erreur inattendue: {e}")
