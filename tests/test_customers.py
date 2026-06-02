def test_create_customer(client):
    res = client.post("/customers/", json={
        "name":     "Test User",
        "email":    "test@example.com",
        "age":      25,
        "location": "New York",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "test@example.com"
    assert data["name"]  == "Test User"


def test_duplicate_email_rejected(client):
    client.post("/customers/", json={"name": "A", "email": "dup@example.com"})
    res = client.post("/customers/", json={"name": "B", "email": "dup@example.com"})
    assert res.status_code == 400


def test_get_customers(client):
    res = client.get("/customers/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_customer_by_id(client):
    create = client.post("/customers/", json={"name": "Find Me", "email": "findme@example.com"})
    cid    = create.json()["customer_id"]
    res    = client.get(f"/customers/{cid}")
    assert res.status_code == 200
    assert res.json()["customer_id"] == cid


def test_customer_not_found(client):
    res = client.get("/customers/999999")
    assert res.status_code == 404


def test_update_customer(client):
    create = client.post("/customers/", json={"name": "Old Name", "email": "update@example.com"})
    cid    = create.json()["customer_id"]
    res    = client.put(f"/customers/{cid}", json={"name": "New Name", "email": "update@example.com"})
    assert res.status_code == 200
    assert res.json()["name"] == "New Name"


def test_delete_customer(client):
    create = client.post("/customers/", json={"name": "Del Me", "email": "del@example.com"})
    cid    = create.json()["customer_id"]
    res    = client.delete(f"/customers/{cid}")
    assert res.status_code == 204
    assert client.get(f"/customers/{cid}").status_code == 404
