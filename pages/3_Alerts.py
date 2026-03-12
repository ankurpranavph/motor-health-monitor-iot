import streamlit as st
import time
from firebase_admin import db
from firebase_config import *

st.set_page_config(page_title="Alerts", layout="centered")

st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#ff4444;">🚨 Alerts</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

NORMAL_THRESHOLD  = 0.2
WARNING_THRESHOLD = 0.4

def classify_reading(r):
    max_vib = max(
        abs(float(r.get("vibration_x", 0))),
        abs(float(r.get("vibration_y", 0))),
        abs(float(r.get("vibration_z", 0)))
    )
    if max_vib < NORMAL_THRESHOLD:
        return "normal"
    elif max_vib < WARNING_THRESHOLD:
        return "warning"
    else:
        return "fault"

while True:
    readings_ref = db.reference("machines/motor_1/readings")
    raw = readings_ref.order_by_key().limit_to_last(50).get()

    readings = []
    if raw and isinstance(raw, dict):
        for key, value in raw.items():
            if isinstance(value, dict):
                cleaned = {}
                for k, v in value.items():
                    try:
                        cleaned[k] = float(v)
                    except Exception:
                        cleaned[k] = v
                cleaned["_status"] = classify_reading(cleaned)
                readings.append(cleaned)

    pred_data  = db.reference("machines/motor_1/prediction").get() or {}
    fault_type = pred_data.get("fault_type", "unknown")
    ml_action  = pred_data.get("action", "—")
    ml_ts      = pred_data.get("timestamp", "N/A")

    fault_colors = {
        "normal":       "#00ff88",
        "bearing_wear": "#ff4444",
        "imbalance":    "#ff4444",
        "looseness":    "#ffcc00",
        "misalignment": "#ffcc00",
    }
    ml_color = fault_colors.get(fault_type, "#ff4444")

    st.markdown(f"""
        <div style="background-color:#1e1e2e; padding:15px; border-radius:10px; text-align:center; margin-bottom:15px;">
            <h3 style="color:#aaa; margin:0;">🤖 Current ML Prediction</h3>
            <h2 style="color:{ml_color}; margin:5px 0;">{fault_type.upper().replace('_', ' ')}</h2>
            <p style="color:#aaa; margin:0;">🔧 {ml_action}</p>
            <p style="color:#555; margin:0; font-size:12px;">🕒 {ml_ts}</p>
        </div>
    """, unsafe_allow_html=True)

    faults   = [r for r in readings if r["_status"] == "fault"]
    warnings = [r for r in readings if r["_status"] == "warning"]
    total    = len(readings)

    st.markdown(f"""
        <div style="display:flex; gap:10px;">
            <div style="background-color:#4a1a1a; padding:20px; border-radius:10px; text-align:center; flex:1;">
                <h4 style="color:#aaa;">🚨 Faults</h4>
                <h2 style="color:#ff4444;">{len(faults)}</h2>
                <p style="color:#aaa;">of {total} readings</p>
            </div>
            <div style="background-color:#4a3a1a; padding:20px; border-radius:10px; text-align:center; flex:1;">
                <h4 style="color:#aaa;">⚠️ Warnings</h4>
                <h2 style="color:#ffcc00;">{len(warnings)}</h2>
                <p style="color:#aaa;">of {total} readings</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if faults:
        st.markdown("<h3 style='color:#ff4444;'>🚨 Fault Events</h3>", unsafe_allow_html=True)
        for r in reversed(faults):
            st.markdown(f"""
                <div style="background-color:#2a1a1a; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <p style="color:#ff4444; margin:0;">🚨 FAULT DETECTED</p>
                    <p style="color:#aaa; margin:0;">🕒 {r.get("timestamp", "N/A")}</p>
                    <p style="color:#aaa; margin:0;">Accel: ({r.get("vibration_x")} , {r.get("vibration_y")} , {r.get("vibration_z")}) | Gyro: ({r.get("gyro_x")} , {r.get("gyro_y")} , {r.get("gyro_z")})</p>
                    <p style="color:#f97316; margin:0;">⚡ {r.get("current_ma")} mA | {r.get("voltage_v")} V | {r.get("power_mw")} mW</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background-color:#1a2a1a; padding:15px; border-radius:10px; text-align:center;">
                <h3 style="color:#00ff88;">✅ No faults detected in last 50 readings!</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if warnings:
        st.markdown("<h3 style='color:#ffcc00;'>⚠️ Warning Events</h3>", unsafe_allow_html=True)
        for r in reversed(warnings):
            st.markdown(f"""
                <div style="background-color:#2a2a1a; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <p style="color:#ffcc00; margin:0;">⚠️ WARNING</p>
                    <p style="color:#aaa; margin:0;">🕒 {r.get("timestamp", "N/A")}</p>
                    <p style="color:#aaa; margin:0;">Accel: ({r.get("vibration_x")} , {r.get("vibration_y")} , {r.get("vibration_z")}) | Gyro: ({r.get("gyro_x")} , {r.get("gyro_y")} , {r.get("gyro_z")})</p>
                    <p style="color:#f97316; margin:0;">⚡ {r.get("current_ma")} mA | {r.get("voltage_v")} V | {r.get("power_mw")} mW</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background-color:#1a2a1a; padding:15px; border-radius:10px; text-align:center;">
                <h3 style="color:#00ff88;">✅ No warnings!</h3>
            </div>
        """, unsafe_allow_html=True)

    time.sleep(2)
    st.rerun()