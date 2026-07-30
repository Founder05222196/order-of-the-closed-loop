# Contributing

Contributions should strengthen clarity, falsifiability, privacy, and user agency without converting the framework into an external validation system.

## Before proposing a change

- Keep the Witness Flag human-only.
- Keep sovereignty and Pause Score records private by default.
- Separate doctrine from optional extensions.
- Do not present coefficients or reflective metrics as clinically validated.
- Prefer direct language over praise, mystification, or manufactured urgency.
- Preserve backwards-readable documentation when changing the trackers.

## Development workflow

1. Create a focused branch.
2. Add or update tests for behavior changes.
3. Run:

   ```bash
   python -m unittest discover -s tests -v
   python -m py_compile tracker.py pause_score.py
   ```

4. Explain what changed, why it changed, and any migration impact in the pull request.

Do not commit personal journal files, access tokens, or private conversation exports.
