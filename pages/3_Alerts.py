import streamlit as st
from firebase_config import db

st.set_page_config(page_title="Alerts", layout="centered")

st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#ff4444;">🚨 Alerts</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

docs = db.collection("machines").document("motor_1") \
         .collection("readings") \
         .order_by("timestamp") \
         .limit_to_last(50) \
         .get()

readings = [doc.to_dict() for doc in docs]
faults = [r for r in readings if r.get("status") == "fault"]

if faults:
    st.markdown(f"""
        <div style="background-color:#4a1a1a; padding:15px; border-radius:10px; text-align:center;">
            <h3 style="color:#ff4444;">⚠️ {len(faults)} Fault(s) Detected!</h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for fault in reversed(faults):
        st.markdown(f"""
            <div style="background-color:#2a1a1a; padding:15px; border-radius:10px; margin-bottom:10px;">
                <p style="color:#ff4444;">⚠️ Fault Detected</p>
                <p style="color:#aaa;">🕒 Time: {fault.get("timestamp", "N/A")}</p>
                <p style="color:#aaa;">X: {fault.get("vibration_x")} | Y: {fault.get("vibration_y")} | Z: {fault.get("vibration_z")}</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="background-color:#1a2a1a; padding:15px; border-radius:10px; text-align:center;">
            <h3 style="color:#00ff88;">✅ No faults detected!</h3>
        </div>
    """, unsafe_allow_html=True)