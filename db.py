import sqlite3

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            ticker TEXT,
            action TEXT,
            price REAL,
            confidence REAL,
            ai_decision TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_trade(trade_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trades (time, ticker, action, price, confidence, ai_decision, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        trade_data["time"],
        trade_data["ticker"],
        trade_data["action"],
        trade_data["price"],
        trade_data["confidence"],
        trade_data["ai_decision"],
        trade_data["status"]
    ))
    conn.commit()
    conn.close()

init_db()
