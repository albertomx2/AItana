"""Expense parsing & storage."""

from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, TypedDict

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
DATA_DIR.mkdir(exist_ok=True)


class Expense(TypedDict):
    name: str
    amount: float
    place: str
    timestamp: str
    raw: str


_PAT = re.compile(
    r"(?:soy|me llamo)\s+(?P<name>\w+).*?"          # nombre
    r"(?:me\s+acabo\s+de\s+|me\s+he\s+|he\s+)?"
    r"gast\w*\s+"                                   # ↔ gasto, gastado, gastar, gasté…
    r"(?P<amount>\d+[.,]?\d*)\s*"                   # cantidad
    r"(?:€|eur|euros?)\s+"                          # símbolo o palabra euro
    r"(?:en|en\s+el|en\s+la)\s+"                    # preposición
    r"(?P<place>[\w\sÁÉÍÓÚáéíóúñÑ]+)",              # lugar
    re.I | re.S,
)



def parse_expense(text: str) -> Optional[Expense]:
    """Return Expense dict if pattern matches, else None."""
    m = _PAT.search(text)
    if not m:
        return None
    name = m.group("name").capitalize()
    amount = float(m.group("amount").replace(",", "."))
    place = m.group("place").strip().title()
    return {
        "name": name,
        "amount": amount,
        "place": place,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
        "raw": text.replace("\n", " "),
    }


def add_expense(exp: Expense) -> None:
    """Append expense to CSV: data/gastos_<name>.csv."""
    path = DATA_DIR / f"gastos_{exp['name'].lower()}.csv"
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["timestamp", "amount", "place", "raw"]
        )
        if new_file:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": exp["timestamp"],
                "amount": exp["amount"],
                "place": exp["place"],
                "raw": exp["raw"],
            }
        )
