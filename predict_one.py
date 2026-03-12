import pandas as pd
import joblib
import numpy as np

# =========================
# LOAD MODEL + ENCODER
# =========================
MODEL_PATH = "trained_model_90.pkl"
ENCODER_PATH = "label_encoder_90.pkl"

pipeline = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

print("Loaded model:", MODEL_PATH)
print("Loaded encoder:", ENCODER_PATH)

# =========================
# SINGLE RECORD INPUT
# =========================
record = {
    "timestamp": "2026-03-12 10:30:00",
    "sampling_rate_hz": 12000,
    "accel_x": 0.12,
    "accel_y": 0.08,
    "accel_z": 0.15,
    "gyro_x": 0.02,
    "gyro_y": 0.01,
    "gyro_z": 0.03,
    "temperature": 42.5,
    "env_temperature": 30.2,
    "env_humidity": 58.0,
    "rms_x": 0.41,
    "rms_y": 0.39,
    "rms_z": 0.44,
    "kurtosis_x": 3.2,
    "kurtosis_y": 3.1,
    "kurtosis_z": 3.4,
    "std_x": 0.12,
    "std_y": 0.11,
    "std_z": 0.13,
    "dominant_freq_x": 120.0,
    "dominant_freq_y": 118.0,
    "dominant_freq_z": 122.0,
    "dominant_magnitude_x": 1.4,
    "dominant_magnitude_y": 1.3,
    "dominant_magnitude_z": 1.5,
    "spectral_centroid_x": 310.0,
    "spectral_centroid_y": 300.0,
    "spectral_centroid_z": 320.0,
    "spectral_bandwidth_x": 90.0,
    "spectral_bandwidth_y": 88.0,
    "spectral_bandwidth_z": 92.0,
    "band_energy_0_x": 0.22,
    "band_energy_1_x": 0.35,
    "band_energy_2_x": 0.18,
    "band_energy_3_x": 0.10,
    "rms_resultant": 0.72,
    "temp_delta": 12.3,
    "vibration_trend_slope": 0.015
}

# Convert single record to DataFrame
df = pd.DataFrame([record])

# =========================
# FEATURE ENGINEERING
# (must match training exactly)
# =========================

# Parse timestamp
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["hour"] = df["timestamp"].dt.hour.fillna(0)
    df["dayofweek"] = df["timestamp"].dt.dayofweek.fillna(0)
    df["month"] = df["timestamp"].dt.month.fillna(0)
    df = df.drop(columns=["timestamp"])

# Derived features
if {"accel_x", "accel_y", "accel_z"}.issubset(df.columns):
    df["accel_mag"] = np.sqrt(df["accel_x"]**2 + df["accel_y"]**2 + df["accel_z"]**2)

if {"gyro_x", "gyro_y", "gyro_z"}.issubset(df.columns):
    df["gyro_mag"] = np.sqrt(df["gyro_x"]**2 + df["gyro_y"]**2 + df["gyro_z"]**2)

if {"rms_x", "rms_y", "rms_z"}.issubset(df.columns):
    df["rms_mean"] = (df["rms_x"] + df["rms_y"] + df["rms_z"]) / 3
    df["rms_std_axes"] = df[["rms_x", "rms_y", "rms_z"]].std(axis=1)

if {"kurtosis_x", "kurtosis_y", "kurtosis_z"}.issubset(df.columns):
    df["kurtosis_mean"] = (df["kurtosis_x"] + df["kurtosis_y"] + df["kurtosis_z"]) / 3
    df["kurtosis_max"] = df[["kurtosis_x", "kurtosis_y", "kurtosis_z"]].max(axis=1)

if {"std_x", "std_y", "std_z"}.issubset(df.columns):
    df["std_mean_axes"] = (df["std_x"] + df["std_y"] + df["std_z"]) / 3

if {"dominant_freq_x", "dominant_freq_y", "dominant_freq_z"}.issubset(df.columns):
    df["dominant_freq_mean"] = (df["dominant_freq_x"] + df["dominant_freq_y"] + df["dominant_freq_z"]) / 3

if {"dominant_magnitude_x", "dominant_magnitude_y", "dominant_magnitude_z"}.issubset(df.columns):
    df["dominant_mag_mean"] = (df["dominant_magnitude_x"] + df["dominant_magnitude_y"] + df["dominant_magnitude_z"]) / 3

if {"spectral_centroid_x", "spectral_centroid_y", "spectral_centroid_z"}.issubset(df.columns):
    df["spectral_centroid_mean"] = (
        df["spectral_centroid_x"] + df["spectral_centroid_y"] + df["spectral_centroid_z"]
    ) / 3

if {"spectral_bandwidth_x", "spectral_bandwidth_y", "spectral_bandwidth_z"}.issubset(df.columns):
    df["spectral_bandwidth_mean"] = (
        df["spectral_bandwidth_x"] + df["spectral_bandwidth_y"] + df["spectral_bandwidth_z"]
    ) / 3

if {"temperature", "env_temperature"}.issubset(df.columns):
    df["temp_gap"] = df["temperature"] - df["env_temperature"]

if {"temperature", "env_humidity"}.issubset(df.columns):
    df["temp_humidity_interaction"] = df["temperature"] * df["env_humidity"]

if {"rms_resultant", "temperature"}.issubset(df.columns):
    df["rms_temp_ratio"] = df["rms_resultant"] / (df["temperature"].replace(0, np.nan))

# Clean
df = df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(df.median(numeric_only=True))

# One-hot encode if needed
df = pd.get_dummies(df, drop_first=True)

# =========================
# PREDICT
# =========================
pred_encoded = pipeline.predict(df)
pred_label = label_encoder.inverse_transform(pred_encoded)[0]

print("\nPredicted Fault:", pred_label)

# =========================
# OPTIONAL: MAINTENANCE ACTION
# =========================
if pred_label == "normal":
    print("Maintenance Required: No immediate action")
elif pred_label == "bearing_wear":
    print("Maintenance Required: Schedule bearing inspection/replacement")
elif pred_label == "imbalance":
    print("Maintenance Required: Check rotor balance")
elif pred_label == "looseness":
    print("Maintenance Required: Inspect mounting / tighten components")
elif pred_label == "misalignment":
    print("Maintenance Required: Perform alignment check")
else:
    print("Maintenance Required: Manual inspection recommended")