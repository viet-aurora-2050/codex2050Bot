# Codex2050 Render Bot – Stufen 1–6 (Final3)

Dieses Paket enthält den kompletten Code für deinen **AURORA / Codex2050 Render‑Bot**.

**Stack**
- Render.com (Python Web Service)
- Telegram Bot (per Webhook)
- Reiner Flask‑Server + `requests` (kein großes Bot-Framework)

## Dateien

- `main.py` – Flask‑Server + Telegram‑Webhook
- `codex2050_engine.py` – Kernlogik & Texte der Stufen 1–6
- `codex2050_modes.py` – Routing der Nachrichten in die einzelnen Stufen
- `requirements.txt` – Python‑Abhängigkeiten
- `render.yaml` – Deploy‑Konfiguration für Render

---

## Deployment auf Render (Kurzfassung)

1. Neues GitHub‑Repo anlegen und **alle Dateien aus diesem ZIP** hochladen.
2. Auf Render.com:
   - „New Web Service“ → GitHub‑Repo auswählen
   - Python‑Runtime auswählen
   - `render.yaml` wird automatisch erkannt (Infrastructure as Code)
3. Environment‑Variablen setzen:
   - `TELEGRAM_TOKEN` = dein Bot‑Token von BotFather
   - `WEBHOOK_URL`   = HTTPS‑URL deines Render‑Services + `/webhook`
     (z. B. `https://codex2050-render-final.onrender.com/webhook`)
4. Deploy starten. Wenn der Build durch ist, sollte der Bot online sein.
5. In Telegram `/start` an deinen Bot schicken.

---

## Notizen

- Wenn `WEBHOOK_URL` **nicht** gesetzt ist, startet der Bot trotzdem
  und loggt nur eine Warnung.
- Die Antworten sind bewusst kurz gehalten und referenzieren nur
  deinen bestehenden Codex 2050, ohne irgendwelche geheimen Daten.
