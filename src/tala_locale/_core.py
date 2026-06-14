"""
Core inference logic for tala-locale.

All public symbols are re-exported from tala_locale.__init__.
"""

from __future__ import annotations

from datetime import datetime
from datetime import timezone as _stdlib_tz
from typing import NamedTuple
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from tala_locale._area_data import AREA_CODE_MAP
from tala_locale._country_tz import COUNTRY_ALL_TZ, COUNTRY_PRIMARY_TZ
from tala_locale._data import PHONE_PREFIX_MAP
from tala_locale._extended_data import EXTENDED_LOCALE_MAP, ExtendedLocale
from tala_locale._timezone_data import TIMEZONE_COUNTRY_MAP

# Pre-sort prefixes longest-first once at import time — O(1) per lookup
_SORTED_PREFIXES: list[str] = sorted(PHONE_PREFIX_MAP, key=len, reverse=True)


class LocaleResult(NamedTuple):
    """Result of a locale inference call.

    Behaves like a plain tuple so it unpacks naturally::

        country, currency, language = infer_locale("+2348012345678")

    But also has named fields and a helper method::

        result = infer_locale("+2348012345678")
        if result.is_known():
            print(result.currency)   # "NGN"
    """

    country: str | None
    """ISO 3166-1 alpha-2 country code, e.g. "NG", "US", "DE". None if unknown."""

    currency: str | None
    """ISO 4217 currency code, e.g. "NGN", "USD", "EUR". None if unknown."""

    language: str | None
    """ISO 639-1 language code, e.g. "en", "fr", "ar". None if unknown."""

    def is_known(self) -> bool:
        """Return True if the phone prefix was recognised."""
        return self.country is not None


_UNKNOWN = LocaleResult(None, None, None)


class FullLocaleResult(NamedTuple):
    """Full locale inference result — country + timezone + extended formatting + confidence.

    Returned by :func:`infer_full_locale`.  Superset of :class:`LocaleResult`.

    All extended formatting fields (``currency_symbol``, ``date_format``, ``vat_rate``,
    etc.) are flattened directly onto this object for convenience.  They are ``None``
    when the country is not in the extended dataset.

    Fields
    ------
    country : str | None
        ISO 3166-1 alpha-2 country code, e.g. ``"NG"``, ``"US"``, ``"DE"``.
    currency : str | None
        ISO 4217 currency code, e.g. ``"NGN"``, ``"USD"``, ``"EUR"``.
    language : str | None
        BCP 47 language tag for the primary locale, e.g. ``"en-NG"``, ``"fr-SN"``.
        Sourced from extended data when available; falls back to bare ISO 639-1 code.
    timezone : str | None
        IANA timezone string, e.g. ``"Africa/Lagos"``, ``"America/New_York"``.
        ``None`` when the country is not in the IANA database (extremely rare).
    utc_offset_hours : float | None
        Current UTC offset in hours, accounting for DST at the time of the call.
        E.g. ``1.0`` for WAT (Nigeria), ``-5.0`` for EST, ``5.5`` for IST.
    timezones : tuple[str, ...] | None
        All IANA timezones for the country, sorted.
    extended : ExtendedLocale | None
        Full formatting metadata (symbol, separators, VAT, date format, RTL, BCP 47).
        ``None`` when the country is not in the extended dataset.
    confidence : float
        Confidence of the inference:
        - ``1.0`` — phone prefix unambiguously identifies country (single-country prefix)
        - ``0.9`` — multi-country prefix; timezone used as tiebreaker (e.g. +1 → CA vs US)
        - ``0.8`` — country from timezone alone (no phone number given)
        - ``0.0`` — completely unknown

    Flattened extended fields (shortcut access, None when country not in extended dataset):
    currency_symbol, currency_before, decimal_sep, thousands_sep,
    vat_rate, vat_name, date_format, rtl, week_start, bcp47, languages

    Notes
    -----
    ``vat_rate`` is a decimal fraction (``0.075`` for 7.5 %).
    Access ``r.vat_rate * 100`` for percentage form.

    Examples
    --------
    >>> r = infer_full_locale("+2348012345678")
    >>> r.country
    'NG'
    >>> r.timezone
    'Africa/Lagos'
    >>> r.utc_offset_hours
    1.0
    >>> r.confidence
    1.0
    >>> r.currency_symbol
    '₦'
    >>> r.vat_rate
    0.075
    >>> r.date_format
    '%d/%m/%Y'
    >>> r.language       # BCP 47, not bare 'en'
    'en-NG'

    >>> r = infer_full_locale("+14165551234", browser_timezone="America/Toronto")
    >>> r.country
    'CA'
    >>> r.timezone
    'America/Toronto'
    >>> r.confidence
    0.9
    """

    country: str | None
    currency: str | None
    language: str | None
    timezone: str | None
    utc_offset_hours: float | None
    timezones: tuple | None
    extended: ExtendedLocale | None
    confidence: float
    # --- flattened extended fields ---
    currency_symbol: str | None
    currency_before: bool | None
    decimal_sep: str | None
    thousands_sep: str | None
    vat_rate: float | None
    vat_name: str | None
    date_format: str | None
    rtl: bool | None
    week_start: int | None
    bcp47: str | None
    languages: tuple | None


def _canonicalize(phone: str) -> str:
    """Strip all non-digit characters and the 'whatsapp:' prefix."""
    if phone and phone.startswith("whatsapp:"):
        phone = phone[len("whatsapp:") :]
    return "".join(c for c in (phone or "") if c.isdigit())


def infer_locale(phone_number: str) -> LocaleResult:
    """Infer country, currency, and language from a phone number.

    Uses longest-prefix-match against E.164 country calling codes.

    Parameters
    ----------
    phone_number:
        A phone number in any common format.  The following are all
        equivalent::

            "+234 801 234 5678"
            "2348012345678"
            "+2348012345678"
            "whatsapp:+2348012345678"
            "(234) 801-234-5678"

    Returns
    -------
    LocaleResult
        A named tuple ``(country, currency, language)``.  All three fields
        are ``None`` when the prefix is not recognised — the caller should
        ask the user explicitly rather than assuming a default.

    Examples
    --------
    >>> infer_locale("+2348012345678")
    LocaleResult(country='NG', currency='NGN', language='en')
    >>> infer_locale("+14155552671")
    LocaleResult(country='US', currency='USD', language='en')
    >>> infer_locale("+33612345678")
    LocaleResult(country='FR', currency='EUR', language='fr')
    >>> infer_locale("+882123456789")
    LocaleResult(country=None, currency=None, language=None)
    """
    digits = _canonicalize(phone_number)
    if not digits:
        return _UNKNOWN
    for prefix in _SORTED_PREFIXES:
        if digits.startswith(prefix):
            return LocaleResult(*PHONE_PREFIX_MAP[prefix])
    return _UNKNOWN


def infer_country(phone_number: str) -> str | None:
    """Return only the ISO 3166-1 alpha-2 country code, or None."""
    return infer_locale(phone_number).country


def infer_currency(phone_number: str) -> str | None:
    """Return only the ISO 4217 currency code, or None."""
    return infer_locale(phone_number).currency


def infer_language(phone_number: str) -> str | None:
    """Return only the ISO 639-1 language code, or None."""
    return infer_locale(phone_number).language


def is_supported(phone_number: str) -> bool:
    """Return True if the phone number prefix is recognised.

    Shortcut for ``infer_locale(phone_number).is_known()``.

    Examples
    --------
    >>> is_supported("+2348012345678")
    True
    >>> is_supported("+8821234567")
    False
    """
    return infer_locale(phone_number).is_known()


def infer_country_from_timezone(timezone: str) -> str | None:
    """Infer ISO 3166-1 alpha-2 country code from an IANA timezone string.

    Parameters
    ----------
    timezone:
        An IANA timezone string, e.g. ``"Africa/Lagos"``, ``"America/Toronto"``,
        ``"Asia/Jakarta"``.  Typically obtained from
        ``Intl.DateTimeFormat().resolvedOptions().timeZone`` in the browser.

    Returns
    -------
    str | None
        ISO country code, e.g. ``"NG"``, ``"CA"``, ``"ID"``.
        ``None`` if the timezone is unrecognised.

    Notes
    -----
    Multi-timezone countries are handled correctly:

    - Indonesia has three zones (Jakarta/Makassar/Jayapura) — all return ``"ID"``
    - Canada and USA share the +1 calling code, but their timezones are distinct
      (``"America/Toronto"`` → ``"CA"``, ``"America/New_York"`` → ``"US"``)
    - Russia's 11 zones all return ``"RU"``

    Examples
    --------
    >>> infer_country_from_timezone("Africa/Lagos")
    'NG'
    >>> infer_country_from_timezone("America/Toronto")
    'CA'
    >>> infer_country_from_timezone("America/New_York")
    'US'
    >>> infer_country_from_timezone("Asia/Jakarta")
    'ID'
    >>> infer_country_from_timezone("Asia/Makassar")
    'ID'
    >>> infer_country_from_timezone("Unknown/Zone")
    """
    if not timezone:
        return None
    return TIMEZONE_COUNTRY_MAP.get(timezone)


def supported_countries() -> list[dict[str, str]]:
    """Return a list of all supported countries with their metadata.

    Each entry is a dict with keys ``prefix``, ``country``, ``currency``,
    ``language``.  Sorted by prefix length then lexicographically.

    Useful for building country-selector dropdowns, documentation, or
    validation lists.

    Examples
    --------
    >>> entries = supported_countries()
    >>> len(entries)
    191
    >>> entries[0]
    {'prefix': '1', 'country': 'US', 'currency': 'USD', 'language': 'en'}
    """
    return [
        {
            "prefix": prefix,
            "country": country,
            "currency": currency,
            "language": language,
        }
        for prefix, (country, currency, language) in sorted(
            PHONE_PREFIX_MAP.items(), key=lambda kv: (len(kv[0]), kv[0])
        )
    ]


def get_extended(country_code: str) -> ExtendedLocale | None:
    """Return extended locale metadata for a country code, or None if unknown.

    Parameters
    ----------
    country_code:
        ISO 3166-1 alpha-2 country code, e.g. ``"NG"``, ``"DE"``, ``"US"``.
        Case-insensitive.

    Returns
    -------
    ExtendedLocale | None
        Named tuple with currency symbol, number formatting, VAT rate, date
        format, RTL flag, week start, and BCP 47 tag.  ``None`` when the
        country code is not in the extended dataset.

    Examples
    --------
    >>> ext = get_extended("NG")
    >>> ext.currency_symbol
    '₦'
    >>> ext.vat_rate
    0.075
    >>> ext.rtl
    False
    >>> get_extended("XX") is None
    True
    """
    if not country_code:
        return None
    return EXTENDED_LOCALE_MAP.get(country_code.upper())


def format_amount(value: float | int, country_code: str) -> str:
    """Format a monetary amount using the country's locale conventions.

    Places the currency symbol before or after the amount per local convention,
    uses the correct decimal and thousands separators.

    Parameters
    ----------
    value:
        The numeric amount to format, e.g. ``1234.5``.
    country_code:
        ISO 3166-1 alpha-2 country code.  Falls back to plain two-decimal
        formatting with no symbol when the country is not in the extended
        dataset.

    Returns
    -------
    str
        Formatted string, e.g. ``"₦1,234.50"``, ``"1.234,50 €"``,
        ``"R 1 234.50"``.

    Examples
    --------
    >>> format_amount(1234.5, "NG")
    '₦1,234.50'
    >>> format_amount(1234.5, "DE")
    '1.234,50 €'
    >>> format_amount(1234.5, "FR")
    '1 234,50 €'
    >>> format_amount(1234.5, "US")
    '$1,234.50'
    >>> format_amount(1234.5, "ZA")
    'R 1 234.50'
    """
    ext = get_extended(country_code)
    if ext is None:
        return f"{value:.2f}"

    # Build the numeric part with correct separators
    int_part, dec_part = f"{abs(value):.2f}".split(".")

    # Insert thousands separators
    groups: list[str] = []
    while len(int_part) > 3:
        groups.append(int_part[-3:])
        int_part = int_part[:-3]
    groups.append(int_part)
    int_formatted = ext.thousands_sep.join(reversed(groups))

    numeric = f"{int_formatted}{ext.decimal_sep}{dec_part}"
    sign = "-" if value < 0 else ""

    if ext.currency_before:
        return f"{sign}{ext.currency_symbol}{numeric}"
    else:
        return f"{sign}{numeric} {ext.currency_symbol}"


# ---------------------------------------------------------------------------
# v2.0.0 — timezone utilities (pure stdlib, zero deps)
# ---------------------------------------------------------------------------


def _utc_offset_hours(iana_tz: str) -> float | None:
    """Return the current UTC offset for an IANA timezone string, in decimal hours.

    Accounts for DST at the current moment.  Uses Python stdlib ``zoneinfo``
    (Python 3.9+) — no third-party packages required.

    Returns ``None`` only if the IANA string is invalid.
    """
    try:
        zi = ZoneInfo(iana_tz)
        now_utc = datetime.now(_stdlib_tz.utc)
        offset = now_utc.astimezone(zi).utcoffset()
        if offset is None:
            return None
        return offset.total_seconds() / 3600.0
    except (ZoneInfoNotFoundError, Exception):
        return None


def infer_timezone(country_code: str) -> str | None:
    """Return the primary IANA timezone for a country code.

    For single-timezone countries this is the only zone.
    For multi-timezone countries this is the capital / most-populated zone.

    Parameters
    ----------
    country_code:
        ISO 3166-1 alpha-2 country code, case-insensitive.

    Returns
    -------
    str | None
        IANA timezone string, e.g. ``"Africa/Lagos"``, ``"America/New_York"``.
        ``None`` when the country code is not recognised.

    Notes
    -----
    Multi-timezone behaviour:

    - ``"US"`` → ``"America/New_York"`` (Eastern; most-populated)
    - ``"CA"`` → ``"America/Toronto"``
    - ``"RU"`` → ``"Europe/Moscow"``
    - ``"BR"`` → ``"America/Sao_Paulo"``
    - ``"ID"`` → ``"Asia/Jakarta"`` (WIB, most-populated)
    - ``"AU"`` → ``"Australia/Sydney"``
    - ``"IN"`` → ``"Asia/Kolkata"`` (single zone — IST is uniform across all of India)
    - ``"CN"`` → ``"Asia/Shanghai"`` (legally uniform)

    To get ALL timezones for a country, use :func:`infer_timezones`.

    Examples
    --------
    >>> infer_timezone("NG")
    'Africa/Lagos'
    >>> infer_timezone("US")
    'America/New_York'
    >>> infer_timezone("CA")
    'America/Toronto'
    >>> infer_timezone("ID")
    'Asia/Jakarta'
    >>> infer_timezone("XX")
    """
    if not country_code:
        return None
    return COUNTRY_PRIMARY_TZ.get(country_code.upper())


def infer_timezones(country_code: str) -> tuple[str, ...]:
    """Return ALL IANA timezones for a country code, sorted alphabetically.

    For single-timezone countries returns a one-element tuple.
    For multi-timezone countries returns every IANA zone.

    Parameters
    ----------
    country_code:
        ISO 3166-1 alpha-2 country code, case-insensitive.

    Returns
    -------
    tuple[str, ...]
        All IANA timezone strings, alphabetically sorted.
        Empty tuple when the country code is not recognised.

    Examples
    --------
    >>> infer_timezones("NG")
    ('Africa/Lagos',)
    >>> len(infer_timezones("US"))  # 30+ zones
    30
    >>> "America/Toronto" in infer_timezones("CA")
    True
    >>> infer_timezones("ID")
    ('Asia/Jakarta', 'Asia/Jayapura', 'Asia/Makassar', ...)
    """
    if not country_code:
        return ()
    return COUNTRY_ALL_TZ.get(country_code.upper(), ())


def get_utc_offset(country_code_or_tz: str) -> float | None:
    """Return the current UTC offset in decimal hours for a country or IANA timezone.

    Accepts either an ISO 3166-1 alpha-2 country code OR an IANA timezone string.
    Resolves the primary timezone first when a country code is given.
    Accounts for DST at the moment of the call.

    Parameters
    ----------
    country_code_or_tz:
        Either a 2-letter country code (e.g. ``"NG"``, ``"US"``) or a full
        IANA timezone string (e.g. ``"America/New_York"``, ``"Africa/Lagos"``).

    Returns
    -------
    float | None
        UTC offset in decimal hours.  Positive = ahead of UTC, negative = behind.
        Half-hour and quarter-hour offsets are represented as decimals
        (e.g. India → ``5.5``, Nepal → ``5.75``, Newfoundland → ``-3.5``).
        ``None`` when the input is not recognised.

    Examples
    --------
    >>> get_utc_offset("NG")    # WAT — always UTC+1, no DST
    1.0
    >>> get_utc_offset("GB")    # BST in summer, GMT in winter
    1.0  # or 0.0 depending on DST
    >>> get_utc_offset("IN")    # IST — always UTC+5:30
    5.5
    >>> get_utc_offset("NP")    # NPT — always UTC+5:45
    5.75
    >>> get_utc_offset("America/New_York")  # accepts IANA directly
    -4.0  # or -5.0 depending on DST
    """
    if not country_code_or_tz:
        return None
    val = country_code_or_tz.strip()
    # If it looks like a country code (≤ 2 chars, no slash), resolve to primary tz
    if len(val) <= 2 and "/" not in val:
        tz = COUNTRY_PRIMARY_TZ.get(val.upper())
        if tz is None:
            return None
        return _utc_offset_hours(tz)
    # Otherwise treat as IANA timezone string directly
    return _utc_offset_hours(val)


def get_local_datetime(
    dt: datetime,
    country_code_or_tz: str,
) -> datetime:
    """Convert a UTC (or aware) datetime to local time for a country or IANA timezone.

    The returned datetime is timezone-aware and carries the correct IANA zone.

    Parameters
    ----------
    dt:
        A UTC or timezone-aware datetime.  Naive datetimes are assumed to be UTC.
    country_code_or_tz:
        Either a 2-letter country code (``"NG"``, ``"US"``) or an IANA timezone
        string (``"America/New_York"``).  Country codes resolve to the primary zone.

    Returns
    -------
    datetime
        Timezone-aware datetime in the target local time.

    Raises
    ------
    ValueError
        When the country or timezone is unrecognised, or the IANA key is invalid.

    Notes
    -----
    The conversion is pure arithmetic using the IANA database embedded in Python's
    ``zoneinfo`` stdlib module (Python 3.9+).  No network calls.  No probabilistic
    estimation.  The result is mathematically exact.

    Examples
    --------
    >>> from datetime import datetime, timezone
    >>> utc = datetime(2025, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    >>> local = get_local_datetime(utc, "NG")
    >>> local.hour   # WAT = UTC+1
    13
    >>> local = get_local_datetime(utc, "America/New_York")  # EST = UTC-5 in January
    >>> local.hour
    7
    """
    # Resolve timezone
    tz_str: str | None
    val = (country_code_or_tz or "").strip()
    if len(val) <= 2 and "/" not in val:
        tz_str = COUNTRY_PRIMARY_TZ.get(val.upper())
        if tz_str is None:
            raise ValueError(f"Unknown country code: {country_code_or_tz!r}")
    else:
        tz_str = val

    try:
        zi = ZoneInfo(tz_str)
    except ZoneInfoNotFoundError:
        raise ValueError(f"Unknown IANA timezone: {tz_str!r}") from None

    # Make dt UTC-aware if it is naive
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_stdlib_tz.utc)

    return dt.astimezone(zi)


def format_local_datetime(
    dt: datetime,
    country_code_or_tz: str,
    *,
    include_time: bool = True,
    include_seconds: bool = False,
) -> str:
    """Format a UTC datetime as a locale-aware local time string.

    Uses the country's ``date_format`` from extended data for the date portion.
    Falls back to ISO format (``%Y-%m-%d``) when the country is not in the
    extended dataset.

    Parameters
    ----------
    dt:
        UTC or timezone-aware datetime.  Naive datetimes are assumed to be UTC.
    country_code_or_tz:
        Country code or IANA timezone string.
    include_time:
        If ``True`` (default), appends ``" HH:MM"`` to the date.
    include_seconds:
        If ``True``, appends seconds (``" HH:MM:SS"``).  Ignored when
        ``include_time=False``.

    Returns
    -------
    str
        Human-readable local datetime string.

    Examples
    --------
    >>> from datetime import datetime, timezone
    >>> utc = datetime(2025, 6, 14, 11, 30, 0, tzinfo=timezone.utc)
    >>> format_local_datetime(utc, "NG")
    '14/06/2025 12:30'
    >>> format_local_datetime(utc, "US")
    '06/14/2025 07:30'
    >>> format_local_datetime(utc, "DE")
    '14.06.2025 13:30'
    >>> format_local_datetime(utc, "SE")
    '2025-06-14 13:30'
    >>> format_local_datetime(utc, "NG", include_time=False)
    '14/06/2025'
    """
    local = get_local_datetime(dt, country_code_or_tz)

    # Resolve country code for extended data
    val = (country_code_or_tz or "").strip()
    country: str | None = (
        val.upper()
        if len(val) <= 2 and "/" not in val
        else TIMEZONE_COUNTRY_MAP.get(val)
    )

    ext = get_extended(country) if country else None
    date_fmt = ext.date_format if ext else "%Y-%m-%d"

    if not include_time:
        return local.strftime(date_fmt)

    time_fmt = "%H:%M:%S" if include_seconds else "%H:%M"
    return local.strftime(f"{date_fmt} {time_fmt}")


def _resolve_area_code(
    digits: str,
    calling_code: str,
) -> dict | None:
    """Look up area code data for a normalised digit string and its calling code.

    Returns the AREA_CODE_MAP entry dict, or None if not found.
    Tries longest-match on the subscriber portion after the calling code.

    For +1 (NANP) numbers: tries the 3-digit NPA.
    For other countries: tries 2-3 digit area codes.
    """
    code_map = AREA_CODE_MAP.get(calling_code)
    if not code_map:
        return None

    subscriber = digits[len(calling_code) :]  # digits after the calling code
    if not subscriber:
        return None

    # Try 4-digit, 3-digit, 2-digit prefixes in that order (longest match)
    for length in (4, 3, 2):
        prefix = subscriber[:length]
        if prefix in code_map:
            return code_map[prefix]

    return None


def infer_full_locale(
    phone_number: str,
    *,
    browser_timezone: str | None = None,
) -> FullLocaleResult:
    """Infer complete locale from a phone number, optionally confirmed by browser timezone.

    This is the primary v2.0.0 entry point.  It chains all inference signals:

    1. Phone prefix → country, currency, language (longest-prefix-match)
    2. Ambiguity resolution: when prefix is shared by multiple countries
       (e.g. ``+1`` for both USA and Canada), ``browser_timezone`` is used as
       tiebreaker → confidence 0.9
    3. Falls back to phone-only inference at confidence 1.0 for unambiguous prefixes
    4. Falls back to timezone-only if phone is missing/unknown → confidence 0.8

    Parameters
    ----------
    phone_number:
        Phone number in any format.  Accepts E.164, bare digits, with dashes/spaces,
        ``whatsapp:+...`` prefix.  May be empty or ``None`` — in that case
        ``browser_timezone`` must be provided for any inference.
    browser_timezone:
        IANA timezone string from the browser's
        ``Intl.DateTimeFormat().resolvedOptions().timeZone``.
        Optional but improves disambiguation for +1 (US vs CA), +7 (Russia vs Kazakhstan), etc.

    Returns
    -------
    FullLocaleResult
        Named tuple with country, currency, language, timezone, utc_offset_hours,
        extended, and confidence.  All fields are ``None`` / ``0.0`` when inference fails.

    Examples
    --------
    >>> r = infer_full_locale("+2348012345678")
    >>> (r.country, r.timezone, r.utc_offset_hours, r.confidence)
    ('NG', 'Africa/Lagos', 1.0, 1.0)

    >>> r = infer_full_locale("+14165551234", browser_timezone="America/Toronto")
    >>> (r.country, r.timezone, r.confidence)
    ('CA', 'America/Toronto', 0.9)

    >>> r = infer_full_locale("+14155552671", browser_timezone="America/Los_Angeles")
    >>> (r.country, r.timezone, r.confidence)
    ('US', 'America/Los_Angeles', 0.9)

    >>> r = infer_full_locale("", browser_timezone="Africa/Lagos")
    >>> (r.country, r.confidence)
    ('NG', 0.8)
    """
    _EMPTY = FullLocaleResult(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        0.0,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )

    # ── Step 1: phone inference ──────────────────────────────────────────────
    locale = infer_locale(phone_number or "")
    phone_country = locale.country  # None if unknown/empty

    # ── Step 1b: area code resolution (e.g. +1-416 → CA without browser tz) ──
    area_info: dict | None = None
    area_country: str | None = None
    area_tz: str | None = None

    if phone_country is not None:
        digits = _canonicalize(phone_number or "")
        # Find the matched prefix length
        for prefix in _SORTED_PREFIXES:
            if (
                digits.startswith(prefix)
                and PHONE_PREFIX_MAP.get(prefix, ("",))[0] == phone_country
            ):
                area_info = _resolve_area_code(digits, prefix)
                break
        if area_info:
            area_country = area_info.get("country")
            area_tzs = area_info.get("timezones", [])
            # Prefer COUNTRY_PRIMARY_TZ if it appears in area_tzs (avoids legacy aliases
            # like Europe/Guernsey appearing before Europe/London in the list).
            primary_tz = COUNTRY_PRIMARY_TZ.get(phone_country or "")
            if primary_tz and primary_tz in area_tzs:
                area_tz = primary_tz
            else:
                area_tz = area_tzs[0] if area_tzs else None

    # ── Step 2: browser timezone signal ─────────────────────────────────────
    tz_country: str | None = None
    resolved_tz: str | None = None

    if browser_timezone:
        tz_country = TIMEZONE_COUNTRY_MAP.get(browser_timezone)
        resolved_tz = browser_timezone if tz_country else None

    # ── Step 3: combine signals → final country + confidence ────────────────
    # Priority: area_code > browser_timezone > phone_prefix
    final_country: str | None
    confidence: float

    if phone_country is not None:
        if area_country is not None and area_country != phone_country:
            # Area code resolves to a different country (e.g. +1-416 → CA, not US)
            # This is the highest-quality disambiguation — no browser needed
            final_country = area_country
            confidence = 0.95
            if area_tz is not None:
                resolved_tz = area_tz  # e.g. America/Toronto for 416
        elif tz_country is not None and tz_country != phone_country:
            # Phone and timezone disagree → trust timezone (more specific)
            # This resolves CA vs US for +1, RU vs KZ for +7, etc.
            final_country = tz_country
            confidence = 0.9
        elif area_country is not None and area_country == phone_country:
            # Area code confirms phone prefix — full confidence
            # Only use area_tz when it gives disambiguation value (multi-tz countries)
            final_country = phone_country
            confidence = 1.0
            country_zones = COUNTRY_ALL_TZ.get(phone_country or "", ())
            if area_tz is not None and resolved_tz is None and len(country_zones) > 1:
                resolved_tz = area_tz
        else:
            # Phone matches (or no timezone signal) — full confidence
            final_country = phone_country
            confidence = 1.0
    elif tz_country is not None:
        # No phone number or unknown prefix — fall back to timezone
        final_country = tz_country
        confidence = 0.8
    else:
        return _EMPTY

    # ── Step 4: rebuild currency + language from winning country ─────────────
    # When timezone or area code won the tiebreak, re-read from PHONE_PREFIX_MAP
    # for the winning country so currency/language are consistent.
    if final_country != phone_country and final_country is not None:
        # Find the prefix entry for the winning country
        for prefix in _SORTED_PREFIXES:
            entry = PHONE_PREFIX_MAP.get(prefix)
            if entry and entry[0] == final_country:
                currency = entry[1]
                language = entry[2]
                break
        else:
            currency = locale.currency
            language = locale.language
    else:
        currency = locale.currency
        language = locale.language

    # ── Step 5: resolve timezone for the winning country ─────────────────────
    if resolved_tz is None:
        # Use browser_timezone if it belongs to the winning country
        if (
            browser_timezone
            and TIMEZONE_COUNTRY_MAP.get(browser_timezone) == final_country
        ):
            resolved_tz = browser_timezone
        else:
            resolved_tz = COUNTRY_PRIMARY_TZ.get(final_country)

    utc_offset = _utc_offset_hours(resolved_tz) if resolved_tz else None
    all_timezones = COUNTRY_ALL_TZ.get(final_country) if final_country else None
    extended = get_extended(final_country)

    # ── Step 6: upgrade language to BCP 47; flatten extended fields ──────────
    # Prefer the BCP 47 tag from extended data (e.g. "en-NG") over the bare
    # ISO 639-1 code from the phone prefix map (e.g. "en").
    bcp47_language: str | None = extended.bcp47 if extended is not None else language

    return FullLocaleResult(
        country=final_country,
        currency=currency,
        language=bcp47_language,
        timezone=resolved_tz,
        utc_offset_hours=utc_offset,
        timezones=all_timezones,
        extended=extended,
        confidence=confidence,
        # flattened from extended
        currency_symbol=extended.currency_symbol if extended else None,
        currency_before=extended.currency_before if extended else None,
        decimal_sep=extended.decimal_sep if extended else None,
        thousands_sep=extended.thousands_sep if extended else None,
        vat_rate=extended.vat_rate if extended else None,
        vat_name=extended.vat_name if extended else None,
        date_format=extended.date_format if extended else None,
        rtl=extended.rtl if extended else None,
        week_start=extended.week_start if extended else None,
        bcp47=extended.bcp47 if extended else None,
        languages=extended.languages if extended else None,
    )


__all__ = [
    "LocaleResult",
    "FullLocaleResult",
    "ExtendedLocale",
    "infer_locale",
    "infer_full_locale",
    "infer_country",
    "infer_currency",
    "infer_language",
    "infer_country_from_timezone",
    "infer_timezone",
    "infer_timezones",
    "get_utc_offset",
    "get_local_datetime",
    "format_local_datetime",
    "is_supported",
    "supported_countries",
    "get_extended",
    "format_amount",
]
