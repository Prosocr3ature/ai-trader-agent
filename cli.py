import argparse
from portfolio import get_balance, load_portfolio, close_position
from notifier import send_sell_alert

parser = argparse.ArgumentParser(description="AI Trader CLI")
parser.add_argument("--balance", action="store_true")
parser.add_argument("--positions", action="store_true")
parser.add_argument("--close", nargs=2, metavar=("TICKER", "PRICE"))
args = parser.parse_args()

if args.balance:
    print(f"USDT balans: {get_balance():.2f}")

if args.positions:
    for p in load_portfolio()["positions"]:
        print(f"{p['ticker']} @ {p['price']} | Amount: {p['amount']}")

if args.close:
    ticker, price = args.close
    pnl = close_position(ticker, float(price))
    if pnl is not None:
        send_sell_alert(ticker, float(price), pnl)
        print(f"{ticker} stängd. PnL: {pnl:.2f}%")
    else:
        print(f"Ingen position hittad för {ticker}")
