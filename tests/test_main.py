# tests/test_main.py
from app.main import create_app

def _client():
    return create_app().test_client()

def test_status_and_ready():
    c = _client()
    assert c.get("/status").status_code == 200
    assert c.get("/readyz").status_code == 200

def test_echo_and_time_uuid_hash():
    c = _client()
    assert c.get("/echo?msg=hiya").get_json()["echo"] == "hiya"
    assert "utc_iso" in c.get("/time").get_json()
    assert len(c.get("/uuid").get_json()["uuid"]) >= 32
    h = c.get("/hash?text=abc").get_json()
    assert h["hash"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

def test_random_and_email():
    c = _client()
    j = c.get("/random?min=1&max=3&n=5").get_json()
    assert len(j["numbers"]) == 5
    assert all(1 <= x <= 3 for x in j["numbers"])
    assert c.get("/validate-email?email=test@example.com").get_json()["valid"] is True
    assert c.get("/validate-email?email=bad@").get_json()["valid"] is False

def test_todos_crud():
    c = _client()
    # create
    r = c.post("/todos", json={"title": "first task"})
    assert r.status_code == 201
    tid = r.get_json()["id"]

    # list
    j = c.get("/todos").get_json()
    assert any(item["id"] == tid for item in j["items"])

    # update title & done
    r2 = c.patch(f"/todos/{tid}", json={"title": "renamed", "done": True})
    j2 = r2.get_json()
    assert j2["title"] == "renamed" and j2["done"] is True

    # delete
    r3 = c.delete(f"/todos/{tid}")
    assert r3.get_json()["deleted"] == tid
    assert c.patch(f"/todos/{tid}", json={"done": False}).status_code == 404
