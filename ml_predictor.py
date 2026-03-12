import pandas as pd
import joblib
import numpy as np
from scipy import stats
from firebase_admin import db
from firebase_config import *
from datetime import datetime
import time

# Load model
pipeline = joblib.load("trained_model_90.pkl")
label_encoder = joblib.load("label_encoder_90.pkl")

print("✅ Model loaded")

def compute_features(readings):

    ax = [float(r.get("vibration_x",0)) for r in readings]
    ay = [float(r.get("vibration_y",0)) for r in readings]
    az = [float(r.get("vibration_z",0)) for r in readings]

    gx = [float(r.get("gyro_x",0)) for r in readings]
    gy = [float(r.get("gyro_y",0)) for r in readings]
    gz = [float(r.get("gyro_z",0)) for r in readings]

    def rms(arr):
        return float(np.sqrt(np.mean(np.array(arr)**2)))

    def kurtosis(arr):
        return float(stats.kurtosis(arr)) if len(arr) > 1 else 0.0

    record = {
        "timestamp": datetime.now(),

        "accel_x": np.mean(ax),
        "accel_y": np.mean(ay),
        "accel_z": np.mean(az),

        "gyro_x": np.mean(gx),
        "gyro_y": np.mean(gy),
        "gyro_z": np.mean(gz),

        "rms_x": rms(ax),
        "rms_y": rms(ay),
        "rms_z": rms(az),

        "kurtosis_x": kurtosis(ax),
        "kurtosis_y": kurtosis(ay),
        "kurtosis_z": kurtosis(az),

        "std_x": np.std(ax),
        "std_y": np.std(ay),
        "std_z": np.std(az)
    }

    return record


def predict_fault(readings):

    features = compute_features(readings)

    df = pd.DataFrame([features])

    # timestamp features
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    df["dayofweek"] = pd.to_datetime(df["timestamp"]).dt.dayofweek
    df["month"] = pd.to_datetime(df["timestamp"]).dt.month

    df = df.drop(columns=["timestamp"])

    df["accel_mag"] = np.sqrt(df["accel_x"]**2 + df["accel_y"]**2 + df["accel_z"]**2)
    df["gyro_mag"] = np.sqrt(df["gyro_x"]**2 + df["gyro_y"]**2 + df["gyro_z"]**2)

    df = df.replace([np.inf,-np.inf],np.nan)
    df = df.fillna(df.median(numeric_only=True))

    pred_encoded = pipeline.predict(df)

    fault = label_encoder.inverse_transform(pred_encoded)[0]

    return fault


def get_action(fault):

    actions = {
        "normal":"No maintenance required",
        "bearing_wear":"Inspect bearings",
        "imbalance":"Check rotor balance",
        "looseness":"Check bolts",
        "misalignment":"Perform alignment check"
    }

    return actions.get(fault,"Manual inspection required")


def run_predictor():

    print("🔄 Predictor running")

    while True:

        try:

            ref = db.reference("machines/motor_1/readings")

            data = ref.get()

            readings = []

            if data:

                keys = sorted(data.keys())

                for k in keys[-20:]:
                    readings.append(data[k])

            print("📊 readings:",len(readings))

            if len(readings) >= 10:

                fault = predict_fault(readings)

                action = get_action(fault)

                if fault == "normal":
                    status = "NORMAL"
                elif fault in ["misalignment","looseness"]:
                    status = "WARNING"
                else:
                    status = "FAULT"

                print("🔍 predicted:",fault)

                db.reference("machines/motor_1/prediction").set({
                    "fault_type": fault,
                    "status": status,
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                })

                print("✅ prediction written")

            else:
                print("⚠ waiting for more readings")

        except Exception as e:
            print("❌ error:",e)

        time.sleep(5)


if __name__ == "__main__":
    run_predictor()