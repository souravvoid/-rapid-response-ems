from .db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(120), nullable=True)

class Ambulance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(50), nullable=False)
    equipment_type = db.Column(db.String(10), nullable=False)  # ALS/BLS
    status = db.Column(db.String(20), default="available")  # available/assigned/busy
    current_latitude = db.Column(db.Float, nullable=True)
    current_longitude = db.Column(db.Float, nullable=True)

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    ambulance_id = db.Column(db.Integer, db.ForeignKey("ambulance.id"), nullable=True)
    is_available = db.Column(db.Boolean, default=True)

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    has_emergency = db.Column(db.Boolean, default=True)
    available_beds = db.Column(db.Integer, default=0)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(120))
    contact_number = db.Column(db.String(30))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    severity = db.Column(db.String(20))  # critical/high/medium/low
    status = db.Column(db.String(20), default="reported")  # reported/assigned/enroute/completed
    assigned_ambulance_id = db.Column(db.Integer, db.ForeignKey("ambulance.id"), nullable=True)
    assigned_driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=True)
    assigned_hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), nullable=True)
    estimated_arrival_time = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
