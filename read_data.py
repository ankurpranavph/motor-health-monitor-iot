from firebase_admin import db
from firebase_config import *

ref  = db.reference("machines/motor_1/readings")
data = ref.order_by_key().limit_to_last(3).get()

if data:
    for key, value in data.items():
        print(f"Key: {key}")
        print(f"Value: {value}")
        print("---")
else:
    print("No data!")