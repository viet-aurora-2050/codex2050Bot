
"""Kleiner Logik-Kern für den Codex2050 Render-Bot.

Wichtig:
- Kein externer API-Zwang (läuft also auch ohne OpenAI-Key).
- Pro Nutzer wird nur minimaler Zustand im RAM gehalten.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

from codex2050_modes import format_modes_list, format_mode_detail

log = logging.getLogger(__name__)


@dataclass
class UserState:
    mode: str = "1"   # Default: Stufe 1
    last_prompt: Optional[str] = None
    notes: Dict[str, str] = field(default_factory=dict)


class Codex2050Engine:
    """Very small in-memory engine.

    Das hier ist absichtlich simpel gehalten:
    - Kein DB, nur ein Dictionary pro Prozess.
    - Für unser Ziel reicht das komplett.
    """

    def __init__(self) -> None:
        self._users: Dict[int, UserState] = {}

    # --- intern -------------------------------------------------------------

    def _get_state(self, user_id: int) -> UserState:
        if user_id not in self._users:
            self._users[user_id] = UserState()
        return self._users[user_id]

    # --- öffentliche API ----------------------------------------------------

    def handle_command(self, user_id: int, command: str, arg: Optional[str]) -> str:
        state = self._get_state(user_id)
        command = command.lower()

        if command in ("/start", "start"):
            return self._handle_start(state)

        if command in ("/help", "help"):
            return self._handle_help()

        if command in ("/stufen", "/modes", "stufen"):
            return format_modes_list()

        if command == "/mode":
            if not arg:
                return "Welche Stufe? Beispiel: /mode 3"
            return self._handle_set_mode(state, arg.strip())

        if command == "/status":
            return self._handle_status(state)

        # Fallback
        return "Unbekannter Befehl. Nutze /help für eine Übersicht."

    def handle_free_text(self, user_id: int, text: str) -> str:
        state = self._get_state(user_id)
        state.last_prompt = text.strip()
        # Speichere pro Stufe eine letzte Notiz
        state.notes[state.mode] = text.strip()

        base = (
            f"🧠 Eingang registriert in Stufe {state.mode}.
"
            f"Dein Text bleibt im lokalen 2050-Puffer für diesen Lauf.

"
            f"Wenn du die Stufe wechseln willst: /stufen oder /mode <1-6>.
"
            f"Status anzeigen: /status"
        )
        return base

    # --- konkrete Handler ---------------------------------------------------

    def _handle_start(self, state: UserState) -> str:
        return (
            "Codex2050 Render-Bot ist aktiv. 🔥\n\n"
            "Ich arbeite in 6 Stufen (1–6) – alle lokal, ohne Cloud-Logik.\n"
            "Du kannst jederzeit einfache Sätze senden – ich ordne sie in die "
            "aktuelle Stufe ein.\n\n"
            + format_modes_list()
        )

    def _handle_help(self) -> str:
        return (
            "Befehle:\n"
            "/start – Übersicht & Einstieg\n"
            "/stufen – Liste der Stufen 1–6\n"
            "/mode <1-6> – Stufe wechseln (z.B. /mode 4)\n"
            "/status – Aktuellen Modus + letzte Notizen anzeigen\n"
            "\n"
            "Alles andere wird als freier Text in die aktuelle Stufe geschrieben."
        )

    def _handle_set_mode(self, state: UserState, raw: str) -> str:
        key = raw.strip()
        if key not in {str(i) for i in range(1, 7)}:
            return "Bitte eine Zahl von 1–6 wählen. Beispiel: /mode 2"

        state.mode = key
        detail = format_mode_detail(key)
        return (
            f"Stufe gewechselt auf {key}.\n\n"
            f"{detail}\n\n"
            "Schreib in einfachen Sätzen, ich sortiere es in diese Stufe."
        )

    def _handle_status(self, state: UserState) -> str:
        detail = format_mode_detail(state.mode)
        note = state.notes.get(state.mode)
        extra = f"\n\nLetzte Notiz in dieser Stufe:\n{note}" if note else ""
        return f"Aktuelle Stufe: {state.mode}\n\n{detail}{extra}"
