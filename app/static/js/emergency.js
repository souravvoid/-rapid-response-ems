document.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('emergencyForm');
  const useGps = document.getElementById('useGps');
  useGps.addEventListener('click', ()=>{
    if(!navigator.geolocation){ alert('No geolocation'); return;}
    navigator.geolocation.getCurrentPosition(pos=>{
      document.getElementById('latitude').value = pos.coords.latitude;
      document.getElementById('longitude').value = pos.coords.longitude;
    }, err=> alert('GPS error'));
  });

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const payload = {
      patient_name: document.getElementById('patient_name').value,
      contact_number: document.getElementById('contact_number').value,
      latitude: document.getElementById('latitude').value,
      longitude: document.getElementById('longitude').value,
      severity: document.getElementById('severity').value
    };
    const res = await fetch('/api/emergency', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if(data.error) document.getElementById('result').innerText = data.error;
    else {
      document.getElementById('result').innerText = 'Assigned ambulance ID: ' + data.assigned_ambulance.id + ' ETA: ' + data.eta;
      // redirect to dashboard and show incident status
      window.location.href = '/dashboard';
    }
  });
});
