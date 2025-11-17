def test_home_redirect(client):
    response = client.get("/")
    assert response.status_code == 302  # redirect
    assert "/login" in response.location

def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

def test_signup_page(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_api_signup(client):
    response = client.post("/api/signup", json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Tester"
    })
    assert response.status_code == 201
    assert response.json["message"] == "ok"
