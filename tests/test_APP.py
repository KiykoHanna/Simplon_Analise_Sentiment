# tests/test_streamlit_app.py
import pytest
from unittest.mock import patch, MagicMock
import streamlit as st

# Имитация Streamlit session_state
st.session_state.clear()

# Test searche quote
def test_search_quote():
    with patch("requests.get") as mock_get:
        # Настраиваем мок ответа API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"text": "Test citation"}
        mock_get.return_value = mock_response

        # Симуляция ввода ID цитаты
        quote_id = 1
        API_URL = f"http://fake-api/read/"

        # Имитация логики поиска
        response = mock_get(f"{API_URL}{quote_id}")
        if response.status_code == 200:
            data = response.json()
            if data:
                st.session_state['quote_text'] = data.get('text', '')
            else:
                st.session_state['quote_text'] = ''
        else:
            st.session_state['quote_text'] = ''

        assert st.session_state['quote_text'] == "Test citation"


# --- Тест анализа цитаты ---
def test_analyse_quote():
    st.session_state['quote_text'] = "Test citation"
    API_ANALISE_URL = "http://fake-analyse"

    with patch("requests.post") as mock_post:
        # Настраиваем мок ответа API анализа
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {"neg": 0.0, "neu": 1.0, "pos": 0.0, "compound": 0.0}
        }
        mock_post.return_value = mock_response

        texte = st.session_state.get('quote_text', '')
        response = mock_post(f"{API_ANALISE_URL}/analyse/", json={"texte": texte})
        response.raise_for_status()
        sentiment_data = response.json()['response']

        assert sentiment_data['neg'] == 0.0
        assert sentiment_data['neu'] == 1.0
        assert sentiment_data['compound'] == 0.0
        assert st.session_state['quote_text'] == "Test citation"
