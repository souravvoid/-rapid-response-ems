from flask import Blueprint, request, jsonify, session, render_template
from app.models import Incident, Ambulance, Driver, Hospital
from app.db import db
from app.utils.graph import build_graph_from_points, estimate_eta_from_distance_km
from app.utils.hospital_check import find_nearest_available_hospitals

emergency_bp = Blueprint("emergency", __name__)

@emergency_bp.route("/emergency", methods=["GET"])
def emergency_form_page():
   
    return render_template("emergency_form.html")

@emergency_bp.route("/api/emergency", methods=["POST"])
def api_emergency():
    data = request.json
    # required fields
    patient_name = data.get("patient_name")
    contact = data.get("contact_number")
    lat = float(data.get("latitude"))
    lon = float(data.get("longitude"))
    severity = data.get("severity", "medium")

   
    incident = Incident(
        patient_name=patient_name,
        contact_number=contact,
        latitude=lat,
        longitude=lon,
        severity=severity,
        status="reported"
    )
    db.session.add(incident)
    db.session.commit()

    # fetch available ambulances & hospitals
    ambulances = Ambulance.query.filter(Ambulance.status == "available").all()
    hospitals = Hospital.query.filter(Hospital.has_emergency == True).all()

   
    if not ambulances:
        return jsonify({"error":"No ambulances available","incident_id":incident.id}), 200

   
    graph = build_graph_from_points(ambulances, hospitals, (lat, lon))

    # compute for each ambulance: distance (via graph) and full route to hospital through incident
    candidates = []
    for amb in ambulances:
        amb_node = f"AMB-{amb.id}"
        # path from ambulance to incident
        dist_to_incident, _ = graph.dijkstra(amb_node, "INCIDENT")
        if dist_to_incident is None:
            continue
        # pick nearest hospital that has bed and can accept
        hospital_list = find_nearest_available_hospitals(db.session, lat, lon, limit=5)
        assigned_hospital = None
        for (h_dist, hosp) in hospital_list:
            if hosp.available_beds and hosp.available_beds > 0:
                assigned_hospital = hosp
                break
        if not assigned_hospital:
            # fallback to nearest hospital (even if 0 beds)
            if hospital_list:
                assigned_hospital = hospital_list[0][1]
        # distance from incident to hospital
        hosp_node = f"HOSP-{assigned_hospital.id}"
        dist_incident_to_hosp, _ = graph.dijkstra("INCIDENT", hosp_node)
        total_km = dist_to_incident + (dist_incident_to_hosp or 0)
        eta = estimate_eta_from_distance_km(dist_to_incident)
        candidates.append({
            "ambulance": amb,
            "driver": Driver.query.filter_by(ambulance_id=amb.id, is_available=True).first(),
            "distance_km": dist_to_incident,
            "total_km_to_hospital": total_km,
            "assigned_hospital": assigned_hospital,
            "eta_iso": eta
        })

    if not candidates:
        return jsonify({"error":"No route candidates found","incident_id":incident.id}), 200

    # score by ETA or distance + severity weighting; here we choose shortest distance->incident
    candidates.sort(key=lambda c: c["distance_km"])
    best = candidates[0]

  
    incident.assigned_ambulance_id = best["ambulance"].id
    incident.assigned_driver_id = best["driver"].id if best["driver"] else None
    incident.assigned_hospital_id = best["assigned_hospital"].id if best["assigned_hospital"] else None
    incident.status = "assigned"
    incident.estimated_arrival_time = best["eta_iso"]

  
    best["ambulance"].status = "assigned"
    if best["driver"]:
        best["driver"].is_available = False
    # decrease hospital bed count (reservation)
    if best["assigned_hospital"] and best["assigned_hospital"].available_beds > 0:
        best["assigned_hospital"].available_beds -= 1

    db.session.commit()

    response = {
        "incident_id": incident.id,
        "assigned_ambulance": {
            "id": best["ambulance"].id,
            "vehicle_number": best["ambulance"].vehicle_number,
            "lat": best["ambulance"].current_latitude,
            "lon": best["ambulance"].current_longitude
        },
        "assigned_driver": {
            "id": best["driver"].id if best["driver"] else None,
            "name": best["driver"].name if best["driver"] else None
        },
        "assigned_hospital": {
            "id": best["assigned_hospital"].id if best["assigned_hospital"] else None,
            "name": best["assigned_hospital"].name if best["assigned_hospital"] else None
        },
        "eta": best["eta_iso"],
        "distance_km": round(best["distance_km"],2)
    }
    return jsonify(response), 200

@emergency_bp.route("/api/incident/<int:incident_id>", methods=["GET"])
def api_incident_status(incident_id):
    inc = Incident.query.get(incident_id)
    if not inc:
        return jsonify({"error":"Not found"}), 404
    return jsonify({
        "id": inc.id,
        "status": inc.status,
        "assigned_ambulance_id": inc.assigned_ambulance_id,
        "assigned_driver_id": inc.assigned_driver_id,
        "assigned_hospital_id": inc.assigned_hospital_id,
        "eta": inc.estimated_arrival_time
    })
