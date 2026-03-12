import streamlit as st
from firebase_admin import db
from firebase_config import *

st.set_page_config(page_title="Sensor Graphs", layout="centered")

st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#00ffcc;">📈 Sensor Graphs</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

ref  = db.reference("machines/motor_1/readings")
data = ref.order_by_key().limit_to_last(50).get()

readings = []
if data:
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                cleaned = {}
                for k, v in value.items():
                    try:
                        cleaned[k] = float(v)
                    except:
                        cleaned[k] = v
                readings.append(cleaned)

if readings:
    st.markdown("<h3 style='color:#00ffcc;'>📉 Acceleration (MPU6500)</h3>", unsafe_allow_html=True)
    st.line_chart({
        "Accel X": [float(r.get("vibration_x", 0)) for r in readings],
        "Accel Y": [float(r.get("vibration_y", 0)) for r in readings],
        "Accel Z": [float(r.get("vibration_z", 0)) for r in readings],
    })

    st.markdown("<h3 style='color:#00ffcc;'>🌀 Gyroscope (MPU6500)</h3>", unsafe_allow_html=True)
    st.line_chart({
        "Gyro X": [float(r.get("gyro_x", 0)) for r in readings],
        "Gyro Y": [float(r.get("gyro_y", 0)) for r in readings],
        "Gyro Z": [float(r.get("gyro_z", 0)) for r in readings],
    })

    st.markdown("<h3 style='color:#00ffcc;'>⚡ Power (INA219)</h3>", unsafe_allow_html=True)
    st.line_chart({
        "Current (mA)": [float(r.get("current_ma", 0)) for r in readings],
        "Voltage (V)":  [float(r.get("voltage_v",  0)) for r in readings],
        "Power (mW)":   [float(r.get("power_mw",   0)) for r in readings],
    })
else:
    st.warning("No data found!")