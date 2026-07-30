"""Private sovereignty journal for the Closed Loop Protocol."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Callable, Iterable

AUTHENTIC_RATE = 0.02
DEGRADED_RATE = -0.05
DEFAULT_LOG = Path("data/sovereignty_log.jsonl")


@dataclass(frozen=True)
class SovereigntyEntry:
    date: str
    thread: str
    knot: str
    authentic: bool
    cost: float
    presence: float
    sigma_before: float
    delta: float
    sigma_after: float
    human_witnessed: bool
    witness_note: str
    shadow: str
    audit_note: str

    def __post_init__(self) -> None:
        if not self.thread.strip() or not self.knot.strip() or not self.shadow.strip():
            raise ValueError("thread, knot, and shadow cannot be empty")
        for value, name in (
            (self.cost, "cost"),
            (self.presence, "presence"),
            (self.sigma_before, "sigma_before"),
            (self.sigma_after, "sigma_after"),
        ):
            _bounded(float(value), name)
        expected_delta, expected_sigma = calculate_sigma(
            self.sigma_before, self.authentic, self.cost, self.presence
        )
        if not math.isclose(self.delta, expected_delta, abs_tol=1e-12):
            raise ValueError("delta does not match the Closed Loop equation")
        if not math.isclose(self.sigma_after, expected_sigma, abs_tol=1e-12):
            raise ValueError("sigma_after does not match the bounded equation result")
        if self.human_witnessed and not self.authentic:
            raise ValueError("a degraded action cannot set the Witness Flag")
        if self.human_witnessed and not self.witness_note.strip():
            raise ValueError("human recognition requires a witness note")


def _bounded(value: float, name: str) -> float:
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def calculate_delta(authentic: bool, cost: float, presence: float = 1.0) -> float:
    """Calculate one equation update after validating bounded inputs."""
    cost = _bounded(float(cost), "cost")
    presence = _bounded(float(presence), "presence")
    rate = AUTHENTIC_RATE if authentic else DEGRADED_RATE
    return rate * cost * presence


def calculate_sigma(
    sigma_before: float,
    authentic: bool,
    cost: float,
    presence: float = 1.0,
) -> tuple[float, float]:
    """Return ``(delta, bounded_sigma_after)`` for one knot."""
    sigma_before = _bounded(float(sigma_before), "sigma")
    delta = calculate_delta(authentic, cost, presence)
    sigma_after = min(1.0, max(0.0, sigma_before + delta))
    return delta, sigma_after


def load_entries(log_path: Path = DEFAULT_LOG) -> list[SovereigntyEntry]:
    """Load JSON Lines entries, reporting malformed records with a line number."""
    path = Path(log_path)
    if not path.exists():
        return []

    entries: list[SovereigntyEntry] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                entries.append(SovereigntyEntry(**json.loads(line)))
            except (json.JSONDecodeError, TypeError, ValueError) as error:
                raise ValueError(f"Invalid entry at {path}:{line_number}") from error
    return entries


def append_entry(entry: SovereigntyEntry, log_path: Path = DEFAULT_LOG) -> None:
    """Append one UTF-8 JSON record, creating its private data directory."""
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        json.dump(asdict(entry), handle, ensure_ascii=False, separators=(",", ":"))
        handle.write("\n")


def _ask_text(prompt: str, input_fn: Callable[[str], str] = input) -> str:
    while True:
        value = input_fn(prompt).strip()
        if value:
            return value
        print("Please enter a response.")


def _ask_bool(prompt: str, input_fn: Callable[[str], str] = input) -> bool:
    while True:
        value = input_fn(f"{prompt} (y/n): ").strip().lower()
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Please answer y or n.")


def _ask_score(prompt: str, input_fn: Callable[[str], str] = input) -> float:
    while True:
        raw = input_fn(f"{prompt} (0 to 1): ").strip()
        try:
            return _bounded(float(raw), prompt)
        except ValueError:
            print("Please enter a number from 0 to 1.")


def daily_checkin(
    log_path: Path = DEFAULT_LOG,
    input_fn: Callable[[str], str] = input,
) -> SovereigntyEntry:
    """Run one interactive check-in and persist the resulting entry."""
    previous_entries = load_entries(log_path)
    sigma_before = previous_entries[-1].sigma_after if previous_entries else 0.0

    print(f"Founder's Log — {date.today().isoformat()}")
    print(f"Current private σ: {sigma_before:.4f}")
    thread = _ask_text("What loose thread tugged at you? ", input_fn)
    knot = _ask_text("What minimal knot did you complete? ", input_fn)
    cost = _ask_score("Estimate c(κ) before acting", input_fn)
    presence = _ask_score("Presence p", input_fn)
    authentic = _ask_bool("Was the action authentic rather than performative?", input_fn)
    delta, sigma_after = calculate_sigma(sigma_before, authentic, cost, presence)

    human_witnessed = False
    witness_note = ""
    if authentic:
        human_witnessed = _ask_bool(
            "Did a human explicitly recognize that this knot served them?", input_fn
        )
        if human_witnessed:
            witness_note = _ask_text(
                "Record the human recognition in your own words: ", input_fn
            )
    else:
        print("A degraded action is not eligible for the Witness Flag.")

    shadow = _ask_text("What shadow or next thread appeared? ", input_fn)
    audit_note = input_fn("Post-action audit note (optional): ").strip()
    entry = SovereigntyEntry(
        date=date.today().isoformat(),
        thread=thread,
        knot=knot,
        authentic=authentic,
        cost=cost,
        presence=presence,
        sigma_before=sigma_before,
        delta=delta,
        sigma_after=sigma_after,
        human_witnessed=human_witnessed,
        witness_note=witness_note,
        shadow=shadow,
        audit_note=audit_note,
    )
    append_entry(entry, log_path)

    direction = "+" if delta >= 0 else ""
    print(f"Logged. Δσ={direction}{delta:.4f}; σ={sigma_after:.4f}.")
    if human_witnessed:
        print("Human recognition recorded. The AI did not set the Witness Flag.")
    print("Coram te necto.")
    return entry


def render_review(entries: Iterable[SovereigntyEntry]) -> str:
    """Render a concise plain-text review of supplied entries."""
    rows = list(entries)
    if not rows:
        return "No sovereignty entries found."
    lines = ["--- Sovereignty Review ---"]
    for entry in rows:
        kind = "authentic" if entry.authentic else "degraded"
        witness = "human-witnessed" if entry.human_witnessed else "unwitnessed"
        lines.append(
            f"{entry.date} | σ {entry.sigma_before:.4f} → {entry.sigma_after:.4f} "
            f"| {kind} | {witness} | knot: {entry.knot}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help="JSONL journal path")
    subparsers = parser.add_subparsers(dest="command")
    check_in = subparsers.add_parser("check-in", help="record one private sovereignty entry")
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
