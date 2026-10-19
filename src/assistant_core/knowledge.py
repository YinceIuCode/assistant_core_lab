import csv
import json
from dataclasses import dataclass
from pathlib import Path

from assistant_core.errors import DataError

@dataclass(frozen=True)
class Office:
    name: str
    room: str
    hours: str

class OfficeDirectory:
    def __init__(self, offices: dict[str, Office]):
        self._offices = offices

    @classmethod
    def from_csv(cls, path: Path) -> "OfficeDirectory":
        try:
            with path.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
        except FileNotFoundError as exc:
            raise DataError(f"Office file not found: {path}") from exc
        return cls({r["name"].lower(): Office(r["name"], r["room"], r["hours"]) for r in rows})

    @property
    def names(self) -> set[str]:
        return set(self._offices)

    def find(self, text: str) -> Office | None:
        t = text.lower()
        return next((o for name, o in self._offices.items() if name in t), None)

@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    text: str

class Handbook:
    def __init__(self, rules: list[Rule]):
        self._rules = rules

    @classmethod
    def from_json(cls, path: Path) -> "Handbook":
        try:
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as exc:
            raise DataError(f"Handbook file not found: {path}") from exc
        return cls([Rule(r["id"], r["title"], r["text"]) for r in data])

    def search(self, query: str) -> Rule | None:
        q_words = set(query.lower().split())
        best_rule = None
        best_score = 0
        for rule in self._rules:
            r_words = set(rule.text.lower().split()) | set(rule.title.lower().split())
            score = len(q_words & r_words)
            if score > best_score:
                best_score = score
                best_rule = rule
        return best_rule