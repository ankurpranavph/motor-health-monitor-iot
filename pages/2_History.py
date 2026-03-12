import streamlit as st
from firebase_config import db

st.set_page_config(page_title="Reading History", layout="centered")

st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#00ffcc;">📋 Reading History</h1>
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
    st.markdown(f"<p style='color:#aaa;'>Showing last {len(readings)} readings</p>", unsafe_allow_html=True)
    st.dataframe(readings, use_container_width=True)

    # Summary stats
    st.markdown("<h3 style='color:#00ffcc;'>📊 Summary</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    normal_count = sum(1 for r in readings if r.get("status") == "normal")
    fault_count = sum(1 for r in readings if r.get("status") == "fault")
    col1.metric("Total Readings", len(readings))
    col2.metric("✅ Normal", normal_count)
    col3.metric("⚠️ Faults", fault_count)
else:
    st.warning("No data found!")