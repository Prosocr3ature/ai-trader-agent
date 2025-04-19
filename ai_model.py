import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from notifier import send_model_trained_alert

MODEL_PATH = "model_ensemble.pkl"
SCALER_PATH = "scaler.pkl"

def generate_advanced_mock_data(n=2000):
    data = []
    for _ in range(n):
        rsi = np.random.uniform(10, 90)
        ema_20 = np.random.uniform(30000, 60000)
        ema_50 = np.random.uniform(30000, 60000)
        macd = np.random.normal(0, 100)
        volatility = np.random.uniform(0.5, 5)
        candle_body = np.random.uniform(-300, 300)
        pattern_score = int(candle_body > 100) - int(candle_body < -100)
        label = "buy" if (rsi < 35 and macd > 0 and pattern_score == 1) else (
                "sell" if (rsi > 65 and macd < 0 and pattern_score == -1) else "ignore")
        data.append([rsi, ema_20, ema_50, macd, volatility, pattern_score, label])
    return pd.DataFrame(data, columns=["rsi", "ema_20", "ema_50", "macd", "volatility", "pattern_score", "label"])

def train_advanced_model():
    df = generate_advanced_mock_data()
    X = df.drop("label", axis=1)
    y = df["label"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    rf = RandomForestClassifier(n_estimators=100)
    gb = GradientBoostingClassifier(n_estimators=100)
    model = VotingClassifier(estimators=[("rf", rf), ("gb", gb)], voting='soft')
    model.fit(X_scaled, y)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    send_model_trained_alert()

def predict_advanced_action(feature_dict):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        train_advanced_model()
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    X = pd.DataFrame([feature_dict])
    X_scaled = scaler.transform(X)
    return model.predict(X_scaled)[0]
