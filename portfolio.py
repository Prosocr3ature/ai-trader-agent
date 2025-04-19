import os
import json

PORTFOLIO_FILE = "portfolio.json"

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    else:
        return {"USDT": 10000, "positions": []}

def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_balance():
    pf = load_portfolio()
    return pf["USDT"]

def add_position(ticker, price, amount):
    pf = load_portfolio()
    pf["positions"].append({"ticker": ticker, "price": price, "amount": amount})
    pf["USDT"] -= price * amount
    save_portfolio(pf)

def close_position(ticker, sell_price):
    pf = load_portfolio()
    position = next((p for p in pf["positions"] if p["ticker"] == ticker), None)
    if position:
        pnl = ((sell_price - position["price"]) / position["price"]) * 100
        pf["USDT"] += sell_price * position["amount"]
        pf["positions"].remove(position)
        save_portfolio(pf)
        return round(pnl, 2)
    return None
