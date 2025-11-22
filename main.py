
import logging
import os

from flask import Flask, jsonify, request

from codex2050_modes import load_config
from codex2050_engine import process_update

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    cfg = load_config()
    return jsonify(
        {
            "status": "ok",
            "message": "Codex2050 Render-Bot Webhook",
            "stage": cfg.stage,
        }
    )


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    cfg = load_config()
    try:
        update = request.get_json(force=True, silent=False) or {}
    except Exception as e:
        logger.error("Webhook JSON-Fehler: %s", e)
        return "bad request", 400

    logger.info("Update erhalten: %s", update)
    replies = process_update(update, cfg)

    # Antworten an Telegram schicken
    token = os.getenv("TELEGRAM_TOKEN", "").strip()
    if not token:
        logger.error("TELEGRAM_TOKEN ist nicht gesetzt.")
        return "no token", 500

    import requests

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"

    chat_id = None
    if "message" in update:
        chat_id = update["message"].get("chat", {}).get("id")

    if chat_id is None:
        logger.warning("Kein chat_id im Update gefunden.")
        return "no chat", 200

    for text in replies:
        try:
            resp = requests.post(
                api_url,
                json={"chat_id": chat_id, "text": text},
                timeout=10,
            )
            if resp.status_code != 200:
                logger.error("Fehler beim Senden an Telegram: %s %s", resp.status_code, resp.text)
        except Exception as e:
            logger.error("HTTP-Fehler Richtung Telegram: %s", e)

    return "ok", 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
