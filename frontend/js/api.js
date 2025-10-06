const API_URL = "http://127.0.0.1:5000";

async function requestAmbulance() {
    const lat = parseFloat(document.getElementById("lat").value);
    const lon = parseFloat(document.getElementById("lon").value);
    const res = await fetch(`${API_URL}/incidents/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lat, lon })
    });
    const data = await res.json();
    document.getElementById("result").innerText =
        `Assigned Ambulance: ${data.assigned_ambulance}`;

    // Refresh ambulance list automatically
    loadAmbulances();
}

async function loadAmbulances() {
    const res = await fetch(`${API_URL}/ambulances/`);
    const ambs = await res.json();
    const list = document.getElementById("ambulancesList");
    list.innerHTML = "";
    ambs.forEach(a => {
        const li = document.createElement("li");
        li.innerText = `${a.name} - ${a.status} (Lat:${a.lat}, Lon:${a.lon})`;
        list.appendChild(li);
    });
}
