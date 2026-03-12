from firebase_config import db

def get_readings():
    docs = db.collection("machines").document("motor_1") \
             .collection("readings").order_by("timestamp").stream()
    
    readings = []
    for doc in docs:
        readings.append(doc.to_dict())
    
    return readings

data = get_readings()
for row in data:
    print(row)
```

---

## ✅ Your folder should now look like this:
```
motor-monitor/
├── serviceAccountKey.json
├── firebase_config.py
├── send_data.py
└── read_data.py