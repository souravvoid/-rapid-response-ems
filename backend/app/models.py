from .db import db
from datetime import datetime

class Ambulance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lon = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default="available")

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255), default="Personal Emergency")
    assigned_ambulance_id = db.Column(db.Integer, db.ForeignKey('ambulance.id'), nullable=True)
    status = db.Column(db.String(20), default="reported")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
