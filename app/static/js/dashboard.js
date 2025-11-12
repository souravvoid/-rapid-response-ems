let map, markers = [];
document.addEventListener('DOMContentLoaded', ()=>{
  map = L.map('map').setView([28.6139,77.2090], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);

  fetchAssigned();
});

async function fetchAssigned(){
  // for demo: fetch last incident assigned to the user (simpler - fetch latest assigned incident)
  const r = await fetch('/api/latest_incident');
  const data = await r.json();
  const div = document.getElementById('assigned');
  if(data.error){ div.innerText = 'No assigned incidents'; return; }
  div.innerHTML = `<p>Incident ${data.id} — ETA: ${data.eta} — Ambulance: ${data.assigned_ambulance.vehicle_number}</p>`;
  // show markers
  clearMarkers();
  L.marker([data.assigned_ambulance.lat, data.assigned_ambulance.lon]).addTo(map).bindPopup('Ambulance');
  L.marker([data.incident_lat, data.incident_lon]).addTo(map).bindPopup('Patient');
  map.fitBounds([[data.assigned_ambulance.lat, data.assigned_ambulance.lon],[data.incident_lat, data.incident_lon]]);
}

function clearMarkers(){
  // simple: remove all markers by reinitializing map layers (lightweight)
  map.eachLayer((layer)=>{ if(layer instanceof L.Marker) map.removeLayer(layer); });
}
