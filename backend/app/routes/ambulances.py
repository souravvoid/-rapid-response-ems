from flask import Blueprint, jsonify
from app.models import Ambulance

ambulances_bp = Blueprint("ambulances", __name__)

@ambulances_bp.route("/", methods=["GET"])
def list_ambulances():
    ambs = Ambulance.query.all()
    return jsonify([{
        "id": a.id,
        "name": a.name,
        "lat": a.lat,
        "lon": a.lon,
        "status": a.status
    } for a in ambs])
