def test_home_redirect(client):
    res = client.get("/")
    assert res.status_code == 302  # redirect
    assert "/login" in res.location

def test_signup_page_get(client):
    res = client.get("/signup")
    assert res.status_code == 200
    assert b"Sign Up" in res.data

def test_login_page_get(client):
    res = client.get("/login")
    assert res.status_code == 200
    assert b"Login" in res.data
