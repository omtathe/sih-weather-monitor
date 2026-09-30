from backend import db, service


def fresh():
    con = db.connect(":memory:")
    service.seed_if_empty(con)
    return con


def test_seed_loads_ten_reports():
    assert service.stats(fresh())["reports"] == 10


def test_ingest_stores_and_returns_report():
    con = fresh()
    r = service.ingest(con, "Heavy flooding in Pune near Swargate", "X", 900, "new1")
    assert r["id"] == 11 and r["x"]["city"] == "Pune" and r["label"] in ("Verified", "Suspicious", "Fake")
    assert db.get_report(con, 11)["text"] == r["text"]


def test_filters_and_alerts():
    con = fresh()
    assert all(r["label"] == "Fake" for r in db.list_reports(con, label="Fake"))
    assert service.alerts(con)[0]["imd_advisory"] is True
