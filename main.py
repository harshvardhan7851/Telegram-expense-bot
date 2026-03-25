from fastapi import FastAPI, Request
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from fastapi.responses import HTMLResponse
from io import BytesIO
import base64
from dotenv import load_dotenv

from db_operations import add_expense
from database import engine
from sqlalchemy import text

load_dotenv()

app = FastAPI()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


# Send message back to Telegram
def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(TELEGRAM_URL, json=payload)


# Telegram webhook
@app.post("/telegram")
async def telegram_webhook(request: Request):

    data = await request.json()

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # Commands
    if text == "/start":
        send_message(
            chat_id,
            "👋 Welcome to Expense Tracker Bot\n\nSend expense like:\n\nLunch 200"
        )
        return {"status": "ok"}

    if text == "/summary":

        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT SUM(amount) FROM expenses WHERE chat_id=:chat_id"),
                {"chat_id": chat_id}
            ).fetchone()

        total = result[0] if result[0] else 0

        send_message(chat_id, f"💰 Total Spending: ₹{total}")

        return {"status": "ok"}

    # Expense message
    try:

        parts = text.split()

        description = parts[0]
        amount = float(parts[1])

        add_expense(chat_id, description, amount)

        send_message(chat_id, f"✅ Expense added: {description} ₹{amount}")

    except:
        send_message(chat_id, "❌ Format: Lunch 200")

    return {"status": "ok"}


# Dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT description, amount, created_at FROM expenses")
        )

        rows = result.fetchall()

    if not rows:
        return "<h2>No data available</h2>"

    df = pd.DataFrame(rows, columns=["Description", "Amount", "Date"])

    df["Date"] = pd.to_datetime(df["Date"])

    daily = df.groupby(df["Date"].dt.date)["Amount"].sum()

    total_spent = df["Amount"].sum()
    avg_daily = daily.mean()

    plt.figure()
    daily.plot(kind="bar")
    plt.title("Daily Spending")
    plt.xticks(rotation=45)

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode()

    html = f"""
    <h1>Expense Analytics Dashboard</h1>
    <h3>Total Spent: ₹{total_spent}</h3>
    <h3>Average Daily Spend: ₹{avg_daily:.2f}</h3>
    <img src="data:image/png;base64,{image_base64}">
    """

    return html


# Run server
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)