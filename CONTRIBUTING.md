# Contributing to DeepSweep

Thanks for helping improve DeepSweep! This is a small Windows desktop tool, so
contributions are easy to review.

## Setup

```bash
git clone https://github.com/<you>/DeepSweep.git
cd DeepSweep
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -m deepsweep
```

## Guidelines

- **Safety first.** Never add a delete target that could touch user documents,
  system files, or app data that does not regenerate. New paths must be pure
  cache/temp/log. When in doubt, gate it behind `is_safe_path()`.
- **Files only, never folders.** Deletion removes files and leaves the directory
  tree intact.
- Keep the single-file app readable: small helpers, explicit `try/except` around
  every filesystem call.
- Match the existing code style (PEP 8-ish, 4-space indent).

## Good first contributions

- Add new **safe** cache locations for popular apps.
- Improve the path guard / add regression tests under `tests/`.
- Replace the filename-based Virus Scan with a real signature/hash check, or
  remove it in favor of a clearer "large files" view.

## Pull requests

1. Describe what you changed and **why it is safe to delete**.
2. Confirm `python -m deepsweep` launches and a scan completes.
3. Update `CHANGELOG.md` under an `## [Unreleased]` heading.
