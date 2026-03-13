import streamlit as st
import pandas as pd

st.title("📜 Sensor History")

if "buffer" not in st.session_state or len(st.session_state.buffer) == 0:
    st.warning("No history available yet.")
    st.stop()

df = pd.DataFrame(st.session_state.buffer)

st.dataframe(df)