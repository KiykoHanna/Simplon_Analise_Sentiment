import streamlit as st
import requests
import os 
from dotenv import load_dotenv 
from loguru import logger

load_dotenv()

API_ROOT_URL =  f"http://{os.getenv('host')}:{os.getenv('port', '8000')}"

API_ANALISE_URL = "http://127.0.0.1:8001"    # порт API_DB для read

st.title("Lire une citation")

# afficher une citation par ID
st.subheader("Citation par ID")
API_URL =  API_ROOT_URL + "/read/"
# selectionne l'ID
# un formulaire
with st.form("search_by_id"):
    quote_id = st.number_input("Entrez l'ID de la citation:", 
                                min_value=1, step=1)
    submitted = st.form_submit_button("Rechercher")
# connaitre toutes les id
# selectionne l'id
# После поиска цитаты
if submitted:
    try:
        response = requests.get(API_URL + str(quote_id))
        if response.status_code == 200:
            data = response.json()
            if data:
                st.success(f"Citation avec ID {quote_id}")
                st.info(data.get('text', 'text non trouvé'))
                st.session_state['quote_text'] = data.get('text', '')  # сохраняем текст
                # st.balloons()
            else:
                st.warning(f"La citation {quote_id} n'est pas disponible dans la DB")
                st.session_state['quote_text'] = ''
        else:
            st.error(f"Erreur de l'API avec le code {response.status_code}")
            st.session_state['quote_text'] = ''

    except requests.exceptions.ConnectionError:
        st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
        st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")
        st.session_state['quote_text'] = ''

if st.button("Analiser"):
    
    try:
        # Получаем текст цитаты из session_state
        texte = st.session_state.get('quote_text', '')
        logger.info(f"Texte à analyser: {texte}")
        if not texte:
            st.warning("Aucune citation sélectionnée pour l'analyse.")
        else:
            payload = {"texte": texte}
            response = requests.post(f"{API_ANALISE_URL}/analyse/", json=payload)
            
            # Проверка кода ответа
            response.raise_for_status()
            sentiment = response.json()
            # Получаем результат анализа
            sentiment_data = sentiment['response']
            st.write(f"Polarité négative : {sentiment_data['neg']}")
            st.write(f"Polarité neutre : {sentiment_data['neu']}")
            st.write(f"Polarité positive : {sentiment_data['pos']}")
            st.write(f"Score composé : {sentiment_data['compound']}")


            # Интерпретация compound
            if sentiment_data['compound'] >= 0.05:
                st.write("Sentiment global : Positif 😀")
            elif sentiment_data['compound'] <= -0.05:
                st.write("Sentiment global : Négatif 🙁")
            else:
                st.write("Sentiment global : Neutre 😐")

            # Логирование
            logger.info(f"Résultats affichés pour citation {quote_id}: {sentiment}")

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erreur API lors de l'analyse : {http_err}")
        st.error(f"Erreur API lors de l'analyse : {http_err}")
    except requests.exceptions.ConnectionError:
        st.error(f"ERREUR : Impossible de se connecter à l'API à {API_ANALISE_URL}")
        logger.error(f"ERREUR : Impossible de se connecter à l'API à {API_ANALISE_URL}")
        st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")



