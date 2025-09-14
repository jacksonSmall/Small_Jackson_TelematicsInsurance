import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report

# Load data
df = pd.read_csv('data/clean_drivers.csv')

# POC risk formula
risk = (
    0.03 * df['avg_speed'] +
    0.05 * df['extreme_brakes'] +
    0.05 * df['extreme_accels'] +
    0.1 * df['late_driving'] +
    0.07 * df['weather_conditions_rainy'] +
    df['weather_conditions_foggy'] +
    df['weather_conditions_snowy'] +
    0.05 * (1 - df['traffic_conditions_light']) -
    0.02 * df['mileage']
)

# Normalize to 0-1
risk_p = (risk - risk.min()) / (risk.max() - risk.min())

# Assign binary risk label
df['risk'] = np.where(risk_p > 0.5, 1, 0)


X = df.drop(columns=['driver_id', 'risk'])
y = df['risk']

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=21)

# LR
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)
y_pred_p_lr = lr_model.predict_proba(X_test)[:, 1]

auc_lr = roc_auc_score(y_test, y_pred_p_lr)
print("LOGISTIC REGRESSION")
print(f"LR ROC AUC: {auc_lr:.4f}")
print(classification_report(y_test, lr_model.predict(X_test)))

# rf 
rf_model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=21)
rf_model.fit(X_train, y_train)
y_pred_p_rf = rf_model.predict_proba(X_test)[:, 1]

auc_rf = roc_auc_score(y_test, y_pred_p_rf)
print("RANDOM FOREST")
print(f"RF ROC AUC: {auc_rf:.4f}")
print(classification_report(y_test, rf_model.predict(X_test)))

# preds
df["predicted_risk"] = lr_model.predict_proba(X_scaled)[:, 1] * 100  # 0-100

# dynamic prem calc
BASE_PREMIUM = 500
RISK_WEIGHT = 0.5
df["dynamic_premium"] = round(BASE_PREMIUM * (1 + df["predicted_risk"]/100 * RISK_WEIGHT), 2)

# save
df_out = df[["driver_id", "predicted_risk", "risk", "dynamic_premium"]]
df_out.to_csv("data/driver_risk_scores.csv", index=False)

#print("Driver risk scoring and dynamic premium calculation completed.")
#print("Data saved to 'driver_risk_scores.csv'")
