"""Reference data: cities, event keywords, simulated IMD advisories, clickbait phrases.
Keep in sync with frontend/js/data.js"""

# (city, state, lat, lon, extra aliases). The lowercase city name is always an alias.
_CITIES = [
    ("Mumbai", "Maharashtra", 19.08, 72.88, ["मुंबई", "andheri", "thane"]),
    ("Pune", "Maharashtra", 18.52, 73.86, ["पुणे"]),
    ("Nashik", "Maharashtra", 20.0, 73.79, []),
    ("Nagpur", "Maharashtra", 21.15, 79.09, []),
    ("Amravati", "Maharashtra", 20.93, 77.75, []),
    ("Delhi", "Delhi", 28.61, 77.21, ["दिल्ली"]),
    ("Chennai", "Tamil Nadu", 13.08, 80.27, []),
    ("Kolkata", "West Bengal", 22.57, 88.36, []),
    ("Bengaluru", "Karnataka", 12.97, 77.59, ["bangalore", "bellandur"]),
    ("Hyderabad", "Telangana", 17.39, 78.49, []),
    ("Ahmedabad", "Gujarat", 23.02, 72.57, []),
    ("Jaipur", "Rajasthan", 26.91, 75.79, []),
    ("Lucknow", "Uttar Pradesh", 26.85, 80.95, []),
    ("Patna", "Bihar", 25.59, 85.14, []),
    ("Guwahati", "Assam", 26.18, 91.74, []),
    ("Kochi", "Kerala", 9.93, 76.27, []),
    ("Bhubaneswar", "Odisha", 20.3, 85.82, []),
    ("Shimla", "Himachal Pradesh", 31.1, 77.17, []),
    ("Kedarnath", "Uttarakhand", 30.73, 79.07, []),
    ("Srinagar", "Jammu and Kashmir", 34.08, 74.8, []),
]
CITIES = [
    {"name": c[0], "state": c[1], "lat": c[2], "lon": c[3], "aliases": [c[0].lower(), *c[4]]}
    for c in _CITIES
]

# (event, pin letter, keywords). Order matters: the first match wins.
EVENTS = [
    ("cloudburst", "C", ["cloudburst", "बादल फटा"]),
    ("landslide", "L", ["landslide", "भूस्खलन"]),
    ("flood", "F", ["flood", "waterlogging", "बाढ़", "overflowing", "submerged"]),
    ("hail", "H", ["hail"]),
    ("heatwave", "T", ["heatwave", "heat wave", "लू"]),
    ("cyclone", "Y", ["cyclone"]),
    ("rain", "R", ["heavy rain", "rain", "बारिश"]),
]

# Simulated IMD advisory feed. Replace with a real collector later.
ADVISORY = [
    {"state": "Maharashtra", "event": "flood"},
    {"state": "Uttarakhand", "event": "cloudburst"},
    {"state": "Assam", "event": "flood"},
]

CLICKBAIT = ["shocking", "unbelievable", "100% true", "forward", "share this", "breaking!!!", "must watch"]

TRUSTED_SOURCES = {"News RSS", "IMD Official"}
