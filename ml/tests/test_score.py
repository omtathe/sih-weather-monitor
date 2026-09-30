from ml.extract import extract
from ml.score import score_report


def make(text, source="X", age=900, media=None, gps=None):
    return {"text": text, "source": source, "account_age_days": age, "media_id": media, "gps": gps,
            **extract(text, gps)}


def test_extract_english_and_hindi():
    assert extract("Heavy flooding in Pune near Swargate")["city"] == "Pune"
    x = extract("मुंबई में भारी बारिश, बाढ़ जैसे हालात")
    assert (x["city"], x["event"]) == ("Mumbai", "flood")


def test_extract_uses_gps_when_no_city_in_text():
    assert extract("water everywhere", (19.1, 72.85))["city"] == "Mumbai"
    assert extract("water everywhere", (25.0, 60.0))["city"] is None


def test_real_looking_report_is_not_fake():
    r = score_report(make("Heavy flooding in Pune near Swargate, roads blocked", media="new1"))
    assert r["label"] == "Verified" and r["score"] == 75


def test_fake_looking_report_is_fake():
    r = score_report(make("SHOCKING!!! Dam burst in Delhi, 100% TRUE, forward to everyone!!!", age=6, media="m1"))
    assert r["label"] == "Fake" and r["score"] == 0


def test_reused_photo_is_penalised():
    first = {"id": 2, "text": "Andheri flooded", "media_id": "m1", "city": "Mumbai", "event": "flood"}
    r = score_report(make("Flood in Delhi right now", age=20, media="m1"), [first])
    assert ["Same text or photo already used in report #2", -40] in r["reasons"]


def test_score_is_clamped_0_to_100():
    r = score_report(make("IMD says heavy rain in Mumbai, waterlogging", source="IMD Official", age=4000))
    assert 0 <= r["score"] <= 100
