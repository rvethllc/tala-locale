# Contributing to tala-locale

Thanks for taking the time to contribute.

## The most common contribution: adding or fixing a country entry

All country data lives in one file: [`src/tala_locale/_data.py`](src/tala_locale/_data.py)

Each entry is one line:
```python
"234": ("NG", "NGN", "en"),  # Nigeria
```

Format: `"calling_code": ("ISO-3166-1-alpha-2", "ISO-4217", "ISO-639-1")`

To add or fix an entry:
1. Edit `_data.py`
2. Add a test in `tests/test_locale.py`
3. Open a PR — that's it

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

## Reporting a wrong currency or language

Open an issue with:
- The phone prefix
- What the library returns today
- What it should return (with a source — Wikipedia, ISO.org, etc.)

## Code style

```bash
ruff check src/ tests/
ruff format src/ tests/
```

CI enforces both. Fix any ruff errors before pushing.

## What we don't accept

- Changes to the public API without opening an issue first
- Adding runtime dependencies
- Removing the `(None, None, None)` fallback behaviour — callers depend on it
