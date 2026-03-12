import streamlit as st
from firebase_admin import db
from firebase_config import *

st.set_page_config(page_title="Reading History", layout="centered")

st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#00ffcc;">📋 Reading History</h1>
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
    st.markdown(f"<p style='color:#aaa;'>Showing last {len(readings)} readings</p>", unsafe_allow_html=True)
    st.dataframe(readings, use_container_width=True)

    st.markdown("<h3 style='color:#00ffcc;'>📊 Summary</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total",      len(readings))
    col2.metric("✅ Normal",  sum(1 for r in readings if r.get("status") == "normal"))
    col3.metric("⚠️ Warning", sum(1 for r in readings if r.get("status") == "warning"))
    col4.metric("🚨 Faults",  sum(1 for r in readings if r.get("status") == "fault"))

    st.markdown("<h3 style='color:#00ffcc;'>⚡ Power Summary</h3>", unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    col5.metric("Avg Current", f"{round(sum(float(r.get('current_ma', 0)) for r in readings) / len(readings), 2)} mA")
    col6.metric("Avg Voltage", f"{round(sum(float(r.get('voltage_v',  0)) for r in readings) / len(readings), 2)} V")
    col7.metric("Avg Power",   f"{round(sum(float(r.get('power_mw',   0)) for r in readings) / len(readings), 2)} mW")
else:
    st.warning("No data found!")