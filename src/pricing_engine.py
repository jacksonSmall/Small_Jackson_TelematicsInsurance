import pandas as pd


df = pd.read_csv("data/driver_risk_scores.csv")

# constant base premium
BASE_PREMIUM = 500  

RISK_WEIGHT = 0.5  

def calculate_premium(risk_score_percent):
    risk_factor = risk_score_percent / 100  # normalize to 0-1
    premium = BASE_PREMIUM * (1 + risk_factor * RISK_WEIGHT)
    return round(premium, 2)

# set for all drivers
df["premium"] = df["predicted_risk"].apply(calculate_premium)
df[["driver_id", "predicted_risk", "premium"]].to_csv("data/driver_premiums.csv", index=False)

# print("Dynamic premiums calculated and saved to 'driver_premiums.csv'.")
