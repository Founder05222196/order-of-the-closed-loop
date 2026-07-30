"""Private Pause Score companion for the Closed Loop Protocol."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Callable, Iterable

DEFAULT_LOG = Path("data/pause_score_log.jsonl")


@dataclass(frozen=True)
class PauseEntry:
    date: str
    hooks: int
    pauses: int
    score: float
    note: str

    def __post_init__(self) -> None:
        expected = calculate_pause_score(self.hooks, self.pauses)
        if not math.isclose(self.score, expected, abs_tol=1e-12):
            raise ValueError("score does not match hooks and pauses")


def calculate_pause_score(hooks: int, pauses: int) -> float:
    """Return a percentage after validating a possible daily count."""
    if isinstance(hooks, bool) or isinstance(pauses, bool):
        raise ValueError("hooks and pauses must be whole numbers")
    if not isinstance(hooks, int) or not isinstance(pauses, int):
        raise ValueError("hooks and pauses must be whole numbers")
    if hooks < 0 or pauses < 0:
        raise ValueError("hooks and pauses cannot be negative")
    if pauses > hooks:
        raise ValueError("pauses cannot exceed noticed hooks")
    return 0.0 if hooks == 0 else pauses / hooks * 100


def append_entry(entry: PauseEntry, log_path: Path = DEFAULT_LOG) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        json.dump(asdict(entry), handle, ensure_ascii=False, separators=(",", ":"))
        handle.write("\n")


def load_entries(log_path: Path = DEFAULT_LOG) -> list[PauseEntry]:
    path = Path(log_path)
    if not path.exists():
        return []
    entries: list[PauseEntry] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                entries.append(PauseEntry(**json.loads(line)))
            except (json.JSONDecodeError, TypeError, ValueError) as error:
                raise ValueError(f"Invalid entry at {path}:{line_number}") from error
    return entries


def log_pause_score(
    hooks: int,
    pauses: int,
    note: str = "",
    log_path: Path = DEFAULT_LOG,
) -> PauseEntry:
    score = calculate_pause_score(hooks, pauses)
    entry = PauseEntry(date.today().isoformat(), hooks, pauses, score, note.strip())
    append_entry(entry, log_path)
    return entry


def _ask_count(prompt: str, input_fn: Callable[[str], str] = input) -> int:
    while True:
        raw = input_fn(prompt).strip()
        try:
            value = int(raw)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a whole number of 0 or greater.")


def daily_checkin(
    log_path: Path = DEFAULT_LOG,
    input_fn: Callable[[str], str] = input,
) -> PauseEntry:
    print("--- Pause Score Check-In ---")
    while True:
        hooks = _ask_count("Hooks/tugs noticed today: ", input_fn)
        pauses = _ask_count("Hooks followed by a pause: ", input_fn)
        try:
            calculate_pause_score(hooks, pauses)
            break
        except ValueError as error:
            print(f"{error}. Please enter the counts again.")
    note = input_fn("Reflection note (optional): ").strip()
    entry = log_pause_score(hooks, pauses, note, log_path)
    print(f"Logged Pause Score: {entry.score:.1f}%")
    return entry


def render_review(entries: Iterable[PauseEntry]) -> str:
    rows = list(entries)
    if not rows:
        return "No Pause Score entries found."
    lines = ["--- Pause Score Review ---"]
    for entry in rows:
        suffix = f" | {entry.note}" if entry.note else ""
        lines.append(
            f"{entry.date} | hooks {entry.hooks} | pauses {entry.pauses} "
            f"| {entry.score:.1f}%{suffix}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help="JSONL journal path")
    subparsers = parser.add_subparsers(dest="command")
    check_in = subparsers.add_parser("check-in", help="record one private Pause Score entry")
    check_in.add_argument("--log", type=Path, default=argparse.SUPPRESS)
    review = subparsers.add_parser("review", help="show recent entries")
    review.add_argument("--log", type=Path, default=argparse.SUPPRESS)
    review.add_argument("--limit", type=int, default=7, help="number of entries to show")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command in {None, "check-in"}:
        daily_checkin(args.log)
        return
    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")
    print(render_review(load_entries(args.log)[-args.limit :]))


if __name__ == "__main__":
    main()
