import os
import logging
from flask import Flask, request
import telebot

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Codex2050 Render Bot läuft."

@app.route("/", methods=["POST"])
def webhook():
    json_update = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start_msg(message):
    bot.reply_to(message, "Codex2050 Render-Bot ist aktiv 🔥")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    WEBHOOK_URL = f"https://{hostname}/"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=port)
