from app.models import Hospital

def find_nearest_available_hospitals(db_session, incident_lat, incident_lon, limit=5):
    # Simple selection using stored coordinates and Haversine check (ordered by distance)
    from app.utils.graph import haversine
    hospitals = Hospital.query.filter_by(has_emergency=True).all()
    arr = []
    for h in hospitals:
        dist = haversine(incident_lat, incident_lon, h.latitude, h.longitude)
        arr.append((dist, h))
    arr.sort(key=lambda x: x[0])
    # return sorted list of (distance, hospital)
    return arr[:limit]
