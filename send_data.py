from firebase_config import db
from datetime import datetime

def send_vibration(x, y, z, status="normal"):
    data = {
        "vibration_x": x,
        "vibration_y": y,
        "vibration_z": z,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    
    db.collection("machines").document("motor_1") \
      .collection("readings").add(data)
    
    print(f"✅ Sent: x={x}, y={y}, z={z}, status={status}")

# Test data
send_vibration(0.12, 0.10, 0.11, "normal")
send_vibration(0.52, 0.48, 0.50, "fault")