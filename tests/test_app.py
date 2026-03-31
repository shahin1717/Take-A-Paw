# tests/test_app.py
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import create_app
from app.db import db

@pytest.fixture
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    }
    
    app = create_app(test_config=test_config)
    
    with app.app_context():
        db.create_all()
        
    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def init_database(app):
    with app.app_context():
        from app.models import Pet, User
        
        user = User(
    display_name="Test User",
    email="test@example.com",
    username="testuser",        # required if your table has NOT NULL
    password_hash="testpass",   # required if your table has NOT NULL
    public_contact=True         # keep as 1 / True
)
    
        db.session.add(user)
        
        pets = [
            Pet(
                name="Test Dog", species="Dog", breed="Golden Retriever", age="2 years",
                gender="Male", location="Test Shelter", description="Friendly test dog",
                image="https://example.com/dog.jpg", adopted=False
            ),
            Pet(
                name="Test Cat", species="Cat", breed="Siamese", age="1 year",
                gender="Female", location="Test Shelter", description="Playful test cat", 
                image="https://example.com/cat.jpg", adopted=False
            )
        ]
        for pet in pets:
            db.session.add(pet)
        
        db.session.commit()
@pytest.fixture
def client(app):
    return app.test_client()



def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['status'] == 'ok'

def test_home_page(client, init_database):
    response = client.get('/')
    assert response.status_code == 200
    assert b'swipe' in response.data.lower() or b'pet' in response.data.lower()


def test_quiz_page(client, init_database):
    response = client.get('/quiz')
    assert response.status_code == 200

def test_api_status(client, init_database):
    response = client.get('/api/status')
    assert response.status_code == 200
    assert response.is_json

def test_pets_api(client, init_database):
    response = client.get('/pets')
    assert response.status_code == 200
    assert response.is_json

def test_quiz_results(client, init_database):
    quiz_data = {
        "home_type": "apartment",
        "activity_level": "medium", 
        "experience": "some",
        "time_commitment": "1_3_hours",
        "family_situation": "no"
    }
    
    response = client.post('/quiz/results', 
                         json=quiz_data,
                         content_type='application/json')
    
    assert response.status_code == 200
    assert response.is_json

def test_404_page(client):
    response = client.get('/nonexistent-page')
    assert response.status_code == 404