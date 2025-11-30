from flask import Flask, request, render_template
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    app.logger.info(f"Webhook empfangen: {data}")
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run()