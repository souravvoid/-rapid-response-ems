# backend/seed_db.py
from app import create_app
from app.db import db
from app.models import Ambulance

app = create_app()
with app.app_context():
    # Check if ambulances already exist to avoid duplicates
    if Ambulance.query.count() == 0:
        amb1 = Ambulance(name="AMB-101", lat=12.9716, lon=77.5946)
        amb2 = Ambulance(name="AMB-102", lat=12.975, lon=77.599)
        amb3 = Ambulance(name="AMB-103", lat=12.978, lon=77.592)
        db.session.add_all([amb1, amb2, amb3])
        db.session.commit()
        print("Seeded 3 ambulances")
    else:
        print("Ambulances already exist")
