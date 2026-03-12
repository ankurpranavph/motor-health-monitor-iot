import streamlit as st

st.set_page_config(page_title="About", layout="centered")

st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#00ffcc;">ℹ️ About This Project</h1>
    </div>

    <br>

    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px;">
        <h3 style="color:#00ffcc;">🔧 What This System Does</h3>
        <p style="color:#aaa;">This system monitors motor vibration in real-time using an MPU6050 sensor attached to an ESP32 microcontroller. It detects abnormal vibration patterns and predicts potential motor failures before they happen.</p>
    </div>

    <br>

    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px;">
        <h3 style="color:#00ffcc;">⚙️ Tech Stack</h3>
        <p style="color:#aaa;">🔌 Hardware: ESP32 + MPU6050 Accelerometer</p>
        <p style="color:#aaa;">☁️ Cloud: Firebase Firestore</p>
        <p style="color:#aaa;">🐍 Backend: Python</p>
        <p style="color:#aaa;">🤖 ML Model: Random Forest / Isolation Forest</p>
        <p style="color:#aaa;">📊 Dashboard: Streamlit</p>
    </div>

    <br>

    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px;">
        <h3 style="color:#00ffcc;">🎯 What It Achieves</h3>
        <p style="color:#aaa;">✅ Continuous motor vibration monitoring</p>
        <p style="color:#aaa;">✅ Real-time fault detection</p>
        <p style="color:#aaa;">✅ Early maintenance alerts</p>
        <p style="color:#aaa;">✅ Reduces machine downtime and costs</p>
    </div>
""", unsafe_allow_html=True)