// Frontend settings.
// Offline demo (default): open index.html, everything runs in the browser.
// With backend: start the API (see README), then open index.html?api=1
window.WGM_CONFIG = {
  USE_API: new URLSearchParams(location.search).get("api") === "1",
  API_BASE: "http://localhost:8000"
};
