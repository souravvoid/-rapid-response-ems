from app import create_app
from app.db import db
from app.models import Ambulance, Driver, Hospital

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    a1 = Ambulance(vehicle_number="AMB-101", equipment_type="ALS", current_latitude=28.6139, current_longitude=77.2090)
    a2 = Ambulance(vehicle_number="AMB-102", equipment_type="BLS", current_latitude=28.6210, current_longitude=77.2100)
    d1 = Driver(name="Ravi", ambulance_id=1, is_available=True)
    h1 = Hospital(name="City Hospital", latitude=28.615, longitude=77.205, has_emergency=True, available_beds=3)
    h2 = Hospital(name="Central Hospital", latitude=28.63, longitude=77.22, has_emergency=True, available_beds=0)
    db.session.add_all([a1,a2,d1,h1,h2])
    db.session.commit()
    print("seeded")
