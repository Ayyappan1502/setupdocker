from app import app

# Test the home route
def test_home():
    response = app.test_client().get('/')
    assert response.status_code == 200 
    assert response.data == b"Welcome to the Home Page!"