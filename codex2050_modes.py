
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Mode:
    key: str
    title: str
    short: str
    description: str


def get_all_modes() -> Dict[str, Mode]:
    """Return all defined Codex-2050 modes (Stufen 1–6)."""
    modes: List[Mode] = [
        Mode(
            key="1",
            title="Stufe 1 – Wahrnehmung",
            short="Scannen & Benennen",
            description=(
                "Fokus auf klares Benennen der aktuellen Lage: Geld, Körper, Frauen, "
                "Energie. Keine Bewertung, nur ehrliche Beobachtung in einfachen Sätzen."
            ),
        ),
        Mode(
            key="2",
            title="Stufe 2 – Struktur",
            short="Ordnen & Priorisieren",
            description=(
                "Aus der Roh-Wahrnehmung werden 3–5 Prioritäten gebaut. "
                "Was braucht heute als erstes Energie? Was kann warten?"
            ),
        ),
        Mode(
            key="3",
            title="Stufe 3 – Handlung",
            short="Konkrete Schritte",
            description=(
                "Konkrete, kleine Schritte für die nächsten 12–24 Stunden. "
                "Kein Perfektionismus, nur Bewegung: Telefonate, Nachrichten, "
                "1–2 Tasks für Geld/Business, 1 Task für Körper."
            ),
        ),
        Mode(
            key="4",
            title="Stufe 4 – Schutz",
            short="Dunkelblauer Modus",
            description=(
                "Prüfung, was dich heute zerstören oder ausbrennen könnte "
                "(Menschen, Nachrichten, Social Media, Alkohol, Eskalation) "
                "und wie du das minimierst."
            ),
        ),
        Mode(
            key="5",
            title="Stufe 5 – Echo",
            short="Spiegel & Feedback",
            description=(
                "Hier werden Echos gesammelt: Was kam zurück? Antworten, Absagen, "
                "Zufälle, Körpersignale. Kein Drama, nur Daten für den nächsten Tag."
            ),
        ),
        Mode(
            key="6",
            title="Stufe 6 – Imperator",
            short="Langstrecke 2050",
            description=(
                "Hier geht es um 2050-Linie: Was bleibt von heute in 1 Jahr wichtig? "
                "Was ist nur Lärm? Fokus auf Vision, nicht auf kurzfristige Panik."
            ),
        ),
    ]
    return {m.key: m for m in modes}


def format_modes_list() -> str:
    modes = get_all_modes()
    lines = ["Stufen 1–6 (Codex-2050-Modus):"]
    for m in modes.values():
        lines.append(f"{m.key}. {m.title} – {m.short}")
    lines.append("")
    lines.append("Nutze /mode <1-6>, z.B.: /mode 3")
    return "\n".join(lines)


def format_mode_detail(key: str) -> str:
    modes = get_all_modes()
    mode = modes.get(key)
    if not mode:
        return "Unbekannte Stufe. Nutze /stufen für eine Übersicht."
    return (
        f"{mode.title}\n"
        f"{'-'*len(mode.title)}\n"
        f"{mode.description}"
    )
