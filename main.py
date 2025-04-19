from fastapi import FastAPI, Request, HTTPException
from trade_logic import process_signal
from db import log_trade
from notifier import send_trade_alert, send_sell_alert
from portfolio import close_position

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Webhook received:", data)  # Lägg till denna rad
    result = process_signal(data)
    print("Processed signal:", result)  # Lägg till denna också
    if result["status"] == "executed":
        log_trade(result)
        send_trade_alert(result)
    return {"received": True, "result": result}

@app.post("/close")
async def close_trade(payload: dict):
    ticker = payload.get("ticker")
    price = float(payload.get("price", 0))
    if not ticker or price <= 0:
        raise HTTPException(status_code=400, detail="Invalid ticker or price")
    pnl = close_position(ticker, price)
    if pnl is not None:
        send_sell_alert(ticker, price, pnl)
        return {"status": "closed", "ticker": ticker, "pnl": pnl}
    else:
        raise HTTPException(status_code=404, detail="No open position for ticker")

@app.get("/")
def healthcheck():
    return {"status": "AI trader running"}
