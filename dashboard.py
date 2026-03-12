import streamlit as st
import time
import pandas as pd
from firebase_config import db

st.set_page_config(page_title="Motor Health Monitor", layout="centered")

# HTML Title Banner
st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#00ffcc; font-family:Arial;">🔧 Motor Health Monitor</h1>
        <p style="color:#aaa;">Real-time vibration monitoring system</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

while True:
    docs = db.collection("machines").document("motor_1") \
             .collection("readings") \
             .order_by("timestamp") \
             .limit_to_last(20) \
             .get()

    readings = [doc.to_dict() for doc in docs]

    if readings:
        latest = readings[-1]
        status = latest.get("status", "unknown")

        # ── Motor Health Score ──────────────────────────────
        normal_count = sum(1 for r in readings if r.get("status") == "normal")
        fault_count  = sum(1 for r in readings if r.get("status") == "fault")
        total        = len(readings)
        health_score = int((normal_count / total) * 100) if total > 0 else 0

        if health_score >= 80:
            score_color = "#00ff88"
            score_label = "Healthy"
        elif health_score >= 50:
            score_color = "#ffcc00"
            score_label = "Warning"
        else:
            score_color = "#ff4444"
            score_label = "Critical"

        st.markdown(f"""
            <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
                <h3 style="color:#aaa;">🏥 Motor Health Score</h3>
                <h1 style="color:{score_color}; font-size:60px;">{health_score}%</h1>
                <h3 style="color:{score_color};">{score_label}</h3>
                <div style="background-color:#333; border-radius:10px; height:25px; margin-top:10px;">
                    <div style="background-color:{score_color}; width:{health_score}%; height:25px; border-radius:10px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Status Card ─────────────────────────────────────
        if status == "normal":
            st.markdown("""
                <div style="background-color:#1a472a; padding:15px; border-radius:10px; text-align:center;">
                    <h2 style="color:#00ff88;">✅ Motor Status: NORMAL</h2>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color:#4a1a1a; padding:15px; border-radius:10px; text-align:center;">
                    <h2 style="color:#ff4444;">⚠️ Motor Status: FAULT DETECTED</h2>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Popup Alert on Fault ────────────────────────────
        if status == "fault":
            st.error("🚨 ALERT: Abnormal vibration detected! Maintenance recommended immediately!")
            st.toast("⚠️ Fault detected on Motor 1!", icon="🚨")

        # ── Fault vs Normal Counter ─────────────────────────
        normal_pct = int((normal_count / total) * 100) if total > 0 else 0
        fault_pct  = int((fault_count  / total) * 100) if total > 0 else 0

        st.markdown("<h3 style='color:#00ffcc;'>📊 Reading Summary</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="display:flex; gap:10px; justify-content:center;">
                <div style="background-color:#1a472a; padding:20px; border-radius:10px; text-align:center; flex:1;">
                    <h4 style="color:#aaa;">✅ Normal</h4>
                    <h2 style="color:#00ff88;">{normal_count}</h2>
                    <p style="color:#aaa;">{normal_pct}% of readings</p>
                </div>
                <div style="background-color:#4a1a1a; padding:20px; border-radius:10px; text-align:center; flex:1;">
                    <h4 style="color:#aaa;">⚠️ Faults</h4>
                    <h2 style="color:#ff4444;">{fault_count}</h2>
                    <p style="color:#aaa;">{fault_pct}% of readings</p>
                </div>
                <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center; flex:1;">
                    <h4 style="color:#aaa;">📋 Total</h4>
                    <h2 style="color:#00ffcc;">{total}</h2>
                    <p style="color:#aaa;">readings stored</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Vibration Gauge ─────────────────────────────────
        x = round(latest.get("vibration_x", 0), 3)
        y = round(latest.get("vibration_y", 0), 3)
        z = round(latest.get("vibration_z", 0), 3)

        st.markdown("<h3 style='color:#00ffcc;'>📉 Vibration Gauge</h3>", unsafe_allow_html=True)

        def gauge_color(val):
            if val < 0.2:   return "#00ff88"
            elif val < 0.4: return "#ffcc00"
            else:           return "#ff4444"

        def gauge_bar(label, val, max_val=1.0):
            pct   = min(int((abs(val) / max_val) * 100), 100)
            color = gauge_color(abs(val))
            return f"""
                <div style="background-color:#1e1e2e; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <p style="color:#aaa; margin:0;">{label} Axis — <span style="color:{color};">{val}</span></p>
                    <div style="background-color:#333; border-radius:5px; height:20px; margin-top:8px;">
                        <div style="background-color:{color}; width:{pct}%; height:20px; border-radius:5px;"></div>
                    </div>
                </div>
            """

        st.markdown(gauge_bar("X", x), unsafe_allow_html=True)
        st.markdown(gauge_bar("Y", y), unsafe_allow_html=True)
        st.markdown(gauge_bar("Z", z), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Vibration Value Cards ───────────────────────────
        st.markdown(f"""
            <div style="display:flex; gap:10px; justify-content:center;">
                <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center; flex:1;">
                    <h4 style="color:#aaa;">X Axis</h4>
                    <h2 style="color:#00ffcc;">{x}</h2>
                </div>
                <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center; flex:1;">
                    <h4 style="color:#aaa;">Y Axis</h4>
                    <h2 style="color:#00ffcc;">{y}</h2>
                </div>
                <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center; flex:1;">
                    <h4 style="color:#aaa;">Z Axis</h4>
                    <h2 style="color:#00ffcc;">{z}</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Vibration Graph ─────────────────────────────────
        st.markdown("<h3 style='color:#00ffcc;'>📈 Vibration Graph</h3>", unsafe_allow_html=True)
        chart_data = {
            "X": [r.get("vibration_x", 0) for r in readings],
            "Y": [r.get("vibration_y", 0) for r in readings],
            "Z": [r.get("vibration_z", 0) for r in readings],
        }
        st.line_chart(chart_data)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Download CSV Button ─────────────────────────────
        st.markdown("<h3 style='color:#00ffcc;'>📥 Export Data</h3>", unsafe_allow_html=True)
        df = pd.DataFrame(readings)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Readings as CSV",
            data=csv,
            file_name="motor_readings.csv",
            mime="text/csv"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Recent Readings Table ───────────────────────────
        st.markdown("<h3 style='color:#00ffcc;'>📋 Recent Readings</h3>", unsafe_allow_html=True)
        st.dataframe(readings)

    else:
        st.markdown("""
            <div style="background-color:#2a2a1a; padding:15px; border-radius:10px; text-align:center;">
                <h3 style="color:#ffcc00;">⚡ Waiting for data from Firebase...</h3>
            </div>
        """, unsafe_allow_html=True)

    time.sleep(2)
    st.rerun()