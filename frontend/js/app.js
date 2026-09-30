// App start-up and the "Check a new report" flow.
const db = [];
let backendUp = false;

function ingest(p) {
  p.x = extract(p);
  Object.assign(p, verify(p, db));
  db.push(p);
  return p;
}

function setMode(msg) { $("mode").textContent = msg; }

$("go").onclick = async () => {
  const text = $("in").value.trim();
  if (!text) { $("trace").innerHTML = "<div>Paste or load a report first.</div>"; return; }
  const m = $("med").value;
  const payload = {
    text,
    source: $("src").value,
    account_age_days: +$("acct").value,
    media_id: m === "0" ? null : m === "1" ? "new" + Date.now() : "m1",
    gps: null
  };
  let p = null;
  if (backendUp) {
    try { p = normalize(await API.post("/reports/check", payload)); db.push(p); }
    catch (e) { backendUp = false; setMode("Backend stopped answering, using offline scoring."); }
  }
  if (!p) {
    p = ingest({
      id: db.length + 1, text, src: payload.source, t: Date.now(), gps: null,
      media: payload.media_id || 0, age: payload.account_age_days, trusted: payload.source === "News RSS"
    });
  }
  const steps = [
    ["1 Collect", "Got a post from " + p.src],
    ["2 Extract", "City: " + (p.x.city || "not found") + ", state: " + (p.x.state || "not found") + ", event: " + (p.x.event || "not found")],
    ["3 Verify", "Score " + p.score + "/100, " + p.label],
    ["4 Store", "Saved as report #" + p.id + " and shown on the map"]
  ];
  $("trace").innerHTML = "";
  steps.forEach((s, i) => setTimeout(() => {
    $("trace").insertAdjacentHTML("beforeend", `<div><b>${s[0]}:</b> ${esc(s[1])}</div>`);
    if (i === 3) { sel = p.id; render(); }
  }, i * 350));
};

(async function init() {
  let loaded = false;
  if (WGM_CONFIG.USE_API) {
    try {
      (await API.get("/reports")).forEach(r => db.push(normalize(r)));
      loaded = backendUp = true;
      setMode("Connected to backend at " + WGM_CONFIG.API_BASE);
    } catch (e) {
      setMode("Backend not reachable, showing offline sample data.");
    }
  } else {
    setMode("Offline demo mode: sample data and scoring run in your browser.");
  }
  if (!loaded) SEED.forEach(ingest);
  render();
})();
