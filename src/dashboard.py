import streamlit as st
import pandas as pd
import requests

# Load driver risk scores & premiums
df = pd.read_csv("data/driver_risk_scores.csv")  # already has risk & premium

st.set_page_config(page_title="Driver Risk Dashboard", layout="wide")
st.title("Driver Risk & Premium Dashboard!")


# badges
def assign_badge(risk_score):
    if risk_score < 30:
        return "🥇 Safe Driver"
    elif risk_score < 60:
        return "🥈 Moderate Risk"
    else:
        return "🥉 High Risk"

df["badge"] = df["predicted_risk"].apply(assign_badge)

# points game
def reward_points(risk_score):
    if risk_score < 30:
        return 100  # safe drivers earn more
    elif risk_score < 60:
        return 50
    else:
        return 10  # risky drivers earn less
df["rewards_points"] = df["predicted_risk"].apply(reward_points)

# tips

def driving_tips(row):
    tips = []
    if row["predicted_risk"] > 70:
        tips.append("⚠️ Try to avoid harsh braking and acceleration.")
    if row["predicted_risk"] < 30:
        tips.append("✅ Keep up your safe driving!")
    if "late_driving" in row and row["late_driving"] > 0.5:
        tips.append("🌙 Limit night driving when possible.")
    return " | ".join(tips) if tips else "👍 Average driving!"

df["tips"] = df.apply(driving_tips, axis=1)

# distribution charts
st.header("Dynamic Premium Distribution")
st.bar_chart(df.set_index("driver_id")["dynamic_premium"])

# select driver
driver_ids = df["driver_id"].tolist()
selected_driver = st.selectbox("Select a driver for a detailed view!", driver_ids)
driver_data = df[df["driver_id"] == selected_driver].iloc[0]

# Detailed Metrics
st.subheader(f"Driver: {selected_driver}")
st.metric("Predicted Risk (%)", driver_data["predicted_risk"])
st.metric("Dynamic Premium ($)", driver_data["dynamic_premium"])
st.metric("Badge", driver_data["badge"])
st.metric("Rewards Points", driver_data["rewards_points"])

# Personalized Tips
st.info(f"💡 Tip: {driver_data['tips']}")

# real time buttom calling api
API_URL = "http://127.0.0.1:8000/compute_risk"

if st.button("🔄 Refresh Real-Time Risk & Premium"):
    try:
        raw_df = pd.read_csv("data/clean_drivers.csv")
        driver_raw = raw_df[raw_df["driver_id"] == selected_driver].iloc[0].to_dict()
        payload = {
            "driver_id": driver_raw["driver_id"],
            "avg_speed": driver_raw["avg_speed"],
            "extreme_brakes": int(driver_raw["extreme_brakes"]),
            "extreme_accels": int(driver_raw["extreme_accels"]),
            "late_driving": driver_raw["late_driving"],
            "mileage": driver_raw["mileage"],
            "weather_conditions_foggy": driver_raw["weather_conditions_foggy"],
            "weather_conditions_rainy": driver_raw["weather_conditions_rainy"],
            "weather_conditions_snowy": driver_raw["weather_conditions_snowy"],
            "traffic_conditions_light": driver_raw["traffic_conditions_light"],
            "traffic_conditions_moderate": driver_raw["traffic_conditions_moderate"]
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Real-time update fetched!")
            st.metric("Predicted Risk (%)", result["predicted_risk"])
            st.metric("Dynamic Premium ($)", result["dynamic_premium"])
        else:
            st.error(f"API error: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")

# All drivers table
st.header("All Drivers Risk, Premiums, Badges, Points & Tips!")
st.dataframe(df[["driver_id", "predicted_risk", "dynamic_premium", "badge", "rewards_points", "tips"]])
