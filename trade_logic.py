import pandas as pd
import numpy as np
import random
from datetime import datetime
import os
from ai_model import predict_advanced_action
from portfolio import get_balance, add_position
from notifier import send_system_status

def compute_rsi(series, window=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def compute_macd(series, fast=12, slow=26):
    return compute_ema(series, fast) - compute_ema(series, slow)

def compute_volatility(series, window=10):
    return series.pct_change().rolling(window).std() * 100

def extract_features_from_ohlcv(df):
    df["rsi"] = compute_rsi(df["close"])
    df["ema_20"] = compute_ema(df["close"], 20)
    df["ema_50"] = compute_ema(df["close"], 50)
    df["macd"] = compute_macd(df["close"])
    df["volatility"] = compute_volatility(df["close"])
    df["candle_body"] = df["close"] - df["open"]
    df["pattern_score"] = df["candle_body"].apply(lambda x: 1 if x > 100 else (-1 if x < -100 else 0))
    return df.dropna().iloc[-1]

def generate_mock_ohlcv(n=100):
    prices = np.cumsum(np.random.randn(n) * 50) + 50000
    return pd.DataFrame({
        "open": prices + np.random.randn(n) * 5,
        "high": prices + np.random.rand(n) * 10,
        "low": prices - np.random.rand(n) * 10,
        "close": prices,
        "volume": np.random.randint(100, 1000, size=n)
    })

def process_signal(data: dict) -> dict:
    return {
        "time": data["time"],
        "ticker": data["ticker"],
        "action": data["action"],
        "confidence": data["confidence"],
        "price": 65300.0,  # <-- Lägg till dummypris
        "ai_decision": "buy",
        "status": "executed"
    }
    
    df = generate_mock_ohlcv()
    features = extract_features_from_ohlcv(df)
    feature_dict = {
        "rsi": features["rsi"],
        "ema_20": features["ema_20"],
        "ema_50": features["ema_50"],
        "macd": features["macd"],
        "volatility": features["volatility"],
        "pattern_score": features["pattern_score"]
    }

    ai_decision = predict_advanced_action(feature_dict)
    combined_score = confidence + int(ai_decision == "buy")

    if combined_score >= threshold and ai_decision == "buy":
        balance = get_balance()
        if balance < 100:
            send_system_status(f"⚠️ Låg balans: {balance:.2f} USDT. Trade avbröts.")
            return {"status": "ignored", "reason": "Insufficient balance", "balance": balance}
        
        simulated_price = round(random.uniform(30000, 60000), 2)
        amount = round(100 / simulated_price, 4)
        add_position(ticker, simulated_price, amount)
        stop_loss_pct = float(os.getenv("STOP_LOSS_PCT", 0.015))
        trailing_stop_pct = float(os.getenv("TRAILING_STOP_PCT", 0.02))
        stop_loss = round(simulated_price * (1 - stop_loss_pct), 2)
        trailing_stop = round(simulated_price * (1 + trailing_stop_pct), 2)

        return {
            "time": time,
            "ticker": ticker,
            "action": action,
            "price": simulated_price,
            "stop_loss": stop_loss,
            "trailing_stop": trailing_stop,
            "confidence": confidence,
            "ai_decision": ai_decision,
            "status": "executed"
        }

    return {
        "time": time,
        "ticker": ticker,
        "action": action,
        "confidence": confidence,
        "ai_decision": ai_decision,
        "status": "ignored"
    }
