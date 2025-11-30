# main.py

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "✅ Codex2050 Render Bot läuft!"

if __name__ == '__main__':
    app.run()
