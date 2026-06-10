import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="IoT Threat Detection Dashboard", layout="wide")

st.title("IoT Threat Detection Dashboard")
st.write("Real-time visual detection of IoT network threats")

API_URL = "http://127.0.0.1:5000/predict"

# Store history
if "history" not in st.session_state:
    st.session_state.history = []

# Example traffic generator
def generate_sample_data():
    return [random.random() for _ in range(46)]

# Simple severity mapping
def get_severity(label):
    if "Benign" in label:
        return "Low"
    elif "DDoS" in label or "DoS" in label:
        return "High"
    elif "Mirai" in label or "Bot" in label:
        return "High"
    else:
        return "Medium"

# Run prediction
if st.button("Run Detection"):
    data = [0.0] * 46   # you can replace this later with real live data

    try:
        response = requests.post(API_URL, json={"data": data})

        if response.status_code == 200:
            result = response.json()["prediction"]
            severity = get_severity(result)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.session_state.history.append({
                "Time": now,
                "Prediction": result,
                "Severity": severity,
                "Status": "Normal" if "Benign" in result else "Attack"
            })

        else:
            st.error("Prediction request failed.")

    except Exception as e:
        st.error(f"Connection error: {e}")

# Latest result
if st.session_state.history:
    latest = st.session_state.history[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Latest Detection", latest["Prediction"])

    with col2:
        st.metric("Severity", latest["Severity"])

    with col3:
        st.metric("Status", latest["Status"])

    if latest["Status"] == "Normal":
        st.success(f"Normal Traffic Detected ✅ : {latest['Prediction']}")
    else:
        st.error(f"Attack Detected 🚨 : {latest['Prediction']}")

    df = pd.DataFrame(st.session_state.history)

    st.subheader("Detection History")
    st.dataframe(df, use_container_width=True)

    st.subheader("Detection Count by Type")
    count_df = df["Prediction"].value_counts().reset_index()
    count_df.columns = ["Prediction", "Count"]
    st.bar_chart(count_df.set_index("Prediction"))

    st.subheader("Normal vs Attack")
    status_counts = df["Status"].value_counts()
    st.bar_chart(status_counts)

else:
    st.info("No detections yet. Click 'Run Detection' to begin.")
