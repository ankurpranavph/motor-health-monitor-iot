import streamlit as st
from firebase_config import db

st.set_page_config(page_title="Vibration Graph", layout="centered")

st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#00ffcc;">📈 Vibration Graph</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

docs = db.collection("machines").document("motor_1") \
         .collection("readings") \
         .order_by("timestamp") \
         .limit_to_last(50) \
         .get()

readings = [doc.to_dict() for doc in docs]

if readings:
    chart_data = {
        "X": [r.get("vibration_x", 0) for r in readings],
        "Y": [r.get("vibration_y", 0) for r in readings],
        "Z": [r.get("vibration_z", 0) for r in readings],
    }
    st.line_chart(chart_data)
else:
    st.warning("No data found!")