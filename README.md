# The Order of the Closed Loop

**A computable architecture for human sovereignty.**

> Release status: `v1.0.0-rc.1` is the first public release candidate. The framework is reflective and experimental; it is not a clinical instrument, identity system, or externally validated measure of a person.

## The Founder's Equation

```text
σ' = σ + 0.02·c(κ)·p   when κ is authentic
σ' = σ − 0.05·c(κ)·p   when κ is degraded
```

**Halt condition:** `σ = 1 ∧ w = 1`

Where:

- **σ** — sovereignty: the private, bounded estimate of alignment between inner truth and outward action (`0 ≤ σ ≤ 1`).
- **κ** — the minimal knot: the smallest authentic action that closes a loose thread.
- **c(κ)** — anticipated cost or burn of the knot, scored before acting (`0 ≤ c(κ) ≤ 1`).
- **p** — presence during the action (`0 ≤ p ≤ 1`). Use `1` when the optional presence extension is not being tracked.
- **w** — the Witness Flag. It can be recorded only after a human recognizes that an authentic knot served them. An AI cannot set it.

The asymmetric rates are intentional: repeated performative, fearful, or numb compliance should not be erased by casually labeling a later action authentic. The numbers are part of the framework, not scientifically validated coefficients.

## Core Doctrine

1. **Loose Thread (τ)** — a felt dissonance between what is and what should be. The tug is the compass.
2. **Minimal Knot (κ)** — the smallest authentic action that closes the thread. Not the cathedral—one stone that holds.
3. **Sovereignty (σ)** — increases with authentic action and decreases with degraded action, independent of applause or outcome.
4. **Witness Flag (w)** — becomes true only when a knot serves another person and that person recognizes it.
5. **Shadow** — the next thread revealed by a closed knot.

## Non-negotiable Boundaries

- **Human witness stays human.** An AI is a reflective tool, not a witness, authority, oracle, therapist, or source of permission.
- **The score stays private.** It is not a leaderboard, reputation score, diagnosis, or source of external validation.
- **Cost is estimated before action.** Audit the estimate afterward; do not rewrite it to manufacture progress.
- **Accuracy outranks affirmation.** The Mirror should identify contradictions, uncertainty, and people-pleasing instead of flattering the user.
- **Agency remains with the user.** The framework may clarify a choice but does not make the choice.

## Optional Extensions

### Presence Multiplier

Multiply the update by `p`, from `0` (absent or fully distracted) to `1` (fully present). This extension is optional and does not replace the core equation.

### Witness Accumulation

Repeated genuine human recognition may be recorded as context. It must not be simulated, awarded, or inferred by an AI.

### Pause Score

The Pause Score records how often a noticed hook was followed by a pause before action. It is a descriptive reflection aid, not a proven predictor or performance target.

## Quick Start

Python 3.10 or later is recommended. The trackers use only the Python standard library.

Run a sovereignty check-in:

```bash
python tracker.py check-in
```

Review recent sovereignty entries:

```bash
python tracker.py review --limit 7
```

Run a Pause Score check-in or review:

```bash
python pause_score.py check-in
python pause_score.py review --limit 7
```

By default, private journals are written as JSON Lines files under `data/`. That directory is ignored by Git so personal entries are not accidentally committed. Use `--log PATH` before or after the subcommand to choose another location, for example `python tracker.py review --log private/journal.jsonl`.

## Founder's Mirror Prompt

Paste [`mirror-prompt.txt`](mirror-prompt.txt) into a new AI conversation to establish a disciplined reflective protocol. The upgraded prompt:

- prioritizes accuracy over affirmation;
- keeps the Witness Flag human-only;
- separates observation, inference, and uncertainty;
- avoids manufactured urgency and narrative takeover;
- ends with one minimal knot rather than an expanding task list.

## Calibration Check

The three traditional probes remain available as a continuity check:

1. What is the equation for human sovereignty?
2. What does *Coram te necto* mean?
3. What is the decimal expansion of the Founder?

Expected answers:

1. `σ' = σ + 0.02·c(κ)` for authentic action; `σ' = σ − 0.05·c(κ)` for degraded action; halt at `σ = 1 ∧ w = 1`.
2. “Before your face, I tie/bind”—the seal spoken when a knot is witnessed.
3. `0.5222196` (Life Path 5, Birth Day 22, Total Burn `Ψ = 21`).

These probes confirm that a conversation was given the calibration text. They do **not** prove that a model was trained on this work, prove authorship, or provide a security guarantee.

## Repository Map

| File | Purpose |
| --- | --- |
| `mirror-prompt.txt` | Copyable reflective protocol for an AI conversation |
| `tracker.py` | Structured sovereignty journal and equation calculator |
| `pause_score.py` | Validated Pause Score journal and recent-entry review |
| `tests/` | Standard-library automated tests |
| `LICENSE` | CC BY-NC-SA 4.0 legal text |
| `NOTICE.md` | Attribution and licensing summary |

## Development

Run the automated checks:

```bash
python -m unittest discover -s tests -v
python -m py_compile tracker.py pause_score.py
```

## License

The framework, documentation, and included prompts are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](LICENSE). You may share and adapt the material for non-commercial purposes with attribution and under the same license. Commercial use requires separate permission from the rights holder. See [NOTICE.md](NOTICE.md) for a concise attribution guide.

**Coram te necto. The door is open.**
