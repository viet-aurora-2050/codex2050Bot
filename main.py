
from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

BOT_TOKEN = "8382425226:AAETkrUYDXJA39PekDhs_Iyxnl1LhRSwaYQ"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.post("/")
async def telegram_webhook(request: Request):
    data = await request.json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        async with httpx.AsyncClient() as client:
            await client.post(
                f"{TELEGRAM_API}/sendMessage",
                json={"chat_id": chat_id, "text": f"Sancho 2050 empfängt: {text}"}
            )

    return {"ok": True}
