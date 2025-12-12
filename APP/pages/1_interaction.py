import streamlit as st
import requests
import os 
import sys
from dotenv import load_dotenv 
from logger_config import logger

load_dotenv()

# --- path ---
API_DB_URL =  f"http://{os.getenv('host')}:{os.getenv('port', '8000')}"
API_ANALISE_URL = f"http://{os.getenv('host')}:{os.getenv('port2', '8001')}"

# --- choisir les modes ---
st.title("Le Base de donnees de citations")

mode = st.radio("Choisissez le mode:",
         ("Créer une citation",
          "Lire la base de données",
          "Choisir une citation aléatoire",
          "Choisir une citation par ID",
          "Supprimer une citation par ID")
          )


# --- functionalite ---
if mode == "Créer une citation":

    # get sitation
    quote_text = st.text_area("Entrez votre citation ici :")

    if quote_text.strip(): 
        quote_text = quote_text.strip()
        st.session_state['quote_text'] = quote_text

        # logging
        logger.info(f"Nouvelle citation entrée par l'utilisateur : {quote_text}")
        st.success("Citation enregistrée dans l'état de session.")
        st.info(quote_text)

        # Envoyer soulement une fois
        if 'quote_sent' not in st.session_state or not st.session_state['quote_sent']:
            try:
                payload = {"text": st.session_state['quote_text']}
                response = requests.post(f"{API_DB_URL}/write/", json=payload)
                response.raise_for_status()

                if response.status_code == 200:
                    st.success("Citation ajoutée avec succès dans la base de données.")
                    st.session_state['quote_sent'] = True  # помечаем как отправлено
                    logger.info(f"Citation ajoutée dans la DB via API : {st.session_state['quote_text']}")
                else:
                    st.error(f"Erreur API lors de l'ajout : {response.status_code}")
                    logger.error(f"Erreur API lors de l'ajout de la citation : {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors de l'ajout de la citation : {e}")
                logger.error(f"Erreur API lors de l'ajout de la citation : {e}")

    else:
        st.warning("Veuillez entrer une citation valide.")
        st.session_state['quote_text'] = ""
        logger.warning("L'utilisateur a tenté d'enregistrer une citation vide.")

elif mode == "Lire la base de données":
    st.session_state['quote_text'] = ""
    st.subheader("Toutes les citations de la base de données")

    try:
        # GET roquet pour lire tous
        response = requests.get(f"{API_DB_URL}/read/")
        response.raise_for_status() 

        data = response.json()
        if data:
            # affichage
            for item in data:
                st.info(f"ID {item['id']}: {item['text']}")
            
            logger.info(f"Lecture de la DB réussie. Nombre de citations: {len(data)}")
        else:
            st.warning("La base de données est vide.")
            logger.warning("Tentative de lecture: base de données vide.")

    except requests.exceptions.RequestException as e:
        st.error(f"Impossible de se connecter à l'API : {e}")
        logger.error(f"Erreur de connexion à l'API lors de la lecture de la DB : {e}")


elif mode == "Choisir une citation aléatoire":

    st.subheader("Citation Aléatoire")
    # afficher une citation aléatoire
    API_URL =  API_DB_URL + "/read/random/"
    if st.button("obetnir une citation aléatoire:"):
        try : 
            response = requests.get(API_URL)

            if response.status_code == 200:
                result = response.json()
                st.session_state['quote_text'] = result.get('text', '')

                if result:
                    st.success(f"Citation avec ID {result.get('id', 'N/A')}")
                    st.info(result.get('text', 'text non trouvé'))
                else:
                    st.warning("Aucune citation disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")


        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")

elif mode == "Choisir une citation par ID":

    # afficher une citation par ID
    st.subheader("Citation par ID")
    API_URL =  API_DB_URL + "/read/"
    # selectionne l'ID
    with st.form("search_by_id"):
        quote_id = st.number_input("Entrez l'ID de la citation:", 
                                   min_value=1, step=1)
        submitted = st.form_submit_button("Rechercher")

    if submitted:
        # appel la route /read/id
        try : 
            response = requests.get( API_URL + str(quote_id) )
        # le reste est pareil
            if response.status_code == 200:
                result = response.json()
                st.session_state['quote_text'] = result.get('text', '')
                if result:
                    st.success(f"Citation avec ID {quote_id}")
                    st.info(result.get('text', 'text non trouvé'))
                else:
                    st.warning(f"La citation {quote_id} n'est pas disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")


        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")

elif mode == "Supprimer une citation par ID":
    st.subheader("Suppression d'une citation")
    
  
    quote_id = st.number_input("Entrez l'ID de la citation à supprimer:", min_value=1, step=1)
    
    if st.button("Supprimer la citation"):
        if not quote_id:
            st.warning("Veuillez entrer un ID valide.")
        else:
            try:
                response = requests.delete(API_DB_URL + "/delete/" + str(quote_id))
                response.raise_for_status()
                result = response.json()

                st.session_state['quote_text'] = result.get('quote_text', '')
                st.success(f"Citation supprimée avec ID {quote_id}")


            except requests.exceptions.HTTPError as e:
                st.error(f"Erreur de l'API lors de la suppression : {e}")
            except requests.exceptions.ConnectionError:
                st.error(f"Impossible de se connecter à l'API à {API_DB_URL}")


if st.session_state['quote_text']:  # si il y a le text dans une session_state
    st.markdown("---")
    st.subheader("Analyse de la citation")
    if st.button("Analiser"):
        
        try:
            # Prendre le text pour session_state
            texte = st.session_state.get('quote_text', '')
            logger.info(f"Texte à analyser: {texte}")
            if not texte:
                st.warning("Aucune citation sélectionnée pour l'analyse.")
            else:
                payload = {"texte": texte}
                response = requests.post(f"{API_ANALISE_URL}/analyse/", json=payload)
                response.raise_for_status()
                sentiment = response.json()

                # recevoir le result d'analise
                sentiment_data = sentiment['response']
                st.write(f"_{texte}_")
                st.write(f"Polarité négative : {sentiment_data['neg']}")
                st.write(f"Polarité neutre : {sentiment_data['neu']}")
                st.write(f"Polarité positive : {sentiment_data['pos']}")
                st.write(f"Score composé : {sentiment_data['compound']}")

                # Interpretation compound
                if sentiment_data['compound'] >= 0.05:
                    st.write("Sentiment global : Positif 😀")
                elif sentiment_data['compound'] <= -0.05:
                    st.write("Sentiment global : Négatif 🙁")
                else:
                    st.write("Sentiment global : Neutre 😐")

                logger.info(f"Résultats affichés pour citation {texte}: {sentiment}")

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"Erreur API lors de l'analyse : {http_err}")
            st.error(f"Erreur API lors de l'analyse : {http_err}")
        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_ANALISE_URL}")
            logger.error(f"ERREUR : Impossible de se connecter à l'API à {API_ANALISE_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")