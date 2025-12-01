import json

def test_api_signup(client):
    payload = {"email": "test@example.com", "password": "password", "name": "Test"}
    res = client.post("/api/signup", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 201
    assert res.json["message"] == "ok"

def test_api_login(client):
    # first signup
    payload = {"email": "login@example.com", "password": "password"}
    client.post("/api/signup", data=json.dumps(payload), content_type="application/json")

    # then login
    res = client.post("/api/login", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 200
    assert res.json["message"] == "ok"
    assert res.json["user"]["email"] == "login@example.com"

def test_api_login_invalid(client):
    payload = {"email": "notexist@example.com", "password": "password"}
    res = client.post("/api/login", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 401
    assert res.json["error"] == "Invalid credentials"
