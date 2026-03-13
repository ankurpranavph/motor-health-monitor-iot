import streamlit as st
import pandas as pd

st.title("📈 Sensor Graphs")

if "buffer" not in st.session_state or len(st.session_state.buffer) == 0:
    st.warning("No data available yet.")
    st.stop()

df = pd.DataFrame(st.session_state.buffer)

st.subheader("Acceleration")

st.line_chart(df[[
    "vibration_x",
    "vibration_y",
    "vibration_z"
]])

st.subheader("Gyroscope")

st.line_chart(df[[
    "gyro_x",
    "gyro_y",
    "gyro_z"
]])

st.subheader("Power")

st.line_chart(df[[
    "current_ma",
    "voltage_v",
    "power_mw"
]])