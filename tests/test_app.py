"""End-to-end API tests. They run against a throwaway SQLite file, so no
PostgreSQL is needed in CI. conftest.py sets the environment first."""


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/health/db").json() == {"database": "ok"}


def test_register_and_login_flow(client):
    r = client.post("/api/v1/auth/register", json={"username": "alice", "password": "S3cure-pass!"})
    assert r.status_code == 201
    assert r.json()["username"] == "alice"
    assert "hashed_password" not in r.json()

    r = client.post("/api/v1/auth/login", data={"username": "alice", "password": "S3cure-pass!"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    r = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["username"] == "alice"


def test_duplicate_username_rejected(client):
    body = {"username": "bob", "password": "S3cure-pass!"}
    assert client.post("/api/v1/auth/register", json=body).status_code == 201
    assert client.post("/api/v1/auth/register", json=body).status_code == 409


def test_wrong_password_rejected(client):
    client.post("/api/v1/auth/register", json={"username": "carol", "password": "S3cure-pass!"})
    r = client.post("/api/v1/auth/login", data={"username": "carol", "password": "wrong-pass"})
    assert r.status_code == 401


def test_old_hardcoded_admin_login_no_longer_works(client):
    r = client.post("/api/v1/auth/login", data={"username": "admin", "password": "admin"})
    assert r.status_code == 401


def test_weak_password_rejected(client):
    r = client.post("/api/v1/auth/register", json={"username": "dave", "password": "short"})
    assert r.status_code == 422


def test_protected_routes_need_a_token(client):
    assert client.get("/api/v1/users/").status_code == 401
    r = client.get("/api/v1/users/", headers={"Authorization": "Bearer not-a-real-token"})
    assert r.status_code == 401
