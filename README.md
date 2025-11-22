
# Codex2050 Render Bot – Stufen 1–6

Dieser Bot ist für **Render.com + Telegram** gebaut und bündelt alle 6 Stufen
(Codex-2050-Modus) in einem einzigen Deployment.

## Dateien

- `main.py` – Flask-Webserver, Webhook-Endpunkt für Telegram, Stufen-Controller
- `codex2050_engine.py` – Kernlogik für Antworten (Schutz, Echo, Filter etc.)
- `codex2050_modes.py` – Definition der Stufen 1–6 und welche Features aktiv sind
- `requirements.txt` – Python-Abhängigkeiten
- `render.yaml` – Render-Deploy-Konfiguration (Web Service, Python 3)

## Environment Variablen

Auf Render **müssen** mindestens gesetzt werden:

- `TELEGRAM_TOKEN` – dein Bot-Token vom BotFather
- `CODEX2050_STAGE` – höchste aktivierte Stufe (1–6), z.B. `6`
- `OPENAI_API_KEY` – optional, nur für Stufe 6 (Full‑AI‑Bridge)

## Webhook

Nach dem ersten erfolgreichen Deploy musst du beim BotFather das Webhook-Ziel setzen:

`https://DEIN-SERVICE-NAME.onrender.com/webhook`

(Die Domain siehst du im Render-Dashboard unter „Service Address“.)

Danach reagiert der Bot auf `/start` und normale Nachrichten.

Die Stufen im Überblick:

1. **Online‑Echo** – Basis-Webhook, `/start`, einfache Echos.
2. **Schutzfilter** – blockiert Scam/Spam‑Links und Müll.
3. **Autonomer Antwortmodus** – einfache Auto‑Antworten auf Codex‑Kommandos.
4. **Archiv‑Hook** – schreibt kompakte Log‑Einträge in `codex2050_log.txt`.
5. **Monitoring & Rate‑Limit** – schützt vor Spam/Flut.
6. **Full‑AI‑Bridge** – wenn `OPENAI_API_KEY` gesetzt ist, werden komplexe Fragen an OpenAI durchgereicht.

Alle Stufen 1–N sind aktiv, wenn `CODEX2050_STAGE = N` gesetzt ist.
