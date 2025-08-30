from app.main import create_app


def test_status_returns_ok():
    app = create_app().test_client()
    response = app.get("/status")
    assert response.status_code == 200
    assert response.get_json()["ok"] is True
