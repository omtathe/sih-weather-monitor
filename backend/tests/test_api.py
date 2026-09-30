import os

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")
os.environ["WGM_DB"] = ":memory:"

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402

client = TestClient(app)


def test_health_and_reports():
    assert client.get("/health").json() == {"ok": True}
    assert len(client.get("/reports").json()) >= 10


def test_check_report():
    r = client.post("/reports/check", json={"text": "Flood in Guwahati, Fancy Bazar", "source": "X"})
    assert r.status_code == 200 and r.json()["x"]["city"] == "Guwahati"
    assert client.post("/reports/check", json={"text": ""}).status_code == 422
