import pytest
from quotes import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test that the homepage loads successfully and contains expected text"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Daily Inspiration" in response.data  # Checks if your title is on the page
