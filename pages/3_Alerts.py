import streamlit as st
import pandas as pd
import math

st.title("🚨 Alerts")

if "buffer" not in st.session_state or len(st.session_state.buffer) == 0:
    st.warning("No data available yet.")
    st.stop()

latest = st.session_state.buffer[-1]

x = latest["vibration_x"]
y = latest["vibration_y"]
z = latest["vibration_z"]

mag = math.sqrt(x*x + y*y + z*z)
vibration = abs(mag - 1)

if vibration > 0.35:
    st.error("🔴 Fault detected")

elif vibration > 0.15:
    st.warning("🟡 High vibration warning")

else:
    st.success("🟢 Motor operating normally")