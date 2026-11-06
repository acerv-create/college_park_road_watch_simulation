let activeMode = 'all';
let map, pathLayerGroup;
let notices = []; // Dynamic container for live notices

document.addEventListener('DOMContentLoaded', () => {
  map = L.map('map').setView([38.98715, -76.94345], 15);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  pathLayerGroup = L.layerGroup().addTo(map);

  // Load live JSON output from scraper
  fetchLiveNotices();
  fetchCampusPaths();

  setTimeout(() => map.invalidateSize(), 300);
});

function fetchLiveNotices() {
  fetch('notices.json')
    .then(res => res.json())
    .then(data => {
      notices = data;
      renderNotices();
      renderMapMarkers();
    })
    .catch(err => {
      console.warn("Could not load dynamic notices.json:", err);
    });
}