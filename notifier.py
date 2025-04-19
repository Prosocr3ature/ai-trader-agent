import os
import telegram
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_trade_alert(trade_data):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        msg = (
            f"**AI TRADE ALERT**\n"
            f"Asset: {trade_data['ticker']}\n"
            f"Action: {trade_data['action'].upper()} @ ${trade_data['price']}\n"
            f"Confidence: {trade_data['confidence']:.2f}\n"
            f"AI Decision: {trade_data['ai_decision'].upper()}\n"
            f"Status: {trade_data['status'].upper()}"
        )
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

def send_sell_alert(ticker, price, pnl=None):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        msg = (
            f"**SELL EXECUTED**\n"
            f"{ticker} @ ${price}\n"
            f"{f'PnL: {pnl:.2f}%' if pnl is not None else ''}"
        )
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

def send_model_trained_alert():
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="**AI MODEL UPDATED**")

def send_system_status(message="AI-agenten är aktiv."):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"[STATUS]\n{message}")
