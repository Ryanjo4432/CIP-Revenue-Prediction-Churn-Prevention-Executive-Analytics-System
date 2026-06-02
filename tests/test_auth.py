def test_register(client):
    res = client.post("/auth/register", json={
        "username": "testuser",
        "email":    "testuser@example.com",
        "password": "password123",
    })
    assert res.status_code == 201
    assert res.json()["username"] == "testuser"


def test_register_duplicate(client):
    client.post("/auth/register", json={"username": "dupuser", "email": "dup1@example.com", "password": "pw"})
    res = client.post("/auth/register", json={"username": "dupuser", "email": "dup2@example.com", "password": "pw"})
    assert res.status_code == 400


def test_login(client):
    client.post("/auth/register", json={"username": "loginuser", "email": "login@example.com", "password": "pw123"})
    res = client.post("/auth/login", data={"username": "loginuser", "password": "pw123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "wrongpw", "email": "wrongpw@example.com", "password": "correct"})
    res = client.post("/auth/login", data={"username": "wrongpw", "password": "wrong"})
    assert res.status_code == 401


def test_me_endpoint(client):
    client.post("/auth/register", json={"username": "meuser", "email": "me@example.com", "password": "pw"})
    login = client.post("/auth/login", data={"username": "meuser", "password": "pw"})
    token = login.json()["access_token"]

    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == "meuser"


def test_me_no_token(client):
    res = client.get("/auth/me")
    assert res.status_code == 401
