# Projet

## dans l'ideal une appp
1. conception
2. developpement / recherche (notebook)
3. production (code et test)
4. surveillance (monitoring)

# Development / recherche

- choisir une model d'IA
- telecharger le model d'IA
- teste norte model dans une notebook
- Creer et teste db_tools et models d'ORM

# Production

## Les étapes du projet
- creation d'un dossier de travail
- creation des fichiers
  - .venv
  - .env
  - README.md
  - .gitignore
  - logger_config.py
- separation de l' architecture
  - dossiers
    - APP
    - API_DB
    - API_IA
  - architecture en couche
    - separation des modules
    - separation des models
    - separation des donnees

## Logique / étapes

### **Application (APP)**
- setup / preparation de l'application
  - importation des bibliothèques
  - chargement des variables d’environnement
  - configuration du logger
- création des pages de l’application
  - accueil
    - test de connexion ("ping") avec les API
    - affichage d’un message dynamique (API OK / ERREUR)
    - présentation brève de l’application
  - interaction
    - créer une citation
    - lire la base des citations
    - lire une citation par ID
    - lire une citation randome
    - supprimer une citation
    - analyser une citation (IA)
- appels POST/GET/DELETE vers les routes de l’API
- récupération et affichage des résultats
- gestion des exceptions (timeout, 404, connexion refusée)
- maintien des données dans st.session_state pour éviter les rafraîchissements intempestifs

## **API de base de donees (API_DB)**

- importation des bibliothèques
- chargement des variables d’environnement
- définition des modèles Pydantic
    - QuoteRequest
    - QuoteResponse
    - QuoteID
- initialisation de la base de données
    - création automatique des tables avec SQLAlchemy
    - définition du modèle ORM Quote
- création de l’objet application FastAPI
- définition des routes
    - route principale : GET / → {"message": "API DB OK"}
    - créer une citation : POST /write/
    - lire toutes les citations : GET /read/
    - lire une citation par ID : GET /read/{id}
    - lire une citation random : GET /read/random/
    - supprimer une citation : DELETE /delete/
- logique interne
    - ouvrir une session DB
    - exécuter l’opération
    - commit / rollback
    - fermer la session
- gestion des exceptions
- activation du serveur (uvicorn fastapi_DB:app)

## **API d’analyse (API_IA)**

- importation des bibliothèques 
- chargement du modèle d'analyse (SentimentIntensityAnalyzer)
- définition des modèles Pydantic (Text, SentimentOutput, Response)
- création de l’API FastAPI
- définition des routes
    - route principale
    - analyse d’un texte (POST /analyze/)
- formatage de la réponse
- gestion des erreurs (modèle indisponible, input vide)

## Architecture
.
├── APP
│   ├── app.py
│   ├── pages
│   │   ├── accueil.py
│   │   └── interaction.py

│
├── API_DB
│   ├── data
│   │   └── DB_Citation.db
│   ├── modules
│   │   ├── db_tools.py
│   │   └── models.py
│   └── fastapi_DB.py
|
├── API_IA
│   └── fastapi_IA.py
|
├── tests
│   └── fastapi_IA.py
├── .env
├── logger_config.py
├── README.md
└── requirements.txt


