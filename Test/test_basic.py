import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Welcome" in rv.data or b"Hello" in rv.data  # Adjust according to your homepage content

def test_metrics_endpoint(client):
    rv = client.get('/metrics')
    assert rv.status_code == 200
    assert b"python_gc_objects_collected_total" in rv.data
