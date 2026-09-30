"""Step 2: pull city, state and event type out of a post."""
import math

from .data import CITIES, EVENTS


def haversine_km(lat1, lon1, lat2, lon2):
    r = math.radians
    dl, dn = r(lat2 - lat1), r(lon2 - lon1)
    h = math.sin(dl / 2) ** 2 + math.cos(r(lat1)) * math.cos(r(lat2)) * math.sin(dn / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def extract(text, gps=None):
    """Return {city, state, lat, lon, event, letter}. Missing values are None ('?' for letter).

    gps is an optional (lat, lon). If the text names no city, the nearest city
    within 150 km of the GPS point is used.
    """
    t = text.lower()
    city = next((c for c in CITIES if any(a in t for a in c["aliases"])), None)
    if city is None and gps:
        d, i = min((haversine_km(gps[0], gps[1], c["lat"], c["lon"]), i) for i, c in enumerate(CITIES))
        if d < 150:
            city = CITIES[i]
    ev = next((e for e in EVENTS if any(k in t for k in e[2])), None)
    return {
        "city": city["name"] if city else None,
        "state": city["state"] if city else None,
        "lat": city["lat"] if city else None,
        "lon": city["lon"] if city else None,
        "event": ev[0] if ev else None,
        "letter": ev[1] if ev else "?",
    }
