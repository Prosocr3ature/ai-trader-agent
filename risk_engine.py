from portfolio import load_portfolio, close_position
from notifier import send_sell_alert

def evaluate_risk(current_prices: dict):
    pf = load_portfolio()
    for pos in pf["positions"]:
        ticker = pos["ticker"]
        entry = pos["price"]
        current = current_prices.get(ticker)
        if not current:
            continue

        pnl_pct = (current - entry) / entry

        if pnl_pct >= 0.03:  # take profit
            pnl = close_position(ticker, current)
            send_sell_alert(ticker, current, pnl)

        elif pnl_pct <= -0.015:  # stop loss
            pnl = close_position(ticker, current)
            send_sell_alert(ticker, current, pnl)
