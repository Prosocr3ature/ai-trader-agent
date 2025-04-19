import time
from risk_engine import evaluate_risk
from notifier import send_system_status

def get_mock_prices():
    return {
        "BTCUSDT": 50000 + (500 * (0.5 - time.time() % 2)),
        "ETHUSDT": 3100 + (100 * (0.5 - time.time() % 2))
    }

def run_loop(interval=60):
    send_system_status("Risk Engine är igång.")
    while True:
        prices = get_mock_prices()
        evaluate_risk(prices)
        time.sleep(interval)

if __name__ == "__main__":
    run_loop()
