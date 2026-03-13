import time
from datetime import datetime
from firebase_admin import db
from firebase_config import *

CHECK_INTERVAL = 5      # seconds between checks
MAX_IDLE_TIME = 15      # seconds allowed without new reading


def run_watchdog():

    print("👀 Firebase Watchdog Started")

    last_timestamp = None

    while True:

        try:

            ref = db.reference("machines/motor_1/readings")

            data = ref.get()

            if not data:

                print("⚠ No sensor data found in Firebase")
                time.sleep(CHECK_INTERVAL)
                continue

            # since your database stores a single reading object
            if isinstance(data, dict):

                timestamp = data.get("timestamp")

            else:

                timestamp = None


            if timestamp != last_timestamp:

                print("✅ New reading detected:", timestamp)

                last_timestamp = timestamp

            else:

                print("⚠ No new readings detected")


            # check if data is stale
            if timestamp:

                try:

                    now = datetime.now()

                    # timestamp might be millis or simple number
                    if isinstance(timestamp, (int, float)):

                        delta = now.timestamp() - float(timestamp)

                    else:

                        delta = 0

                    if delta > MAX_IDLE_TIME:

                        print("🚨 Sensor readings may have stopped!")

                except Exception as e:

                    print("Timestamp parse error:", e)


        except Exception as e:

            print("❌ Watchdog error:", e)


        time.sleep(CHECK_INTERVAL)



# only run if executed directly
if __name__ == "__main__":

    run_watchdog()