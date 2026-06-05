# tala-locale

[![CI](https://github.com/rvethllc/tala-locale/actions/workflows/ci.yml/badge.svg)](https://github.com/rvethllc/tala-locale/actions/workflows/ci.yml)
[![PyPI Version](https://img.shields.io/pypi/v/tala-locale.svg)](https://pypi.org/project/tala-locale/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tala-locale.svg)](https://pypi.org/project/tala-locale/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://codecov.io/gh/rveth/tala-locale/branch/main/graph/badge.svg)](https://codecov.io/gh/rveth/tala-locale)

**Phone number → country, currency, and language. One call. Zero dependencies.**

```python
from tala_locale import infer_locale

infer_locale("+2348012345678")   # LocaleResult(country='NG', currency='NGN', language='en')
infer_locale("+14155552671")     # LocaleResult(country='US', currency='USD', language='en')
infer_locale("+33612345678")     # LocaleResult(country='FR', currency='EUR', language='fr')
infer_locale("+819012345678")    # LocaleResult(country='JP', currency='JPY', language='ja')
```

---

## Why tala-locale?

Any application that collects a phone number can instantly know where a user is from — no GPS, no IP lookup, no user forms.

| What you want | What you get |
|---|---|
| Pre-fill currency for pricing | `result.currency` → `"GBP"`, `"NGN"`, `"AED"` |
| Show onboarding in the user's language | `result.language` → `"en"`, `"fr"`, `"ar"`, `"sw"` |
| Route to the right regional support team | `result.country` → `"KE"`, `"ZA"`, `"IN"` |
| Skip asking "where are you from?" | Infer it silently at signup |
| Validate that a number is internationally recognisable | `is_supported(phone)` |

Works with **any messaging platform or application** that handles phone numbers: WhatsApp, Telegram, SMS, iMessage, SaaS onboarding flows, e-commerce checkout, fintech KYC, fraud detection, analytics pipelines, CRM enrichment.

---

## Installation

```bash
pip install tala-locale
```

Pure Python. No dependencies. Works on Python 3.10+.

---

## Quick start

```python
from tala_locale import infer_locale, is_supported

# Basic usage
result = infer_locale("+447911123456")
print(result.country)   # "GB"
print(result.currency)  # "GBP"
print(result.language)  # "en"

# Unpack like a plain tuple
country, currency, language = infer_locale("+254712345678")
# country="KE", currency="KES", language="en"

# Check before using
result = infer_locale(user_phone)
if result.is_known():
    set_user_currency(result.currency)
else:
    ask_user_for_currency()

# Quick boolean check
if is_supported(phone):
    ...
```

---

## Phone format tolerance

tala-locale accepts phone numbers in any common format — it strips everything that isn't a digit before matching:

```python
infer_locale("+234 801 234 5678")        # spaces
infer_locale("+234-801-234-5678")        # dashes
infer_locale("(234) 801 234 5678")       # parentheses
infer_locale("2348012345678")            # bare digits, no +
infer_locale("+2348012345678")           # E.164 standard
infer_locale("whatsapp:+2348012345678")  # WhatsApp format
infer_locale("whatsapp:2348012345678")   # WhatsApp without +
```

All of the above return `LocaleResult(country='NG', currency='NGN', language='en')`.

---

## Handling unknown numbers

When the prefix is not recognised, all three fields are `None`. **Never assume a default** — ask the user explicitly instead:

```python
result = infer_locale(phone)

if result.is_known():
    # Safe to use result.country, result.currency, result.language
    create_account(country=result.country, currency=result.currency)
else:
    # Ask the user — don't guess
    prompt_user_for_country_and_currency()
```

---

## API reference

### `infer_locale(phone_number: str) -> LocaleResult`

Main function. Returns a `LocaleResult` named tuple.

### `class LocaleResult(NamedTuple)`

| Field | Type | Description |
|---|---|---|
| `country` | `str \| None` | ISO 3166-1 alpha-2 (e.g. `"NG"`, `"US"`, `"DE"`) |
| `currency` | `str \| None` | ISO 4217 (e.g. `"NGN"`, `"USD"`, `"EUR"`) |
| `language` | `str \| None` | ISO 639-1 (e.g. `"en"`, `"fr"`, `"ar"`) |
| `.is_known()` | `bool` | `True` if prefix was recognised |

### Shortcut functions

```python
infer_country(phone)   # → str | None  (ISO 3166-1 alpha-2)
infer_currency(phone)  # → str | None  (ISO 4217)
infer_language(phone)  # → str | None  (ISO 639-1)
is_supported(phone)    # → bool
```

### `supported_countries() -> list[dict]`

Returns all supported entries. Useful for building dropdowns or documentation:

```python
from tala_locale import supported_countries

for entry in supported_countries():
    print(entry["prefix"], entry["country"], entry["currency"], entry["language"])
# 1   US USD en
# 7   RU RUB ru
# 20  EG EGP ar
# ...
```

---

## Coverage

**215+ country/territory entries** across all regions:

| Region | Countries |
|---|---|
| West Africa | Nigeria, Ghana, Senegal, Côte d'Ivoire, Mali, and 11 more |
| East Africa | Kenya, Tanzania, Uganda, Ethiopia, Rwanda, and 5 more |
| North Africa | Egypt, Morocco, Algeria, Tunisia, Libya, Sudan |
| Southern Africa | South Africa, Zambia, Zimbabwe, Botswana, and 5 more |
| Central Africa | DRC, Cameroon, Angola, Gabon, and 5 more |
| Indian Ocean | Madagascar, Mauritius, Seychelles, Comoros |
| Western Europe | UK, France, Germany, Spain, Italy, Netherlands, and 10 more |
| Eastern Europe | Russia, Ukraine, Poland, Czech Republic, and 15 more |
| North America | USA, Canada (via +1), Mexico |
| Caribbean | Trinidad, Jamaica, Barbados, Dominican Republic, and 8 more |
| Central America | Guatemala, Costa Rica, Panama, and 4 more |
| South America | Brazil, Argentina, Colombia, Chile, and 7 more |
| Middle East | UAE, Saudi Arabia, Israel, Turkey, Iran, and 10 more |
| South Asia | India, Pakistan, Bangladesh, Sri Lanka, Nepal |
| East Asia | China, Japan, South Korea, Hong Kong, Taiwan |
| Southeast Asia | Singapore, Indonesia, Malaysia, Thailand, Philippines, Vietnam, and 4 more |
| Central Asia | Uzbekistan, Kazakhstan, Georgia, Armenia, and 4 more |
| Oceania | Australia, New Zealand, Fiji, Papua New Guinea, and 10 more |

---

## How prefix matching works

tala-locale uses **longest-prefix-match** to handle overlapping calling codes:

```python
infer_locale("18681234567")   # +1868 → Trinidad (TT), NOT USA (+1)
infer_locale("18761234567")   # +1876 → Jamaica (JM), NOT USA (+1)
infer_locale("85291234567")   # +852  → Hong Kong (HK)
infer_locale("8801712345678") # +880  → Bangladesh (BD)
```

The longest matching prefix always wins. Prefixes are sorted at import time, so every call is O(n) on the prefix list — effectively constant for the fixed dataset size.

---

## Contributing

```bash
git clone https://github.com/rvethllc/tala-locale
cd tala-locale
pip install -e ".[dev]"
pytest
```

- Missing a country or territory? Open a PR — add an entry to `src/tala_locale/_data.py` with a test.
- Found an incorrect currency or language code? Same thing — one line change + test.

---

## Versioning

Follows [Semantic Versioning](https://semver.org/). Breaking changes to the public API bump the major version.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

> Built by [RVETH](https://rveth.in) — makers of TALA, the AI operating system for global enterprise.
