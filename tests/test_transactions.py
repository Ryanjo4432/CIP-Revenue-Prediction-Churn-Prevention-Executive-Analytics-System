def test_create_transaction(client):
    customer = client.post("/customers/", json={"name": "Txn User", "email": "txn@example.com"}).json()
    cid      = customer["customer_id"]

    res = client.post("/transactions/", json={
        "customer_id": cid,
        "amount":      199.99,
        "category":    "subscription",
    })
    assert res.status_code == 201
    assert float(res.json()["amount"]) == 199.99


def test_transaction_invalid_customer(client):
    res = client.post("/transactions/", json={
        "customer_id": 999999,
        "amount":      50.00,
    })
    assert res.status_code == 404


def test_get_transactions(client):
    res = client.get("/transactions/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_transactions_by_customer(client):
    customer = client.post("/customers/", json={"name": "Txn Owner", "email": "txnowner@example.com"}).json()
    cid      = customer["customer_id"]
    client.post("/transactions/", json={"customer_id": cid, "amount": 100})
    client.post("/transactions/", json={"customer_id": cid, "amount": 200})

    res = client.get(f"/transactions/customer/{cid}")
    assert res.status_code == 200
    assert len(res.json()) >= 2


def test_delete_transaction(client):
    customer = client.post("/customers/", json={"name": "Del Txn", "email": "deltxn@example.com"}).json()
    txn      = client.post("/transactions/", json={"customer_id": customer["customer_id"], "amount": 50}).json()
    res      = client.delete(f"/transactions/{txn['transaction_id']}")
    assert res.status_code == 204
