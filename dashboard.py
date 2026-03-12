import streamlit as st
import pandas as pd
import math
from firebase_admin import db
from firebase_config import *
from streamlit_autorefresh import st_autorefresh

# ----------------------------
# PAGE SETUP
# ----------------------------

st.set_page_config(page_title="Motor Health Monitor", layout="centered")

# refresh every 2 seconds
st_autorefresh(interval=2000)

st.title("🔧 Motor Health Monitor")
st.caption("Real-time vibration monitoring system")

# ----------------------------
# FIREBASE REFERENCES
# ----------------------------

readings_ref = db.reference("machines/motor_1/readings")
prediction_ref = db.reference("machines/motor_1/prediction")

data = readings_ref.get()

# ----------------------------
# HANDLE SENSOR DATA
# ----------------------------

if isinstance(data, dict) and "vibration_x" in data:
    latest = data
else:
    st.warning("Waiting for sensor readings...")
    st.stop()

# ----------------------------
# RAW SENSOR VALUES
# ----------------------------

RAW_TO_G = 16384.0

x = float(latest.get("vibration_x",0)) / RAW_TO_G
y = float(latest.get("vibration_y",0)) / RAW_TO_G
z = float(latest.get("vibration_z",0)) / RAW_TO_G

gx = float(latest.get("gyro_x",0))
gy = float(latest.get("gyro_y",0))
gz = float(latest.get("gyro_z",0))

current = float(latest.get("current_ma",0))
voltage = float(latest.get("voltage_v",0))
power = float(latest.get("power_mw",0))

# ----------------------------
# VIBRATION CALCULATION
# ----------------------------

mag = math.sqrt(x*x + y*y + z*z)

# remove gravity
vibration_level = abs(mag - 1)

# thresholds (in g)
WARNING_THRESHOLD = 0.15
FAULT_THRESHOLD = 0.35

# ----------------------------
# MOTOR STATUS
# ----------------------------

st.subheader("⚙ Motor Status")

if vibration_level > FAULT_THRESHOLD:

    st.error("🔴 FAULT: Excessive vibration detected")

elif vibration_level > WARNING_THRESHOLD:

    st.warning("🟡 WARNING: High vibration detected")

else:

    st.success("🟢 NORMAL: Motor operating normally")

# ----------------------------
# SENSOR METRICS
# ----------------------------

st.subheader("📊 Latest Sensor Values")

c1,c2,c3 = st.columns(3)

c1.metric("Accel X (g)", round(x,3))
c2.metric("Accel Y (g)", round(y,3))
c3.metric("Accel Z (g)", round(z,3))

c4,c5,c6 = st.columns(3)

c4.metric("Gyro X", round(gx,2))
c5.metric("Gyro Y", round(gy,2))
c6.metric("Gyro Z", round(gz,2))

c7,c8,c9 = st.columns(3)

c7.metric("Current (mA)", round(current,2))
c8.metric("Voltage (V)", round(voltage,2))
c9.metric("Power (mW)", round(power,2))

st.metric("Vibration Level (g)", round(vibration_level,3))

# ----------------------------
# GRAPH BUFFER
# ----------------------------

if "buffer" not in st.session_state:
    st.session_state.buffer = []

buffer_data = {
    "vibration_x": x,
    "vibration_y": y,
    "vibration_z": z,
    "gyro_x": gx,
    "gyro_y": gy,
    "gyro_z": gz,
    "current_ma": current,
    "voltage_v": voltage,
    "power_mw": power
}

st.session_state.buffer.append(buffer_data)

# keep last 20 points
st.session_state.buffer = st.session_state.buffer[-20:]

df = pd.DataFrame(st.session_state.buffer)

# ----------------------------
# GRAPHS
# ----------------------------

st.subheader("📈 Acceleration")

st.line_chart(df[[
    "vibration_x",
    "vibration_y",
    "vibration_z"
]])

st.subheader("🌀 Gyroscope")

st.line_chart(df[[
    "gyro_x",
    "gyro_y",
    "gyro_z"
]])

st.subheader("⚡ Power")

st.line_chart(df[[
    "current_ma",
    "voltage_v",
    "power_mw"
]])

# ----------------------------
# ML PREDICTION
# ----------------------------

st.subheader("🧠 ML Motor Prediction")

prediction = prediction_ref.get()

if prediction:

    fault = prediction.get("fault_type","unknown")
    status = prediction.get("status","unknown")
    action = prediction.get("action","No action")

    if status == "NORMAL":

        st.success(f"Motor Condition: {fault}")

    elif status == "WARNING":

        st.warning(f"⚠ Possible Issue: {fault}")

    elif status == "FAULT":

        st.error(f"🚨 Fault Detected: {fault}")

    else:

        st.info("ML model running...")

    st.markdown("**Recommended Action**")
    st.info(action)

else:

    st.info("Waiting for ML prediction...")

# ----------------------------
# EXPORT DATA
# ----------------------------

st.subheader("📥 Export Sensor Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "motor_readings.csv",
    "text/csv"
)