// Thin wrapper around the FastAPI backend (see docs/API.md).
const API = {
  async get(path) {
    const r = await fetch(WGM_CONFIG.API_BASE + path);
    if (!r.ok) throw new Error("GET " + path + " failed: " + r.status);
    return r.json();
  },
  async post(path, body) {
    const r = await fetch(WGM_CONFIG.API_BASE + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error("POST " + path + " failed: " + r.status);
    return r.json();
  }
};

// Backend report -> the shape the UI expects (x.c holds the city coordinates).
function normalize(r) {
  const x = r.x || {};
  x.c = x.lat != null && x.lon != null ? { la: x.lat, lo: x.lon } : null;
  x.letter = x.letter || "?";
  r.x = x;
  return r;
}
