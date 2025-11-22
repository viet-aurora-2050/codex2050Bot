
import json
import logging
import os
import re
import time
from typing import Dict, Any, List

from codex2050_modes import Codex2050Config

logger = logging.getLogger(__name__)

# einfache In-Memory-Rate-Limit-Struktur
_rate_limit_state: Dict[int, List[float]] = {}


SCAM_PATTERNS = [
    r"premium_gift",
    r"free\s+telegram\s+premium",
    r"ordershunter",
    r"crypto\s+giveaway",
]


def _looks_like_scam(text: str) -> bool:
    t = text.lower()
    for pattern in SCAM_PATTERNS:
        if re.search(pattern, t):
            return True
    return False


def _check_rate_limit(user_id: int, window_seconds: int = 30, max_msgs: int = 6) -> bool:
    # True = OK, False = zu viele Nachrichten
    now = time.time()
    history = _rate_limit_state.get(user_id, [])
    history = [ts for ts in history if now - ts < window_seconds]
    history.append(now)
    _rate_limit_state[user_id] = history
    return len(history) <= max_msgs


def _archiv_log(entry: Dict[str, Any]) -> None:
    try:
        line = json.dumps(entry, ensure_ascii=False)
        with open("codex2050_log.txt", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        logger.warning("Archiv-Log Fehler: %s", e)


def _call_openai(prompt: str) -> str:
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return "Stufe 6 (Full‑AI) ist vorbereitet, aber es wurde kein OPENAI_API_KEY gesetzt."

        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist der interaktive Kern von Codex2050. Antworte kurz, klar und hilfreich auf Deutsch.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=350,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logger.error("OpenAI Fehler: %s", e)
        return "Full‑AI-Brücke ist aktiv, aber es gab einen Fehler beim Zugriff auf das OpenAI‑API."


def process_update(update: Dict[str, Any], cfg: Codex2050Config) -> List[str]:
    # Nimmt ein Telegram-Update (JSON) und gibt eine Liste von Antwort-Texten zurück.
    messages: List[str] = []

    if "message" not in update:
        return messages

    msg = update["message"]
    chat_id = msg.get("chat", {}).get("id")
    user_id = msg.get("from", {}).get("id")
    text = msg.get("text") or ""

    # Stage 4: Archiv-Hook
    if cfg.stage4_archiv_hook:
        _archiv_log(
            {
                "ts": int(time.time()),
                "chat_id": chat_id,
                "user_id": user_id,
                "text": text,
                "stage": cfg.stage,
            }
        )

    # Stage 5: Rate-Limit
    if cfg.stage5_monitoring and user_id is not None:
        ok = _check_rate_limit(int(user_id))
        if not ok:
            return ["Langsam, Bruder. Der Codex will, dass du kurz durchatmest. 🫠"]

    # /start
    if text.startswith("/start") and cfg.stage1_online_echo:
        intro = [
            "Codex2050 Render‑Bot ist online. 🔥",
            f"Aktive Stufe: {cfg.stage}",
        ]
        if cfg.stage6_full_ai:
            intro.append("Full‑AI‑Bridge ist scharf. Du kannst mir jede Frage stellen.")
        else:
            intro.append("Du kannst mir schreiben – der Bot filtert, spiegelt und antwortet im 2050‑Modus.")
        messages.append("\n".join(intro))
        return messages

    # Stage 2: Schutzfilter
    if cfg.stage2_protection_filter and text:
        if _looks_like_scam(text):
            return [
                "Dieser Link riecht nach Scam. ❌\n"
                "Codex2050 hat ihn blockiert, damit dein Chat sauber bleibt."
            ]

    # Stage 3: einfache Auto-Kommandos
    if cfg.stage3_auto_reply:
        lower = text.lower().strip()
        if lower in {"/help", "hilfe", "was kannst du", "menu"}:
            messages.append(
                "Ich bin der Codex2050‑Render‑Bot.\n"
                "– Stufe 1: Echo & Online‑Check\n"
                "– Stufe 2: Scam‑Filter\n"
                "– Stufe 3: einfache Auto‑Antworten\n"
                "– Stufe 4: Archiv‑Log\n"
                "– Stufe 5: Monitoring\n"
                "– Stufe 6: Full‑AI‑Bridge (OpenAI)\n"
                "Schreib mir einfach – ich sortiere den Rest."
            )
            return messages

        if lower in {"/status", "status"}:
            ai = "aktiv" if cfg.stage6_full_ai else "bereit, aber kein API‑Key"
            messages.append(
                f"Status:\nStufe: {cfg.stage}\nFull‑AI‑Bridge: {ai}\n"
                "Logfile: codex2050_log.txt (falls Stufe ≥ 4)."
            )
            return messages

    # Stage 6: Full‑AI‑Bridge
    if cfg.stage6_full_ai and text:
        answer = _call_openai(text)
        messages.append(answer)
        return messages

    # Standard‑Echo (Stage 1)
    if cfg.stage1_online_echo and text:
        messages.append(f"ECHO 2050: {text}")
        return messages

    # Fallback – sollte selten vorkommen
    messages.append("Codex2050 hat nichts zu sagen, aber ist wach. 👁️")
    return messages
