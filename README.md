
# Codex2050 Render Bot – Stufen 1–6

Dieser Bot läuft auf **Render.com** als Python‑Webservice und verbindet sich per Webhook mit Telegram.
Er bündelt alle 6 Stufen (Codex‑2050‑Modus) in einem kleinen Engine‑Modul – komplett ohne externe
KI‑API. Alles bleibt lokal im Prozess.

## Dateien

- `main.py` – Flask‑Server + Telegram‑Webhook
- `codex2050_engine.py` – Logik für Stufen, Status & Texte
- `codex2050_modes.py` – Definition der 6 Stufen (Titel, Kurzbeschreibung, Erklärung)
- `requirements.txt` – Python‑Abhängigkeiten
- `render.yaml` – Beispiel‑Konfiguration für Render

## Umgebungsvariablen

Auf Render **muss** gesetzt sein:

- `TELEGRAM_TOKEN` – dein Bot‑Token von BotFather
- `PORT` – wird von Render meist automatisch gesetzt; wenn nötig: `10000`

## Webhook setzen

Wenn der Service läuft und eine öffentliche URL hat, z.B.:

`https://codex2050-render-final.onrender.com`

kannst du den Webhook im Browser setzen (oder per curl):

`https://api.telegram.org/bot<DEIN_TOKEN>/setWebhook?url=https://codex2050-render-final.onrender.com/webhook`

Danach schickt Telegram alle Updates an deinen Render‑Service.

## Nutzung in Telegram

Befehle:

- `/start` – Einstieg & Überblick
- `/help` – kurze Hilfe
- `/stufen` – Liste der Stufen 1–6
- `/mode <1-6>` – aktuelle Stufe setzen, z.B. `/mode 3`
- `/status` – zeigt aktuelle Stufe + letzte Notiz

Alles andere, was du schreibst, wird als freier Text in die aktuelle Stufe einsortiert.
