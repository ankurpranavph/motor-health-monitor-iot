import time
from datetime import datetime
from firebase_admin import db
from firebase_config import *

CHECK_INTERVAL = 5       # seconds between checks
MAX_IDLE_TIME = 10       # seconds allowed without new reading

last_seen_timestamp = None

print("👀 Firebase Watchdog Started")

while True:

    try:
        ref = db.reference("machines/motor_1/readings")

        data = ref.get()

        if not data:
            print("⚠ No readings found in Firebase")
            time.sleep(CHECK_INTERVAL)
            continue

        keys = sorted(data.keys())
        latest_key = keys[-1]

        latest_reading = data[latest_key]

        timestamp = latest_reading.get("timestamp")

        if timestamp != last_seen_timestamp:

            last_seen_timestamp = timestamp
            print("✅ New reading detected:", timestamp)

        else:

            print("⚠ No new readings detected")

        # check time difference
        if timestamp:
            try:
                t = datetime.fromisoformat(timestamp)
                delta = (datetime.now() - t).total_seconds()

                if delta > MAX_IDLE_TIME:
                    print("🚨 Readings appear stalled! Last update:", delta, "seconds ago")

            except:
                pass

    except Exception as e:

        print("❌ Watchdog error:", e)

    time.sleep(CHECK_INTERVAL)