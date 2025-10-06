from flask import Blueprint, request, jsonify
from app.models import Incident, Ambulance, db

incidents_bp = Blueprint("incidents", __name__)

@incidents_bp.route("/", methods=["POST"])
def create_incident():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")
    reason = data.get("reason", "Personal Emergency")

    incident = Incident(lat=lat, lon=lon, reason=reason)
    db.session.add(incident)
    db.session.commit()

    # Assign first available ambulance
    ambulance = Ambulance.query.filter_by(status="available").first()
    if ambulance:
        incident.assigned_ambulance_id = ambulance.id
        incident.status = "assigned"
        ambulance.status = "busy"  # Mark as busy
        db.session.commit()

    return jsonify({
        "incident_id": incident.id,
        "assigned_ambulance": ambulance.name if ambulance else None
    }), 201
