# tala-locale

[![CI](https://github.com/rvethllc/tala-locale/actions/workflows/ci.yml/badge.svg)](https://github.com/rvethllc/tala-locale/actions/workflows/ci.yml)
[![PyPI Version](https://img.shields.io/pypi/v/tala-locale.svg)](https://pypi.org/project/tala-locale/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tala-locale.svg)](https://pypi.org/project/tala-locale/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://codecov.io/gh/rveth/tala-locale/branch/main/graph/badge.svg)](https://codecov.io/gh/rveth/tala-locale)

**Phone number + timezone → country, currency, language, IANA timezone, formatting, VAT, and more. Zero runtime dependencies.**

```python
from tala_locale import infer_full_locale

r = infer_full_locale("+2348012345678")
r.country          # "NG"
r.currency         # "NGN"
r.language         # "en-NG"   ← BCP 47, not bare "en"
r.languages        # ("en-NG", "ha-NG", "yo-NG", "ig-NG", "pcm-NG")
r.timezone         # "Africa/Lagos"
r.utc_offset_hours # 1.0
r.currency_symbol  # "₦"
r.vat_rate         # 0.075     ← 7.5%
r.date_format      # "%d/%m/%Y"
r.confidence       # 1.0
```

---

## Why tala-locale?

Any application that collects a phone number can instantly know where a user is from — country, currency, timezone, language, number formatting, VAT rate, RTL direction — all from one call, with no GPS, no IP lookup, no user forms, and zero runtime dependencies.

| What you want | What you get |
|---|---|
| Pre-fill currency for pricing | `r.currency` → `"GBP"`, `"NGN"`, `"AED"` |
| Show onboarding in the user's language | `r.language` → `"en-NG"`, `"fr-SN"`, `"ar-MA"` |
| Know ALL languages spoken in a country | `r.languages` → `("ar-MA", "fr-MA", "tzm-MA", "zgh-MA")` |
| Format money correctly | `r.currency_symbol`, `r.decimal_sep`, `r.currency_before` |
| Apply correct VAT rate | `r.vat_rate` → `0.075` (7.5%), `0.20` (20%) |
| Right-to-left layout | `r.rtl` → `True` for Arabic, Hebrew, Persian, Urdu |
| Correct date format | `r.date_format` → `"%d/%m/%Y"` (Nigeria), `"%Y-%m-%d"` (Sweden) |
| Disambiguate +1 (US vs Canada) | Area code resolution → `+1-416` → Canada at 0.95 confidence |
| Route to the right support team | `r.country` → `"KE"`, `"ZA"`, `"IN"` |
| Skip "where are you from?" | Infer it silently at signup |
| Convert times to local | `format_local_datetime(utc_dt, "NG")` → `"14/06/2025 13:30"` |

Works with **any messaging platform or application** that handles phone numbers: WhatsApp, Telegram, SMS, SaaS onboarding, e-commerce checkout, fintech KYC, fraud detection, CRM enrichment, AI assistants.

---

## Installation

```bash
pip install tala-locale
```

Pure Python. Zero runtime dependencies. Python 3.10+.

> On Windows only: installs `tzdata` (IANA timezone database). On Linux/Mac the OS provides it. Lambda (Linux) = truly zero deps at runtime.

---

## Quick start

### Basic: country, currency, language from a phone number

```python
from tala_locale import infer_locale

result = infer_locale("+447911123456")
result.country   # "GB"
result.currency  # "GBP"
result.language  # "en-GB"

# Unpack like a tuple
country, currency, language = infer_locale("+254712345678")
# country="KE", currency="KES", language="sw-KE"

# Check before using
if result.is_known():
    set_user_currency(result.currency)
else:
    ask_user_for_currency()
```

### Full: timezone + formatting + confidence + all languages

```python
from tala_locale import infer_full_locale

# Nigeria — single-country prefix, full confidence
r = infer_full_locale("+2348012345678")
r.country          # "NG"
r.language         # "en-NG"
r.languages        # ("en-NG", "ha-NG", "yo-NG", "ig-NG", "pcm-NG")
r.timezone         # "Africa/Lagos"
r.utc_offset_hours # 1.0
r.currency_symbol  # "₦"
r.vat_rate         # 0.075
r.date_format      # "%d/%m/%Y"
r.rtl              # False
r.confidence       # 1.0

# Morocco — Arabic primary, but French + Berber also in use
r = infer_full_locale("+212612345678")
r.language         # "ar-MA"
r.languages        # ("ar-MA", "fr-MA", "tzm-MA", "zgh-MA")
r.rtl              # True
r.date_format      # "%d/%m/%Y"

# UAE — Gulf Arabic, not Egyptian Arabic, not Levantine Arabic
r = infer_full_locale("+971501234567")
r.language         # "ar-AE"
r.languages        # ("ar-AE", "en-AE")

# Lebanon — genuinely trilingual in business
r = infer_full_locale("+96170123456")
r.languages        # ("ar-LB", "fr-LB", "en-LB")

# South Africa — 11 official languages
r = infer_full_locale("+27821234567")
r.languages        # ("en-ZA", "zu-ZA", "xh-ZA", "af-ZA", "nso-ZA", ...)

# Disambiguating +1 (US vs Canada) — area code resolution, no browser needed
r = infer_full_locale("+14165551234")  # 416 = Toronto
r.country          # "CA"
r.timezone         # "America/Toronto"
r.confidence       # 0.95

# With browser timezone as additional signal
r = infer_full_locale("+14165551234", browser_timezone="America/Toronto")
r.country          # "CA"
r.confidence       # 0.95

# Timezone-only fallback (no phone given)
r = infer_full_locale("", browser_timezone="Africa/Lagos")
r.country          # "NG"
r.confidence       # 0.8
```

---

## Timezone-correct timestamps

This is the most powerful use case. A server clock (AWS Lambda, ECS, any cloud) gives you a perfectly accurate UTC time. `tala-locale` gives you the IANA key to convert it to the user's exact local time — correct to the microsecond.

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo          # stdlib, Python 3.9+
from tala_locale import infer_timezone

# One call: country → IANA timezone key
tz_key = infer_timezone("NG")          # "Africa/Lagos"
tz_key = infer_timezone("AE")          # "Asia/Dubai"
tz_key = infer_timezone("MA")          # "Africa/Casablanca"

# Convert server UTC clock to business local time
utc_now = datetime.now(timezone.utc)   # AWS atomic clock, accurate to ~0.1ms
local_now = utc_now.astimezone(ZoneInfo(tz_key))

# 2026-06-14 23:58:42.019234+01:00   ← Lagos, microsecond precision
# 2026-06-15 02:58:42.019234+04:00   ← Dubai (next day!)
# 2026-06-14 23:58:42.019234+01:00   ← Casablanca

# Write the correct local date to your database
local_date = local_now.date()          # date(2026, 6, 14) or date(2026, 6, 15)
```

**Why this matters for financial records:** A server in Ireland (UTC+0/+1) writing `date.today()` would stamp a Dubai invoice with yesterday's date at 1am local time. With `infer_timezone` + `ZoneInfo`, every invoice, transaction, and journal entry gets the business's actual local date — regardless of where your servers run.

The full timestamp written to the database includes the UTC offset, so you can always convert back:

```python
# Stamp written: 2026-06-15 02:58:42.019234+04:00  (Dubai)
# Convert to UTC: 2026-06-14 22:58:42.019234+00:00  (same instant)
# All timestamps align perfectly across timezones
```

**Works with `format_local_datetime` for display:**

```python
from tala_locale import format_local_datetime
from datetime import datetime, timezone

utc_now = datetime.now(timezone.utc)

format_local_datetime(utc_now, "NG")           # "14/06/2026 23:58"
format_local_datetime(utc_now, "SE")           # "2026-06-14 23:58"  (ISO, Sweden)
format_local_datetime(utc_now, "US")           # "06/14/2026 23:58"  (US format)
format_local_datetime(utc_now, "AE")           # "15/06/2026 02:58"  (next day, Dubai)
```

The date format is locale-correct automatically — `r.date_format` drives it.

---

## Phone format tolerance

tala-locale accepts phone numbers in any common format:

```python
infer_locale("+234 801 234 5678")        # spaces
infer_locale("+234-801-234-5678")        # dashes
infer_locale("(234) 801 234 5678")       # parentheses
infer_locale("2348012345678")            # bare digits, no +
infer_locale("+2348012345678")           # E.164 standard
infer_locale("whatsapp:+2348012345678")  # WhatsApp format
```

All of the above return `LocaleResult(country='NG', currency='NGN', language='en-NG')`.

---

## Language tags: BCP 47, not bare ISO 639-1

tala-locale returns **country-qualified BCP 47 language tags**, not bare ISO 639-1 codes.

This matters because:

- `ar-EG` (Egyptian Arabic) ≠ `ar-SA` (Gulf Arabic) ≠ `ar-MA` (Moroccan Darija) ≠ `ar-LY` (Libyan Arabic)
- `en-NG` (Nigerian English) ≠ `en-GB` ≠ `en-US` ≠ `en-AU` ≠ `en-IN`
- `pt-BR` (Brazilian Portuguese) ≠ `pt-PT` (European Portuguese)
- `zh-CN` (Simplified) ≠ `zh-HK` / `zh-TW` (Traditional)

When you pass a language tag to an LLM, TTS engine, or translation service, the dialect signal is what produces the correct register, vocabulary, and cultural context.

The `languages` tuple lists **all significant languages** for a country, primary first. Use it when you need to:
- Offer a language selector pre-populated with the right options
- Route a customer message to the right support agent
- Prompt an LLM to respond in any of the customer's languages

```python
# India — 11 languages listed
r = infer_full_locale("+919812345678")
r.languages
# ("en-IN", "hi-IN", "bn-IN", "te-IN", "mr-IN", "ta-IN", "ur-IN",
#  "gu-IN", "kn-IN", "ml-IN", "pa-IN")

# Switzerland — 4 official languages
from tala_locale import get_extended
ext = get_extended("CH")
ext.languages  # ("de-CH", "fr-CH", "it-CH", "rm-CH")

# Paraguay — genuinely bilingual: Spanish + Guaraní
ext = get_extended("PY")
ext.languages  # ("es-PY", "gn-PY")
```

---

## Monetary formatting

```python
from tala_locale import format_amount

format_amount(1234.5, "NG")  # "₦1,234.50"
format_amount(1234.5, "DE")  # "1.234,50 €"
format_amount(1234.5, "FR")  # "1 234,50 €"
format_amount(1234.5, "US")  # "$1,234.50"
format_amount(1234.5, "ZA")  # "R 1 234.50"
format_amount(1234.5, "JP")  # "¥1,234.50"
```

---

## Datetime localisation

```python
from datetime import datetime, timezone
from tala_locale import format_local_datetime, get_local_datetime

utc = datetime(2025, 6, 14, 11, 30, 0, tzinfo=timezone.utc)

format_local_datetime(utc, "NG")  # "14/06/2025 12:30"   (WAT = UTC+1)
format_local_datetime(utc, "US")  # "06/14/2025 07:30"   (EDT = UTC-4)
format_local_datetime(utc, "DE")  # "14.06.2025 13:30"   (CEST = UTC+2)
format_local_datetime(utc, "SE")  # "2025-06-14 13:30"   (CEST = UTC+2)
format_local_datetime(utc, "SA")  # "14/06/2025 14:30"   (AST = UTC+3)

# Date only
format_local_datetime(utc, "NG", include_time=False)  # "14/06/2025"
```

---

## Area code disambiguation (+1 US vs Canada)

tala-locale includes 1,590+ area codes across 27 calling code regions. For shared prefixes like +1, it uses the area code to identify the country without needing a browser timezone:

```python
r = infer_full_locale("+14165551234")   # 416 = Toronto
r.country    # "CA"
r.timezone   # "America/Toronto"
r.confidence # 0.95

r = infer_full_locale("+12125551234")   # 212 = New York City
r.country    # "US"
r.timezone   # "America/New_York"
r.confidence # 0.95
```

Confidence levels:
- `1.0` — unambiguous prefix (single-country calling code)
- `0.95` — area code disambiguated (e.g. +1-416 → CA)
- `0.9` — browser timezone disambiguated
- `0.8` — timezone-only (no phone number)
- `0.0` — unknown

---

## API reference

### `infer_locale(phone_number) → LocaleResult`

Fast lookup. Returns `(country, currency, language)`. All `None` if unknown.

### `infer_full_locale(phone_number, *, browser_timezone=None) → FullLocaleResult`

Full inference. 19-field named tuple covering everything below.

### `class FullLocaleResult`

| Field | Type | Example |
|---|---|---|
| `country` | `str \| None` | `"NG"` |
| `currency` | `str \| None` | `"NGN"` |
| `language` | `str \| None` | `"en-NG"` (BCP 47 primary) |
| `languages` | `tuple \| None` | `("en-NG", "ha-NG", "yo-NG", "ig-NG", "pcm-NG")` |
| `timezone` | `str \| None` | `"Africa/Lagos"` |
| `utc_offset_hours` | `float \| None` | `1.0` |
| `timezones` | `tuple \| None` | All IANA zones for the country |
| `extended` | `ExtendedLocale \| None` | Full formatting object |
| `confidence` | `float` | `1.0` / `0.95` / `0.9` / `0.8` / `0.0` |
| `currency_symbol` | `str \| None` | `"₦"` |
| `currency_before` | `bool \| None` | `True` (symbol before amount) |
| `decimal_sep` | `str \| None` | `"."` |
| `thousands_sep` | `str \| None` | `","` |
| `vat_rate` | `float \| None` | `0.075` (= 7.5%) |
| `vat_name` | `str \| None` | `"VAT"`, `"TVA"`, `"MwSt."`, `"GST"` |
| `date_format` | `str \| None` | `"%d/%m/%Y"` |
| `rtl` | `bool \| None` | `False` |
| `week_start` | `int \| None` | `0` = Monday, `6` = Sunday |
| `bcp47` | `str \| None` | `"en-NG"` (same as `language`) |

### `class ExtendedLocale`

Available via `r.extended` or `get_extended("NG")`. Same fields as above plus `languages` tuple.

### Other functions

```python
infer_country(phone)                     # → str | None
infer_currency(phone)                    # → str | None
infer_language(phone)                    # → str | None  (BCP 47)
is_supported(phone)                      # → bool
infer_country_from_timezone(tz)          # → str | None
infer_timezone(country_code)             # → str | None  (primary IANA)
infer_timezones(country_code)            # → tuple[str, ...]  (all IANA)
get_utc_offset(country_code_or_tz)       # → float | None
get_local_datetime(utc_dt, country_or_tz)     # → datetime (aware)
format_local_datetime(utc_dt, country_or_tz)  # → str
format_amount(value, country_code)            # → str
get_extended(country_code)               # → ExtendedLocale | None
supported_countries()                    # → list[dict]
```

---

## Coverage

**191 countries/territories** across all regions:

| Region | Countries |
|---|---|
| West Africa | Nigeria, Ghana, Senegal, Côte d'Ivoire, Mali, Burkina Faso, and 10 more |
| East Africa | Kenya, Tanzania, Uganda, Ethiopia, Rwanda, Somalia, and 4 more |
| North Africa | Egypt, Morocco, Algeria, Tunisia, Libya, Sudan |
| Southern Africa | South Africa (11 official languages), Zambia, Zimbabwe, Botswana, and 5 more |
| Central Africa | DRC, Cameroon, Angola, Gabon, and 5 more |
| Indian Ocean | Madagascar, Mauritius, Seychelles, Comoros |
| Western Europe | UK, France, Germany, Spain, Italy, Netherlands, Switzerland, and 10 more |
| Eastern Europe | Russia, Ukraine, Poland, Czech Republic, and 15 more |
| North America | USA, Canada (area code disambiguation), Mexico |
| Caribbean | Trinidad, Jamaica, Barbados, Dominican Republic, Haiti, and 8 more |
| Central America | Guatemala, Costa Rica, Panama, and 4 more |
| South America | Brazil, Argentina, Colombia, Chile, Peru, Bolivia, Paraguay (Guaraní), and 4 more |
| Middle East | UAE, Saudi Arabia, Israel, Turkey, Iran, Lebanon (trilingual), and 8 more |
| South Asia | India (11 languages), Pakistan, Bangladesh, Sri Lanka, Nepal, Afghanistan |
| East Asia | China, Japan, South Korea, Hong Kong, Macao, Taiwan, Mongolia |
| Southeast Asia | Singapore (4 official), Indonesia, Malaysia, Thailand, Philippines, Vietnam, and 3 more |
| Central Asia | Uzbekistan, Kazakhstan, Georgia, Armenia, Azerbaijan, and 3 more |
| Oceania | Australia, New Zealand, Fiji, Papua New Guinea, and 10 more |

---

## How prefix matching works

tala-locale uses **longest-prefix-match** to handle overlapping calling codes:

```python
infer_locale("18681234567")   # +1868 → Trinidad (TT), not USA (+1)
infer_locale("18761234567")   # +1876 → Jamaica (JM), not USA (+1)
infer_locale("85291234567")   # +852  → Hong Kong (HK)
infer_locale("8801712345678") # +880  → Bangladesh (BD)
```

Prefixes are sorted at import time — every lookup is O(n) on the fixed prefix list.

---

## Handling unknown numbers

When the prefix is not recognised, all fields are `None`. Never assume a default:

```python
result = infer_locale(phone)

if result.is_known():
    create_account(country=result.country, currency=result.currency)
else:
    prompt_user_for_country_and_currency()
```

---

## Contributing

```bash
git clone https://github.com/rvethllc/tala-locale
cd tala-locale
pip install -e ".[dev]"
pytest
```

- Missing a country? Add an entry to `src/tala_locale/_data.py` and `_extended_data.py` with a test.
- Wrong VAT rate or language list? One-line fix + test.
- New area code region? See `scripts/generate_area_data.py` for the build-time generator.

---

## Versioning

Follows [Semantic Versioning](https://semver.org/).

| Version | What changed |
|---|---|
| **3.0.0** | `languages` tuple (all significant languages per country, BCP 47), 1,590+ area codes for CA/US disambiguation, flat `FullLocaleResult` (direct field access), BCP 47 primary language tags (`"en-NG"` not `"en"`), 191-country extended dataset |
| **2.0.0** | Timezone support, `infer_full_locale`, UTC offset, datetime localisation, monetary formatting |
| **1.0.0** | `infer_locale`, 191 countries, ISO 4217 currencies |

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

> Built by [RVETH](https://rveth.in) — makers of TALA, the AI operating system for global enterprise.
