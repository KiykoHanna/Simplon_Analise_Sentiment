import pytest
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from API_DB.modules.db_tools import write_db, read_db
from API_DB.modules.models import Base, Quote


# FIXTURE

## create engine
@pytest.fixture(scope="module")
def test_engine():
    """ Create engine """
    return create_engine("sqlite:///:memory:")


## create DB
@pytest.fixture(scope="module")
def setup_db(test_engine):
    """ Create table """
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


## create DB session
@pytest.fixture(scope="function")
def SessionTest(test_engine, setup_db):
    """Create class Session"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    yield SessionLocal

@pytest.fixture(scope="function")
def db_session(SessionTest, test_engine, setup_db):
    """ Yeld DB Session"""
    connection = test_engine.connect()
    transaction = connection.begin()

    session = SessionTest(bind=connection)

    yield session

    #clean
    session.close()
    transaction.rollback()
    connection.close()


# MOCK
## OVERRIDE SESSION LOCAL
def override_get_db_session(monkeypatch, db_session):
    """ Mock get db session """
    def mock_get_db_session():
        return db_session
    monkeypatch.setattr("API_DB.modules.db_tools.get_db_session", mock_get_db_session)

# TEST write db
def test_add_and_read_quote(SessionTest):
    text = {"text": "test"}
    
    write_db(SessionTest, text)

    df2 = read_db(SessionTest)
    citation = df2.iloc[0]["quote_text"]
    assert not df2.empty
    assert citation == text["text"]
