
import logging
import os
from typing import Any, Dict

from flask import Flask, request, jsonify

from codex2050_engine import Codex2050Engine

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    # Wir loggen nur – der Service kann trotzdem bauen, aber nicht sinnvoll antworten.
    log.warning("TELEGRAM_TOKEN ist nicht gesetzt – Bot kann nicht mit Telegram sprechen.")

TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}" if TELEGRAM_TOKEN else None

app = Flask(__name__)
engine = Codex2050Engine()


def _telegram_request(method: str, payload: Dict[str, Any]) -> None:
    """Sende eine Anfrage an die Telegram Bot API; Fehler werden nur geloggt."""
    import requests  # lazy import, damit build schneller ist

    if not TELEGRAM_API_BASE:
        log.error("Kein TELEGRAM_TOKEN gesetzt, kann nicht zu Telegram senden.")
        return

    url = f"{TELEGRAM_API_BASE}/{method}"
    try:
        r = requests.post(url, json=payload, timeout=10)
        if not r.ok:
            log.error("Telegram API error %s: %s", r.status_code, r.text[:400])
    except Exception as exc:  # pragma: no cover – defensive
        log.error("Fehler beim Telegram-Request: %s", exc)


@app.route("/", methods=["GET"])
def index() -> Any:
    return "Codex2050 Render-Bot – alive", 200


@app.route("/webhook", methods=["POST"])
def telegram_webhook() -> Any:
    update = request.get_json(force=True, silent=True) or {}
    log.debug("Update: %s", update)

    message = update.get("message") or update.get("edited_message")
    if not message:
        return jsonify(ok=True)

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if not isinstance(chat_id, int):
        return jsonify(ok=True)

    text = message.get("text") or ""
    text = text.strip()

    if text.startswith("/"):
        if " " in text:
            cmd, arg = text.split(" ", 1)
        else:
            cmd, arg = text, None
        reply = engine.handle_command(chat_id, cmd, arg)
    else:
        reply = engine.handle_free_text(chat_id, text)

    _telegram_request("sendMessage", {"chat_id": chat_id, "text": reply})
    return jsonify(ok=True)


def main() -> None:
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
