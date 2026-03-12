from firebase_config import db

ref = db.reference("machines/motor_1/readings")

ref.set({})

print("✅ All readings cleared")